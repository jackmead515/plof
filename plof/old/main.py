from collections import deque
import time

from plof.pipe import Pipe
from plof.metric import Aggregator
from plof.parse import Parser
from plof.config import initialize, get_config

import plotext as plot
            
def main():
    initialize()

    config = get_config()

    pipe = Pipe(config)
    aggregator = Aggregator(config)
    parser = Parser(config)

    x = range(1, config.buffer_size+1)
    y = deque(maxlen=config.buffer_size)
    [y.append(config.default_value) for _ in x]
        
    plot.title(f"{config.metric} of value every {config.refresh} seconds")
    plot.clear_color()
    plot.grid(False, False)
    plot.frame(True)
    plot.ylim(config.y_lower_limit, config.y_upper_limit)

    while True:
        values = pipe.read()
        values = parser.parse(values)
        values = aggregator.compute(values)

        y.appendleft(values.get(config.metric))

        plot.clear_data()
        plot.clear_terminal()
        plot.plot(x, list(y), marker=".")
        plot.show()

        print(values)


if __name__ == "__main__":
    main()