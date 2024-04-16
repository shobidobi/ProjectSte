from flask import Flask, Blueprint
from flask_socketio import SocketIO, emit
from Entity.PasswordsT import Passwords as EntityPasswordsTable
from Entity.User import Users
from Entity.e import getSession
from flask_cors import CORS

log = ["Login Successful",  # 0
       "User does not exist",  # 1
       "One of the details is incorrect",  # 2
       "error"]  # 3

app = Flask(__name__)
socketio = SocketIO(app, cors_allowed_origins="*")
CORS(app)
login_route = Blueprint('login_route', __name__)

def check_user_info(username, password):
    print("---------------------------------------------")
    try:
        # Create session
        Session = getSession()
        session = Session()
        # Query user by username
        user = session.query(Users).filter_by(user_name=username).first()
        if user is None:
            return log[1]
        # Check if user exists and if key matches
        if user:
            latest_password = session.query(EntityPasswordsTable).filter_by(user_id=user.get_id()).order_by(
                EntityPasswordsTable.date_c.desc()).first()
            if latest_password and latest_password.password == password:
                #print(log[0] + ":" + user.get_username())

                return log[0] + ":" + user.get_username()

        return log[2]
    except Exception as e:
        print("An error occurred:", str(e))
        return log[3]


@socketio.on('login')
def handle_login(data):
    username = data.get('username')
    password = data.get('password')
    result = check_user_info(username, password)
    emit('login_response', {'message': result})




if __name__ == "__main__":
    socketio.run(app, debug=True, use_reloader=False, allow_unsafe_werkzeug=True)

