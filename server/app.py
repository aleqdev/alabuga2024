from flask import Flask, send_from_directory, request
from flask_socketio import SocketIO, emit


app = app = Flask(__name__)
socketio = SocketIO(app, cors_allowed_origins='*')


@app.route('/')
def index():
    return send_from_directory("static/", "index.html")


@socketio.event
def execute(message):
    emit('result', message)


socketio.run(app, allow_unsafe_werkzeug=True)