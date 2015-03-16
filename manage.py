import os, sys
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from flask.ext.script import Manager
from webapp import app, socketio

manager = Manager(app)


@manager.command
def runserver():
    socketio.run(app)

if __name__ == "__main__":
    manager.run()
