from flask import Flask, Blueprint
from flask_socketio import SocketIO, emit

from Api_test.switcher import switch_code
from Entity.PasswordsT import Passwords as EntityPasswordsTable
from Entity.User import Users
from Entity.e import getSession
from flask_cors import CORS
from Rsa.encrypt import createKeys
from ViewObject.User import UserViewObject
from sock_io import socketio
log = ["Login Successful",  # 0
       "User does not exist",  # 1
       "One of the details is incorrect",  # 2
       "error"]  # 3

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
                user_view_object.set_is_change_code(user.get_is_change_company_code())
                print("is cjange?", user_view_object.get_is_change_code())
                user_view_object.set_access_key(createKeys(user.get_id()))
                print(user_view_object.get_access_key())
                return log[0] + ":" + user.get_username()

        return log[2]
    except Exception as e:
        print("An error occurred:", str(e))
        return log[3]

user_view_object = UserViewObject('JohnDoe', 123456, 'abc123', '789',False)

@socketio.on('login')
def handle_login(data):
    username = data.get('username')
    password = data.get('password')
    result = check_user_info(username, password)
    emit('login_response', {'message': result, "user_view": user_view_object.to_dict()})


from flask import Flask, request, jsonify
from flask_socketio import SocketIO, emit
import os
import base64
from Stenography.Image.LSBEncode import lsb
from Stenography.Image.LSBDecoded import decode as lsb_d
from Stenography.Audio.LSBEncodedA import encode
from Stenography.Audio.LSBDncodedA import decode
from Rsa.decrypt import decrypt_Text_Rsa

import PIL
from sock_io import socketio

def encode_s(text, file):
    f = lsb(text, file,[50,80])
    print("the msg" + lsb_d(file,[50,80]))


def delete_file(file_path):
    try:
        os.remove(file_path)
        print(f"File '{file_path}' deleted successfully.")
    except Exception as e:
        print(f"Error deleting file: {e}")
def get_file_type(file_path):
    # משיגים את סיומת הקובץ
    file_extension = os.path.splitext(file_path)[1]

    # מסודרים את הסוג של הקובץ לפי הסיומת
    if file_extension == '':
        file_type = 'No extension'
    elif file_extension == '.txt':
        file_type = 'txt'
    elif  file_extension == '.jpeg':
        file_type = 'jpeg'
    elif file_extension == '.jpg':
        file_type = 'jpg'
    elif file_extension == '.png':
        file_type = 'png'
    elif file_extension == '.pdf':
        file_type = 'pdf'
    else:
        file_type = 'Unknown'

    return file_type
@socketio.on('encode')
def upload_file(data):
    file_data = data['file']
    text_value = data['text']
    file_type = data['option']
    print(text_value)
    user_id = data['user_id']
    t_d=decrypt_Text_Rsa(text_value,user_id)
    # Define the filename
    filename = 'uploaded_file'+str(user_id)+'.png'
    print(file_data)
    # Save the file to the desired location
    file_path = os.path.join(r'C:\Users\ariel\PycharmProjects\pythonProject1\image_c', filename)
    with open(file_path, 'wb') as f:
        f.write(file_data)

    # Encode the text into the file
    #encode_s(t_d, file_path)
    x,algorit=switch_code(1, 'PVD', [50,80], file_type, 'encode', t_d,file_path)
    if algorit!='LSB':
        file_path=r'C:\Users\ariel\PycharmProjects\pythonProject1\image_c\modified_image.png'
    # Send the file back to the client
    with open(file_path, 'rb') as file:
        file_data = base64.b64encode(file.read()).decode('utf-8')
        emit('file_download', {'file': file_data})

    # Emit a response back to the client
    emit('upload_response', {'message': 'File uploaded successfully'})

    # Delete the file after processing
    delete_file(file_path)
@socketio.on('decode')
def upload_file_d(data):
    print("-------------------------------------------------------------------------")
    file_data = data['file']
    user_id = data['user_id']
    file_type = data['option']
    # Define the filename
    filename = 'uploaded_file'+str(user_id)+'.png'
    # Save the file to the desired location
    file_path = os.path.join(r'C:\Users\ariel\PycharmProjects\pythonProject1\image_c', filename)
    with open(file_path, 'wb') as f:
        f.write(file_data)

    # Encode the text into the file
    message_d,A = switch_code(1, 'PVD', [50,80], file_type, 'decode','',file_path)
    print(message_d)
    # Emit a response back to the client
    emit('decode_response', {'message': message_d})

    # Delete the file after processing
    delete_file(file_path)

from flask import Flask, request, jsonify, Blueprint
from flask_socketio import SocketIO, emit
from flask_cors import CORS

from Entity.Company import Company
from Entity.User import Users
from Entity.e import getSession
from Entity.PasswordsT import Passwords
from sock_io import socketio

Sign = [
    "Register successfully",  # 0
    "The user already exists in the system",  # 1
    "The email already exists in the system",  # 2
    "INVALID_EMAIL",  # 3
    "WEAK_PASSWORD",  # 4
    "INVALID_COMPANY_ID",  # 5
    "error"  # 6
]



def check_register(_username, _password, _email, _company_id):
    print(_username, _password, _email, _company_id)
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

@socketio.on('signup')
def handle_signup(data):
    username = data.get('username')
    password = data.get('password')
    email = data.get('email')
    company_id = data.get('company')
    result = check_register(username, password, email, company_id)
    emit('signup_response', {'message': result})



