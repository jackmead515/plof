from jsonpointer import resolve_pointer

def pointer(config):

    pointer = config.get('config')

    def parser(state):
        data = state['parse']['data']

        state['parse']['data'] = resolve_pointer(data, pointer)

        return state

    return parser