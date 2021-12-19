import argparse
from dataclasses import dataclass
from enum import Enum


class ContentType(Enum):
    RAW = 'raw'
    JSON = 'json'
    CSV = 'csv'


@dataclass
class Config:
    host: str
    port: int
    pipe: bool
    timeout: float
    delimiter: str
    refresh: float
    buffer_size: int
    metric: str
    content_type: ContentType
    json_field: str
    csv_field: str
    y_upper_limit: float
    y_lower_limit: float
    x_limit: float
    default_value: float


config: Config = None

def get_config() -> Config:
    global config
    return config


def initialize():
    global config

    parser = argparse.ArgumentParser(description="Plof -> Graph To Terminal")

    parser.add_argument("-ylim", dest="ylim", type=str, default="1.0,100.0", help="Limit the y axis too min and max")
    parser.add_argument("-xlim", dest="xlim", type=float, default=100.0, help="Limit the points on x axis")
    parser.add_argument("-metric", dest="metric", type=str, default="avg", help="One of: avg, med, std, sum, total, min, max")

    parser.add_argument("-type", dest="type", type=str, default="raw", help="Content type: raw, json, csv")
    parser.add_argument("-csv", dest="csv", type=str, default="0,1", help="csv column numbers to parse. i.e: time,value. EX: 0,5")
    parser.add_argument("-json", dest="json", type=str, default="value", help="jq syntax to parse the value from. EX: 'content?.nested?.value'")
    parser.add_argument("-dlim", dest="dlim", type=str, default='\n', help="The input line deliminator")

    #parser.add_argument("-title", dest="title", type=str, default='plof data', help="The title of the graph")

    parser.add_argument("-default", dest="default", type=float, default=0, help="default value if input cannot be parsed")
    parser.add_argument("-refresh", dest="refresh", type=float, default=5.0, help="refresh speed of the graph")
    parser.add_argument("-timeout", dest="timeout", type=float, default=1.0, help="timeout of pipe or tcp host")
    parser.add_argument("-buffer", dest="buffer", type=int, default=100, help="how many data points to store before graph refresh")
    parser.add_argument("-pipe", dest="pipe", action="store_true", help="accept input from standard input")
    parser.add_argument("-host", dest="host", type=str, help="ip address of the input")
    parser.add_argument("-port", dest="port", type=int, help="port of the input")
    
    args = parser.parse_args()

    strip_split = lambda f: [m.strip() for m in f.strip().split(',')]
    y_lower_limit, y_upper_limit = strip_split(args.ylim)

    config = Config(
        host=args.host,
        port=args.port,
        pipe=args.pipe,
        delimiter=args.dlim,
        timeout=args.timeout,
        refresh=args.refresh,
        buffer_size=args.buffer,
        metric=args.metric,
        content_type=ContentType(args.type),
        json_field=args.json,
        csv_field=args.csv,
        y_upper_limit=y_upper_limit,
        y_lower_limit=y_lower_limit,
        x_limit=args.xlim,
        default_value=args.default
    )