__version__ = "0.0.1"

import sys
import os
from copy import deepcopy
import json

from jsonschema import validate
import yaml

from stages import pipe, parse, plot

if __name__ == "__main__":

    config = sys.argv[1:]

    config_path = config[0]

    with open("./schema.json", "r") as f:
        schema = json.load(f)

    if os.path.isfile(config_path):
        with open(config_path, 'r') as stream:
            config = yaml.safe_load(stream)

    validate(config, schema)

    # type: file
    #     config:
    #         path: "./data.txt"
    #         mode: a

    piper = pipe.pipe(config)
    parser = parse.parse(config)
    plotter = plot.plot(config)

    for state in piper:

        # default the parse state to the pipe. The parse
        # stage is not required
        state['parse'] = deepcopy(state['pipe'])

        plotter(parser(state))