from jsonpointer import resolve_pointer

def rolling_average(config):
    window_size = config.get('config').get('window')
    pointer = config.get('config').get('pointer')
    window = []

    def parser(state):
        data = state['parse']['data']

        value = data
        if pointer:
            value = resolve_pointer(data, pointer)

        window.append(value)

        if len(window) > window_size:
            window.pop(0)

        rolling_average = sum(window) / len(window)

        state['parse']['data'] = rolling_average

        return state

    return parser