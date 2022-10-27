from dataclasses import dataclass


@dataclass
class ParseConfig:

    type: str

    config: dict

@dataclass
class ParseResult:

    data: 'list[float, float]'

    elapsed: float

    time: float