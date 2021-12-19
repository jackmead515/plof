import math
import sys
import time
import random
import json

import argparse

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Generate Test Plof Data")

    parser.add_argument("-mult", dest="mult", type=float, default=1, help="multiplier for function")
    parser.add_argument("-json", dest="json", action="store_true", help="generate data in json format")
    parser.add_argument("-sin", dest="sin", action="store_true", help="generate sin wave")
    parser.add_argument("-log", dest="log", action="store_true", help="generate log curve")
    parser.add_argument("-random", dest="random", action="store_true", help="generate random data")
    parser.add_argument("-sleep", dest="sleep", type=float, default=0.1, help="sleep delay")

    args = parser.parse_args()

    i = 0

    while True:
        i += 1

        value = 0
        func = None

        if args.sin:
            func = math.sin
        elif args.log:
            func = math.log
        elif args.random:
            func = lambda f: random.random()

        value = func(i) * args.mult

        if args.json:
            value = json.dump({'value': value, 'content': { 'nested': { 'value': value } }})

        print(value, file=sys.stdout, flush=True)
        time.sleep(args.sleep)