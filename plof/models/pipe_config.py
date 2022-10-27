from dataclasses import dataclass


@dataclass
class PipeConfig:

    type: str

    config: dict


@dataclass
class PipeResult:

    data: str

    elapsed: float

    time: float