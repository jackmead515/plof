
import requests
import time
import serial
import re

from util.time import parse_elapsed_time

def initial_serial(pipe_config):
    port = pipe_config.get('port')
    baudrate = pipe_config.get('baudrate')
    stopbits = pipe_config.get('stopbits')
    timeout = pipe_config.get('timeout')
    write_timeout = pipe_config.get('write_timeout')

    return serial.Serial(
        port=port,
        baudrate=baudrate,
        stopbits=stopbits,
        timeout=timeout,
        write_timeout=write_timeout
    )
    

def read_until_ok(serial_connection):
    response = ""
    while True:
        line = serial_connection.readline().decode().strip()
        response += line + "\n"  # Accumulate lines
        if "OK" in line:
            break
    return response


def pipe(config):

    pipe_config = config.get('pipe').get('config')
    poll_time = pipe_config.get('poll_time')

    connection = None
    
    while True:
        
        if connection is None:
            try:
                connection = initial_serial(pipe_config)
            except serial.SerialException:
                time.sleep(1)
                connection = None
                continue

        start_time = time.time()


        connection.write(b'AT+CSQ\r')
        csq_response = read_until_ok(connection)

        csq_matches = re.findall(r'\+CSQ: (\d+),(\d+)', csq_response)
        if csq_matches:
            score, ber = csq_matches[0]
        else:
            print("No CSQ data found.")
            continue
        
        connection.write(b'AT+COPS?\r')
        cops_response = read_until_ok(connection)

        cops_matches = re.findall(r'\+COPS: (\d+),(\d+),"([^"]*)",(\d+)', cops_response)
        if cops_matches:
            mode, format, operator, access_tech = cops_matches[0]
        else:
            print("No COPS data found.")
            continue

        data = [score, ber, mode, format, operator, access_tech]

        yield {
            'pipe': {
                'data': data,
                'elapsed': elapsed,
                'time': start_time
            }
        }
        
        elapsed = time.time() - start_time

        sleep_time = poll_time - elapsed
        if sleep_time > 0:
            time.sleep(sleep_time)

