

def python_code(config):
    func = eval(config.get('config').get('code'))

    def parser(state):
        state['parse']['data'] = func(state)
        return state

    return parser