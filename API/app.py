# app.py

from flask import Flask
from flask_cors import CORS
from flask_socketio import SocketIO

from API.Login import socket_blueprint
from Controller_File import upload_blueprint
from SignUp import register_blueprint

app = Flask(__name__)
app.register_blueprint(socket_blueprint, url_prefix='/Login')
app.register_blueprint(upload_blueprint, url_prefix='/upload')
app.register_blueprint(register_blueprint, url_prefix='/register')

socketio = SocketIO(app, cors_allowed_origins="*")
CORS(app)

if __name__ == "__main__":
    socketio.run(app, debug=True, use_reloader=False, allow_unsafe_werkzeug=True)
