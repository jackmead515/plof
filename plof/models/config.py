from dataclasses import dataclass

from models.pipe_config import PipeConfig
from models.parse_config import ParseConfig
from models.plot_config import PlotConfig

@dataclass
class Config:

    pipe: PipeConfig

    parse: ParseConfig

    plot: PlotConfig