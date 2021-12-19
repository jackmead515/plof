import sys
import time
import socket
import select
from collections import deque

from plof.config import Config


class Pipe:

    def __init__(self, config: Config):
        self.config = config
        if config.pipe:
            self.pipe = StandardPipe(config)
        else:
            self.pipe = NetworkPipe(config)

    def read(self) -> 'list[str]':
        start = time.perf_counter()

        buffered = deque(maxlen=self.config.buffer_size)
        while start + self.config.timeout >= time.perf_counter():
            message = self.pipe.recv()
            if message is not None:
                buffered.append(message)
        
        return list(buffered)


class NetworkPipe:


    def __init__(self, config: Config):
        self.config = config
        self.client = self.create_client()


    def create_client(self):
        return self.create_tcp_client()


    def create_tcp_client(self):
        try:
            client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            client.settimeout(self.config.timeout)
            client.connect((self.config.host, self.config.port))
            return client
        except:
            return None


    def destory_client(self):
        try:
            if self.client is not None:
                self.client.close()
        finally:
            self.client = None

    
    def recv(self):
        if not self.client:
            self.client = self.create_client()
            return None

        buffer = ''
        while True:
            data = None
            try:
                data = self.client.recv(1).decode('utf-8')
            except socket.timeout:
                pass
            if data == self.config.delimiter:
                return buffer
            elif not data:
                self.destory_client()
                return None
            else:
                buffer += data


class StandardPipe:

    def __init__(self, config: Config):
        self.config = config
        self.client = self.create_client()


    def create_client(self):
        return select.select([sys.stdin], [], [], self.config.timeout)[0][0]


    def destory_client(self):
        try:
            if self.client is not None:
                self.client.close()
        finally:
            self.client = None


    def recv(self):
        if not self.client:
            self.client = self.create_client()
            return None

        buffer = ''
        while True:
            data = self.client.read(1)
            if data == self.config.delimiter:
                return buffer
            elif not data:
                self.destory_client()
                return None
            else:
                buffer += data