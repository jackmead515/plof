import sys
import os

from jsonpointer import resolve_pointer

def plot(config):
    file_config = config.get('plot').get('config')

    path = file_config.get('path')
    mode = file_config.get('mode')
    pointer = file_config.get('pointer')

    if not os.path.exists(path):
        os.makedirs(os.path.dirname(path), exist_ok=True)

    file = open(path, mode)

    def plotter(state):
        try:
            if pointer:
                file.write(f'{resolve_pointer(state, pointer)}')
            else:
                file.write(f'{state}')
            
            file.write('\n')
            file.flush()
        except:
            file.close()

    return plotter