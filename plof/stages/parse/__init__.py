import time

from util.time import parse_elapsed_time

from .clamp import clamp
from .compress import compress
from .cast import cast
from .rolling_average import rolling_average
from .python_code import python_code
from .pointer import pointer

# from .average import average
# from .mode import mode
# from .regex import regex
# from .split import split
# from .mapper import mapper

def reduce_func(funcs):
    def func(state):
        start_time = time.time()

        for f in funcs:
            state = f(state)

        elapsed = time.time() - start_time

        state['parse']['elapsed'] = elapsed
        state['parse']['time'] = start_time

        return state
    return func


def get_parse_func(config):
    if config.get('type') == 'python':
        return python_code(config)
    
    if config.get('type') == 'rolling_average':
        return rolling_average(config)

    if config.get('type') == 'clamp':
        return clamp(config)

    if config.get('type') == 'cast':
        return cast(config)

    if config.get('type') == 'pointer':
        return pointer(config)
    
    if config.get('type') == 'compress':
        return compress(config)

    # default to finding the length of the data
    def parser(state):
        return {
            'data': len(state['parse']['data']),
            'time': time.time()
        }

    return parser


def parse(config):

    parse_config = config.get('parse')

    funcs = []

    if isinstance(parse_config, list):
        for pconfig in parse_config:
            funcs.append(get_parse_func(pconfig))
    else:
        funcs.append(get_parse_func(parse_config))

    return reduce_func(funcs)