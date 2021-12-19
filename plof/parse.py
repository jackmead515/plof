import json

from plof.config import Config, ContentType

import jq

def safe_cast(value, cast, default=None):
    try:
        return cast(value)
    except ValueError:
        return default


def safe_json_loads(value, default=None):
    try:
        return json.loads(value)
    except json.decoder.JSONDecodeError:
        return default


class Parser:


    def __init__(self, config: Config):
        self.config = config
        #self.json_parser = jq.compile(self.config.json_field)


    def parse_raw(self, values):
        parsed = []
        for value in values:
            pvalue = safe_cast(value, float)
            if pvalue is not None:
                parsed.append(pvalue)
        return parsed

    
    def parse_json(self, values):
        parsed = []
        for value in values:
            jvalue = self.json_parser.input(value).first()
            jvalue = safe_cast(jvalue, float)
            if jvalue is not None:
               parsed.append(jvalue)
        return parsed


    def parse_csv(self, values):
        pass

    
    def parse(self, values) -> 'list[float]':

        if self.config.content_type == ContentType.RAW:
            return self.parse_raw(values)
        
        if self.config.content_type == ContentType.JSON:
            return self.parse_json(values)
        
        if self.config.content_type == ContentType.CSV:
            return self.parse_csv(values)
         