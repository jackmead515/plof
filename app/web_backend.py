
# generate Flask boilerplate
from flask import Flask
from flask_cors import CORS
from flask import Flask, render_template, send_file, jsonify #used as back-end service for Vue2 WebApp
import serial
import time
import csv
import threading #used to run main app within a thread
import requests #used to communicate with Vue2 app
app = Flask(__name__)
cors = CORS(app, resources={r"/api/*": {"origins": "*"}})

import config

config.initialize()

from routes.project import get_project_data
from routes.project import upload_eye_tracking
from routes import upload

app.register_blueprint(upload.mod)
app.register_blueprint(get_project_data.mod)
app.register_blueprint(upload_eye_tracking.mod)

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=4204)



import re
from datetime import datetime
from flask import Flask, render_template, send_file, jsonify #used as back-end service for Vue2 WebApp
import requests #used to communicate with Vue2 app
import threading #used to run main app within a thread
app = Flask(__name__, static_url_path="/static", static_folder="static") #setup flask app





# Configuration variables
serial_port = '/dev/ttyUSB4'
baud_rate = 115200
log_file_path = 'cell_log.csv'
log_execute_every = 30

data = []
def open_log_file(new_file=False):
    mode = 'w' if new_file else 'a'
    return open(log_file_path, mode, newline='')

def read_until_ok(serial_connection):
    response = ""
    while True:
        line = serial_connection.readline().decode().strip()
        response += line + "\n"  # Accumulate lines
        if "OK" in line:
            break
    return response
def main():
    ser = serial.Serial(serial_port, baud_rate)
    ser.reset_input_buffer()  # Clearing input buffer
    ser.reset_output_buffer()  # Clearing output buffer
    time.sleep(2)
    global data

    with open_log_file(True) as csvfile:
        writer = csv.writer(csvfile)
        writer.writerow(['Score', 'RSSI', 'Mode', 'Format', 'Operator', 'Access Technology'])
    print("main started")
    try:
        while True:
            ser.write(b'AT+CSQ\r')
            csq_response = read_until_ok(ser)

            csq_matches = re.findall(r'\+CSQ: (\d+),(\d+)', csq_response)
            if csq_matches:
                score, ber = csq_matches[0]
            else:
                print("No CSQ data found.")
                continue

            ser.write(b'AT+COPS?\r')
            cops_response = read_until_ok(ser)

            cops_matches = re.findall(r'\+COPS: (\d+),(\d+),"([^"]*)",(\d+)', cops_response)
            if cops_matches:
                mode, format, operator, access_tech = cops_matches[0]
            else:
                print("No COPS data found.")
                continue
            data = [score, ber, mode, format, operator, access_tech]
            with open_log_file() as csvfile:
                writer = csv.writer(csvfile)
                writer.writerow(data)
                print("Data logged")
            time.sleep(log_execute_every)


        else:
            print("error")

    except KeyboardInterrupt:
        print("Script interrupted by user. Exiting.")
    finally:
        ser.close()
@app.route('/')
def home():
    return app.send_static_file("index.html")
def get_data():
    return jsonify(data)
@app.route('/download')
def download_file():
    return send_file(log_file, as_attachment=True, cache_timeout=0)

@app.route('/data')
def get_data():
    global data
    return jsonify(data)

if __name__ == '__main__':
    thread = threading.Thread(target=main)
    thread.start()
    app.run(host='0.0.0.0', port=6420)