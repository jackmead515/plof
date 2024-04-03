import sys
import os
import csv

from jsonpointer import resolve_pointer

def plot(config):
    file_config = config.get('plot').get('config')

    path = file_config.get('path')
    headers = file_config.get('headers')
    mode = file_config.get('mode', 'w')
    pointer = file_config.get('pointer')

    already_exists = os.path.exists(path)
    if not already_exists:
        os.makedirs(os.path.dirname(path), exist_ok=True)

    # TODO add error handling
    # We want to handle errors that occur with failing to open the file due
    # to permissions or other issues with malformed data
    file = open(path, mode, newline='')
    writer = csv.writer(file, delimiter=',')
    
    # write headers if file is created
    # TODO: test if the first line in the file is the header
    if not already_exists:
        writer.writerow(headers)

    def plotter(state):
        try:
            writer.writerow(resolve_pointer(state, pointer))
        except:
            file.close()

    return plotter