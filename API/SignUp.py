from flask import Flask, request, jsonify, Blueprint
from flask_cors import CORS

from Entity.Company import Company
from Entity.User import Users
from Entity.e import getSession
from Entity.PasswordsT import Passwords
from Entity import TryLogin

Sign = [
    "Register successfully",  # 0
    "The user already exists in the system",  # 1
    "The email already exists in the system",  # 2
    "INVALID_EMAIL",  # 3
    "WEAK_PASSWORD",  # 4
    "INVALID_COMPANY_ID",  # 5
    "error"  # 6
]

app = Flask(__name__)
CORS(app)
signup_route = Blueprint('signup_route', __name__)


def check_register(_username, _password, _email, _company_id):
    try:
        # Create session
        Session = getSession()
        session = Session()

        if len(_password) < 6:
            return Sign[4]

        company_id = session.query(Company).filter_by(id=_company_id).first()
        print(_company_id)
        if company_id is None:
            return Sign[5]

        # Query user by username
        user = session.query(Users).filter_by(user_name=_username).first()
        if user:
            return Sign[1]

        email = session.query(Users).filter_by(email=_email).first()
        if email:
            return Sign[2]

        # יצירת המשתמש
        new_user = Users(user_name=_username, email=_email, id_company=_company_id)
        session.add(new_user)
        session.commit()

        user_s = session.query(Users).filter_by(user_name=_username).first()
        if user_s:
            psd = Passwords(user_id=user_s.get_id(), password=_password)
            session.add(psd)
            session.commit()

        latest_password = session.query(Passwords).filter_by(user_id=user_s.get_id()).order_by(
            Passwords.date_c.desc()).first()
        if user_s and latest_password:
            return Sign[0]

    except Exception as e:
        print("An error occurred:", str(e))
        return Sign[6]


@signup_route.route('/api/signup', methods=['POST'])
def signup():
    data = request.get_json()
    username = data.get('username')
    password = data.get('key')
    email = data.get('email')
    company_id = data.get('company')
    print(company_id)
    return jsonify({'success': True, 'message': check_register(username, password, email, company_id)})


if __name__ == "__main__":
    app.run(debug=True)
