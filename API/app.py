from flask import Flask
from flask_socketio import SocketIO
from flask_cors import CORS
from Login import login_route
from SignUp import signup_route
from ForgotPassword import forgot_password_route
from Controller_File import file_route

app = Flask(__name__)
app.config['SECRET_KEY'] = 'your_secret_key'
CORS(app)
socketio = SocketIO(app, cors_allowed_origins="*")

app.register_blueprint(login_route)
app.register_blueprint(signup_route)
app.register_blueprint(forgot_password_route)
app.register_blueprint(file_route)

if __name__ == "__main__":
    socketio.run(app, debug=True, use_reloader=False, allow_unsafe_werkzeug=True)
