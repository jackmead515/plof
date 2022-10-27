
import time
import random
import string

from util.time import parse_elapsed_time


def pipe(config):

    pipe_config = config.get('pipe').get('config')
    poll_time = parse_elapsed_time(pipe_config.get('poll')) 
    size = pipe_config.get('size')

    while True:

        start_time = time.time()

        random_string = ''.join(random.choices(
            string.ascii_uppercase + string.digits, k=size
        ))

        elapsed = time.time() - start_time

        result = {
            'pipe': {
                'data': random_string,
                'elapsed': elapsed,
                'time': start_time
            }
        }

        yield result

        sleep_time = poll_time - elapsed
        if sleep_time > 0:
            time.sleep(sleep_time)