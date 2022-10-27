import sys
import os

import plotext as plotext
from jsonpointer import resolve_pointer

import stages.plot.file_plot as file_plot
import stages.plot.line_plot as line_plot

def pretty_table(rows, column_count, column_spacing=4):
    aligned_columns = []
    for column in range(column_count):
        column_data = list(map(lambda row: row[column], rows))
        aligned_columns.append((max(map(len, column_data)) + column_spacing, column_data))

    for row in range(len(rows)):
        aligned_row = map(lambda x: (x[0], x[1][row]), aligned_columns)
        yield ''.join(map(lambda x: x[1] + ' ' * (x[0] - len(x[1])), aligned_row))


def get_table_func(config):
    table_config = config.get('plot').get('config')

    columns = table_config.get('columns')

    column_names = list(map(lambda x: x.get('name'), columns))
    column_pointers = list(map(lambda x: x.get('pointer'), columns))

    table_data = []
    table_data.append(column_names)

    def plotter(state):

        row = []
        for pointer in column_pointers:
            row.append(str(resolve_pointer(state, pointer)))
        table_data.append(row)

        print("\033c", end='')
        for line in pretty_table(table_data, len(column_names)):
            print(line)

    return plotter


def plot(config):
    """Plot the data from the pipe."""

    if config.get('plot').get('type') == 'line':
        return line_plot.plot(config)
    
    if config.get('plot').get('type') == 'table':
        return get_table_func(config)

    if config.get('plot').get('type') == 'file':
        return file_plot.plot(config)

    # default is to just print the state to standard output
    def plotter(state):
        print(state, sep='\n', file=sys.stdout)

    return plotter