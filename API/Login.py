from flask import Flask, Blueprint
from flask_socketio import SocketIO, emit
from Entity.PasswordsT import Passwords as EntityPasswordsTable
from Entity.User import Users
from Entity.e import getSession
from flask_cors import CORS
from Rsa.encrypt import createKeys
from ViewObject.User import UserViewObject

log = ["Login Successful",  # 0
       "User does not exist",  # 1
       "One of the details is incorrect",  # 2
       "error"]  # 3

app = Flask(__name__)
socketio = SocketIO(app, cors_allowed_origins="*")
CORS(app)
login_route = Blueprint('login_route', __name__)
def calculate_hash(text):
    hash_value = ''
    for char in text:
        # חישוב ה-ASCII code של התו וכפלו ב-5
        ascii_code = ord(char) * 5
        hash_value += str(ascii_code)
    return hash_value
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
            if latest_password and calculate_hash(latest_password.password) == password:
                #print(log[0] + ":" + user.get_username())
                print("Logged in successfully")
                user_view_object.set_user_id(user.get_id())
                user_view_object.set_username(user.get_username())
                print(user.get_id_company())
                user_view_object.set_company_number(user.get_id_company())

                user_view_object.set_access_key(createKeys(user.get_id()))
                print(user_view_object.get_access_key())
                return log[0] + ":" + user.get_username()

        return log[2]
    except Exception as e:
        print("An error occurred:", str(e))
        return log[3]

user_view_object = UserViewObject('JohnDoe', 123456, 'abc123', '789')

@socketio.on('login')
def handle_login(data):
    username = data.get('username')
    password = data.get('password')
    result = check_user_info(username, password)
    emit('login_response', {'message': result,"user_view":user_view_object.toJSON()})



if __name__ == "__main__":
    socketio.run(app, debug=True, use_reloader=False, allow_unsafe_werkzeug=True)

