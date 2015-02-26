from __future__ import print_function, division, unicode_literals

from gevent import monkey
monkey.patch_all()

import time
import random
import serial
from threading import Thread
from flask import Flask, render_template
from flask.ext.socketio import SocketIO, emit

app = Flask(__name__)
app.debug = True
app.config['SECRET_KEY'] = 'secret!'
socketio = SocketIO(app)
thread = None

class ArduinoMock():

    def readline(self):
        return ','.join(str(random.random() * 10) for _ in range(3))


class Arduino():
    def __init__(slef, fd, baudios):
        self.connection = serial.Serial(fd, baudios)

    def readline(self):
        return self.connection.readline()



def background_thread():
    serial = ArduinoMock()

    while True:
        data = serial.readline().strip()
        
        tm = time.time()
        if (data and data != 'fail'):
            data = data.split(',')
            print(data)
            socketio.emit('EMA data',
                        {'time': tm, 'temperatura': data[0], 'humedad': data[1],
                            'presion': data[2]}, namespace='/test')
        time.sleep(2)


@app.route('/')
def index():
    global thread
    if thread is None:
        thread = Thread(target=background_thread)
        thread.start()
    return render_template('index.html')


@socketio.on('connect', namespace='/test')
def test_connect():
    print('Client connect')


@socketio.on('disconnect', namespace='/test')
def test_disconnect():
    print('Client disconnected')


if __name__ == '__main__':
    socketio.run(app)

