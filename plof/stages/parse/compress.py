import zlib

def compress(config):
    type = config.get('config').get('type')
    level = config.get('config').get('level', 9)

    def parser(state):
        if type == 'gzip':
            state['parse']['data'] = zlib.compress(state['parse']['data'], level)
        else:
            raise Exception('Unknown compress type: {}'.format(type))
        return state

    return parser