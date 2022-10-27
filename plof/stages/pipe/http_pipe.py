
import requests
import time

from util.time import parse_elapsed_time

def get_http_function(method):
    if method == 'get':
        return requests.get
    elif method == 'post':
        return requests.post
    elif method == 'put':
        return requests.put
    elif method == 'delete':
        return requests.delete
    else:
        raise Exception(f'Invalid method: {method}')


def pipe(config):

    pipe_config = config.get('pipe').get('config')

    url = pipe_config.get('url')
    method = pipe_config.get('method')
    params = pipe_config.get('params')
    headers = pipe_config.get('headers')
    request_data = pipe_config.get('data')
    poll = pipe_config.get('poll')

    poll_time = parse_elapsed_time(poll) 

    http_function = get_http_function(method)

    while True:

        start_time = time.time()

        response = http_function(
            url,
            params=params,
            data=request_data,
            headers=headers
        )

        data = response.text

        elapsed = time.time() - start_time

        print(f'Pipe {method} {url} took {elapsed} seconds')

        yield {
            'pipe': {
                'data': data,
                'elapsed': elapsed,
                'time': start_time
            }
        }

        sleep_time = poll_time - elapsed
        if sleep_time > 0:
            time.sleep(sleep_time)

