import math
import statistics

from plof.config import Config

class Metric:
    def compute(self, values):
        pass


class Average(Metric):
    def compute(self, values):
        if len(values) <= 0:
            return 0
        return statistics.mean(values)


class Median(Metric):
    def compute(self, values):
        if len(values) <= 0:
            return 0
        return statistics.median(values)


class Sum(Metric):
    def compute(self, values):
        return sum(values)


class Total(Metric):
    def compute(self, values):
        return len(values)


class Min(Metric):
    def compute(self, values):
        if len(values) <= 0:
            return 0
        return min(values)


class Max(Metric):
    def compute(self, values):
        if len(values) <= 0:
            return 0
        return max(values)


class SDeviation(Metric):
    def compute(self, values):
        if len(values) <= 0:
            return 0
        return statistics.stdev(values)


class Aggregator(Metric):

    def __init__(self, config: Config):
        self.config = config
        self.aggregators: 'dict[Metric]' = {
            'avg': Average(),
            'min': Min(),
            'max': Max(),
            'med': Median(),
            'sum': Sum(),
            'total': Total(),
            'std': SDeviation()
        }


    def compute(self, values) -> float:
        return self.aggregators[self.config.metric].compute(values)

