from flask import Flask, request, jsonify
from Entity import PasswordsT as EntityPasswords
from Entity.User import Users
from Entity.PasswordsT import Passwords as EntityPasswordsTable
from Entity.e import getSession
from flask_cors import CORS
from enum import Enum


log=["Login Successful",#0
     "User does not exist",#1
     "One of the details is incorrect",#2
     "error"]#3

app = Flask(__name__)
CORS(app)
def check_user_info(username, password):
    try:
        # Create session
        Session = getSession()
        session = Session()

        # Query user by username
        user = session.query(Users).filter_by(user_name=username).first()
        if user is None: return log[1]

        # Check if user exists and if password matches
        if user:
            latest_password = session.query(EntityPasswordsTable).filter_by(user_id=user.get_id()).order_by(EntityPasswordsTable.date_c.desc()).first()
            if latest_password and latest_password.password == password:
                return log[0]

        return log[2]
    except Exception as e:
        print("An error occurred:", str(e))
        return log[3]
@app.route('/upload', methods=['POST'])
def upload_file():
    uploaded_file = request.files['file']
    text_value = request.form['text']
    # השתמש בקובץ ובטקסט כרצונך כאן
    return 'File uploaded successfully'

@app.route('/api/login', methods=['POST'])
def login():
    data = request.get_json()
    username = data.get('username')
    password = data.get('password')

    return jsonify({'success': True, 'message': check_user_info(username, password)})
    # if check_user_info(username, password):
    #     return jsonify({'success': True, 'message': 'User authentication successful!'})
    # else:
    #     return jsonify({'success': False, 'message': 'User authentication failed.'})

if __name__ == "__main__":
    app.run(debug=True)


