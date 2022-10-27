from dataclasses import dataclass


@dataclass
class PlotConfig:

    type: str

    config: dict