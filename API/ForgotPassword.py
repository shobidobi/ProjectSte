from flask import Flask, request, jsonify, Blueprint
from flask_cors import CORS

from Entity.PasswordsT import Passwords
from Entity.User import Users
from Entity.e import getSession
from SendEmail import send_email

app = Flask(__name__)
CORS(app, resources={r"/api/*": {"origins": "http://localhost:3000"}})
forgot_password_route = Blueprint('forgot_password_route', __name__)
Session = getSession()
session = Session()

log = ["Password change successful",  # 0
       "Email does not exist",  # 1
       "error",  # 2
       "User does not exist",  # 3
       'The key exists in the system']  # 4

@forgot_password_route.route('/api/forgotpassword', methods=['POST'])
def forgot_password():
    data = request.json
    newpassword = data.get('newPassword')
    username = data.get('username')
    if newpassword is None:
        return jsonify({'success': False, 'message': 'Missing key in request'})
    if username is None:
        return jsonify({'success': False, 'message': 'Missing username  in request'})

    user = session.query(Users).filter_by(user_name=username).first()
    if user is not None:
        existing_password = session.query(Passwords).filter_by(password=newpassword).first()
        if existing_password is not None and existing_password.get_user_id() == user.get_id():
            return jsonify({'success': True, 'message': log[4]})
        psd = Passwords(user_id=user.get_id(), password=newpassword)
        session.add(psd)
        session.commit()
        return jsonify({'success': True, 'message': log[0]})
    else:
        return jsonify({'success': False, 'message': log[3]})


@app.route('/api/sendemail', methods=['POST'])
def send_mail():
    data = request.json
    email = data.get('email')
    user = session.query(Users).filter_by(email=email).first()
    if user is not None:
        num_code = send_email(email)
        return jsonify({'success': True, 'message': num_code})
    else:
        return jsonify({'success': False, 'message': log[1]})


if __name__ == "__main__":
    app.run(debug=True)
