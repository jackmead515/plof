import socket

from jsonpointer import resolve_pointer


def plot(config):
    plot_config = config.get('plot').get('config')

    host = plot_config.get('host')
    port = plot_config.get('port')
    pointer = plot_config.get('pointer')
    timeout = plot_config.get('timeout', 1)
    blocking = plot_config.get('blocking', False)
    
    def plotter(state):
        client = None
        try:
            if not client:
                client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
                client.connect((host, port))
                client.settimeout(timeout)
                client.setblocking(blocking)

            data = state['parse']['data']

            if pointer:
                data = resolve_pointer(state, pointer)

            client.send(data)
            client.sendall(b'\n')

        except:
            client.close()
            client = None

    return plotter
