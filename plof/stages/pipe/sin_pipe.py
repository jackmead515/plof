
import time
import math

from util.time import parse_elapsed_time


def pipe(config):

    pipe_config = config.get('pipe').get('config')
    poll_time = parse_elapsed_time(pipe_config.get('poll')) 
    amplitude = pipe_config.get('amplitude', 1)

    while True:

        start_time = time.time()

        value = str(amplitude * math.sin(start_time))

        elapsed = time.time() - start_time

        result = {
            'pipe': {
                'data': value,
                'elapsed': elapsed,
                'time': start_time
            }
        }

        yield result

        sleep_time = poll_time - elapsed
        if sleep_time > 0:
            time.sleep(sleep_time)