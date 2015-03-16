from flask import Flask
from flask.ext.mongoengine import MongoEngine
from flask.ext.socketio import SocketIO

from gevent import monkey
monkey.patch_all()

app = Flask(__name__)
app.debug = True
app.reload = True
app.config['MONGODB_SETTINGS'] = {'DB': 'EMA'}
app.config['WTF_CSRF_ENABLED'] = True
app.config['SECRET_KEY'] = 'you-will-never-guess'

socketio = SocketIO(app)
db = MongoEngine(app)

from webapp import views
