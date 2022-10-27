import json
import datetime

def cast(config):
    cast_type = config.get('config').get('cast')
    dateformat = config.get('config').get('dateformat')
    encoding = config.get('config').get('encoding', 'utf-8')

    def parser(state):
        if cast_type == 'float':
            state['parse']['data'] = float(state['parse']['data'])
        elif cast_type == 'int':
            state['parse']['data'] = int(state['parse']['data'])
        elif cast_type == 'str':
            state['parse']['data'] = str(state['parse']['data'])
        elif cast_type == 'json':
            state['parse']['data'] = json.loads(state['parse']['data'])
        elif cast_type == 'bytes':
            state['parse']['data'] = bytes(state['parse']['data'], encoding)
        elif cast_type == 'datetime':
            state['parse']['data'] = datetime.strptime(state['parse']['data'], dateformat)
        else:
            raise Exception('Unknown cast type: {}'.format(cast_type))

        return state

    return parser
