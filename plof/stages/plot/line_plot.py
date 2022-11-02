import plotext as plotext
from jsonpointer import resolve_pointer

def plot(config):
    line_config = config.get('plot').get('config')

    x_pointer = line_config.get('x')
    y_pointer = line_config.get('y')
    max_points = line_config.get('points', 20)
    marker = line_config.get('marker', '·')

    plotext.title(line_config.get('title'))
    plotext.clear_color()
    plotext.grid(False, False)
    plotext.frame(True)
    plotext.ylim(-50, 50)

    xs = []
    ys = []

    def plotter(state):

        x = state['parse']['time']
        if x_pointer:
            x = resolve_pointer(state, x_pointer)

        y = state['parse']['data']
        if y_pointer:
            y = resolve_pointer(state, y_pointer)

        xs.append(x)
        ys.append(y)

        if len(xs) > max_points:
            xs.pop(0)
            ys.pop(0)

        plotext.clt()
        plotext.cld()
        plotext.plot(xs, ys, marker=marker)
        plotext.show()

    return plotter