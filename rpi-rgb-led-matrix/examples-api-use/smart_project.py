import time
from flask import Flask, Response, jsonify
from flask_cors import CORS, cross_origin
import Adafruit_DHT
import threading
import os
import sys
import subprocess
import signal
import psutil
import getpass

import RPi.GPIO as gpio

import time

    
gpio.setmode(gpio.BCM)    
sensor = Adafruit_DHT.DHT11
gpio_pin = 25

# flaks web server

app = Flask(__name__)
CORS(app, resources={r'*':{'origins':'*'}})
app.config['CORS_HEADERS'] = 'content-Type'

humidity = 0
temperature = 0
status = 0

@app.route('/data')
@cross_origin()
def getSensorData():
    global humidity, temperature
    
    data = {
            "sensor1" : temperature,
            "sensor2" : humidity,
            }


    return jsonify(data) 
def getSensorData(): end


def kill(proc_pid):
    process = psutil.Process(proc_pid)
    for proc in process.children(recursive=True):
        proc.kill()
    process.kill()

    
@app.route('/led-on')
def ledOn():
    global proc
    #global pid
    #global status
    
    #if status == 1:
    #    return "okok"
    
    print("on")

    proc = subprocess.Popen(["./demo --led-rows=16 --led-cols=32 --led-no-hardware-pulse -D 1 output-onlinepngtools-_1_.ppm --led-slowdown-gpio=4"], shell=True)
    #time.sleep(3)
#     proc = subprocess.Popen(["./echo"], shell=True)
    
    return "ok"

@app.route('/led-off')
def ledOff():
    time.sleep(3)
    global proc
    #global pid
    #global status
    #status = 0
    
    #pgrp = os.getpgid(proc.pid)
    #os.killpg(pgrp, signal.SIGKILL)
    #proc = subprocess.Popen(["python3 smart_project.py"], shell=True)
    
    kill(proc.pid)
    print("hello")
    print("second")
    print("third")
    
    return "ok"
    
    #def ledOff(): end

def sensorRead():
    global humidity, temperature

    try:
        while True:
            humidity, temperature = Adafruit_DHT.read_retry(sensor, gpio_pin)
            if humidity is None or temperature is None:
                humidity = 0
                temperature = 0
            time.sleep(1)    
    except Exception:
        print("sensorRead error")

    finally:
        print("End of sensorRead")

if __name__ == "__main__":
    t = threading.Thread(target=sensorRead)
    t.daemon = True
    try:
        t.start()
        print("[INFO] sub Thread: sensorRead run")
    except Exception as error:
        print(error)
    app.run(host="0.0.0.0", threaded=True)
