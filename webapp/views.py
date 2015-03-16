from __future__ import print_function, division, unicode_literals


from datetime import datetime
import time
import random
import serial
from threading import Thread

from webapp import app, db, socketio
from flask import render_template, redirect, url_for, json
from models import DataType, Data
from forms import HistoricoForm

from consumer import *
from socket_wrapp import Socket
from protocol import * #usar pyClients


thread = None
cons=Consumidor(Socket())

class ArduinoMock():

    def readline(self):
        return ','.join(str(random.random() * 10) for _ in range(3))


class Arduino():
    def __init__(self, fd, baudios):
        self.connection = serial.Serial(fd, baudios)

    def readline(self):
        return self.connection.readline()


def background_thread():
    serial = ArduinoMock()
    #serial = Arduino('/dev/ttyACM0', 9600)
    temp = DataType.get_or_create('Temperatura', 'float')
    hume = DataType.get_or_create('Humedad', 'int')
    pre = DataType.get_or_create('Presion', 'int')

    while True:
        data = serial.readline().strip()
        tm = datetime.now()
        if (data and data != 'fail'):
            data = data.split(',')
            captura = {'time': tm, 'temperatura': data[0], 'humedad': data[1],
                            'presion': data[2]}
            socketio.emit('EMA data', captura, namespace='/test')

            temp.data.append(Data(timestamp=tm, value=data[0]))
            hume.data.append(Data(timestamp=tm, value=data[1]))
            pre.data.append(Data(timestamp=tm, value=data[2]))
            temp.save()
            hume.save()
            pre.save()

        time.sleep(2)


@app.route('/')
def index():
    return render_template('index.html')


@app.route('/realtime')
def realtime():
    global thread
    if thread is None:
        thread = Thread(target=background_thread)
        thread.start()
    return render_template('realtime.html')


@app.route('/historico', methods=['GET', 'POST'])
def historico():
    form = HistoricoForm()
    if form.validate_on_submit():
        url = url_for('historico_consulta', tm_inicio=str(form.tm_inicio.data),
                tm_fin=str(form.tm_fin.data))
        return redirect(url)
    return render_template('historico_consulta.html', form=form)


@app.route('/historico/<float:tm_inicio>/<float:tm_fin>')
def historico_consulta(tm_inicio, tm_fin):
    tm_inicio = datetime.utcfromtimestamp(tm_inicio)
    tm_fin = datetime.utcfromtimestamp(tm_fin)

    temp = DataType.query_interval('Temperatura', tm_inicio, tm_fin)
    pre = DataType.query_interval('Presion', tm_inicio, tm_fin)
    hume = DataType.query_interval('Humedad', tm_inicio, tm_fin)

 
    return render_template('historico.html', temp=temp, hume=hume, pre=pre)

@app.route('/fuentesds')
def fuentesDS():
    
   # cons = Consumidor(Socket()): EN APP
    cons.connect_server("127.0.0.1",8888)
    sources2=[]  
    sources = [" ".join(data.split(',')) for data in cons.request_sources()]
    
    return render_template('fuentesds.html',fuentes=sources,cantidad=len(sources))

@app.route('/fuentesds/<idFuente>')
def fuentesds_id(idFuente):
    print(idFuente)
    datos=[] 
    i=0
     
    if (cons.select_source(idFuente)):
        for dato in cons.start_stream(GET_OP_NORMAL,1):
            i=i+1
            dato=dato.split(';')            
            datos.append(("{x:"+dato[0]+",y:"+dato[1]+"}").strip("'"))
            
        datos=str(datos) 
        print(datos)                        
        return render_template('rtds.html',id =idFuente,datos=datos)
    else:
        return ("FUENTE INEXISTENTE") #Crear Pagina de ERROR


@socketio.on('connect', namespace='/test')
def test_connect():
    print('Client connect')


@socketio.on('disconnect', namespace='/test')
def test_disconnect():
    print('Client disconnected')

