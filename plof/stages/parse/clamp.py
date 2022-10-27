
def clamp(config):

    minn = config.get('config').get('min')
    maxx = config.get('config').get('max')

    def parser(state):
        data = state['parse']['data']

        if data < minn:
            data = minn
        elif data > maxx:
            data = maxx

        state['parse']['data'] = data

        return state

    return parser