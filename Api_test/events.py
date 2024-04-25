import json
from sqlalchemy.exc import SQLAlchemyError
from Api_test.switcher import switch_code
from Entity.PasswordsT import Passwords as EntityPasswordsTable
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
                user_view_object.set_access_key(createKeys(user.get_id(),'user'))
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
from Rsa.decrypt import decrypt_Text_Rsa, decrypt_Text_Rsa_user
from sock_io import socketio


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
# @socketio.on('encode')
# def upload_file(data):
#     file_data = data['file']
#     text_value = data['text']
#     file_type = data['option']
#     print(text_value)
#     user_id = data['user_id']
#     t_d = decrypt_Text_Rsa(text_value, user_id)
#     # Define the filename
#     filename = 'uploaded_file' + str(user_id) + '.png'
#     #filename = 'uploaded_file' + str(user_id) + '.wav'
#     # if file_type == 'audio':
#     #     file_name ='uploaded_file'+str(user_id)+'.wav'
#     print(file_data)
#     file_path = os.path.join(r'C:\Users\ariel\PycharmProjects\pythonProject1\Audio_c', filename)
#     # Save the file to the desired location
#     if file_type == 'image':
#         file_path = os.path.join(r'C:\Users\ariel\PycharmProjects\pythonProject1\image_c', filename)
#     elif file_type == 'audio':
#         print("---------")
#     with open(file_path, 'wb') as f:
#         f.write(file_data)
#
#     # Encode the text into the file
#     #encode_s(t_d, file_path)
#     x,algorit=switch_code(1, 'LSB', [50,80], 'image', 'encode', t_d,file_path)
#     if algorit!='LSB' and file_type == 'image':
#         file_path=r'C:\Users\ariel\PycharmProjects\pythonProject1\image_c\modified_image.png'
#     # Send the file back to the client
#     with open(file_path, 'rb') as file:
#         file_data = base64.b64encode(file.read()).decode('utf-8')
#         emit('file_download', {'file': file_data})
#
#     # Emit a response back to the client
#     emit('upload_response', {'message': 'File uploaded successfully'})
#
#     # Delete the file after processing
#     delete_file(file_path)


@socketio.on('encode')
def upload_file(data):
    print("Uploading file...")
    print("Received data:", data)
    file_data = data['file'] # קבלת הנתונים בפורמט Uint8Array
    text_value = data['text']
    file_type = data['option']
    user_id = data['user_id']
    t_d = decrypt_Text_Rsa_user(text_value, user_id)

    # המרת הנתונים ל-Bytes
    file_bytes = bytes(file_data)

    # Define the filename
    if file_type == 'audio':
        filename = f'uploaded_file{user_id}.wav'
        file_path = os.path.join(r'C:\Users\ariel\PycharmProjects\pythonProject1\Audio_c', filename)
    elif file_type == 'image':
        filename = f'uploaded_file{user_id}.png'
        file_path = os.path.join(r'C:\Users\ariel\PycharmProjects\pythonProject1\image_c', filename)
    else:
        emit('upload_response', {'message': 'Unsupported file type'})
        return

    with open(file_path, 'wb') as f:
        f.write(file_bytes)

    # Encode the text into the file
    #x, algorithm = switch_code(1, 'LSB', [50, 80], file_type, 'encode', t_d, file_path)
    x, algorithm=decrypt_code(1, 'encode', file_path, t_d,file_type)
    if algorithm != 'LSB' and file_type == 'image':
        file_path = r'C:\Users\ariel\PycharmProjects\pythonProject1\image_c\modified_image.png'
    if file_type=='audio':
        file_path = r'C:\Users\ariel\PycharmProjects\pythonProject1\Audio_c\sampleStego.wav'
    # Send the file back to the client
    with open(file_path, 'rb') as file:
        file_data = base64.b64encode(file.read()).decode('utf-8')
        emit('file_download', {'file': file_data}, binary=True)

    # Emit a response back to the client
    emit('upload_response', {'message': 'File uploaded successfully'})

    # Delete the file after processing
    delete_file(file_path)

import os
import base64

@socketio.on('encode_audio')
def upload_file(data):
    print("מעלה קובץ...")
    print("מקבל נתונים:", data)

    # בדיקה אם סוג הקובץ הוא WAV
    file_type = data.get('option')
    if file_type != 'audio':
        print('סוג קובץ לא נתמך')
        emit('upload_response', {'message': 'סוג קובץ לא נתמך'})
        return

    file_data = data.get('file')  # נניח שזה מערך Uint8Array
    text_value = data.get('text')
    user_id = data.get('user_id')
    t_d = decrypt_Text_Rsa_user(text_value, user_id)

    # המרת הנתונים לבתים
    file_bytes = bytes(file_data)

    # הגדרת שם הקובץ והנתיב
    filename = f'uploaded_file{user_id}.wav'
    file_path = os.path.join(r'C:\Users\ariel\PycharmProjects\pythonProject1\Audio_c', filename)

    with open(file_path, 'wb') as f:
        f.write(file_bytes)
    print(f"קובץ נשמר ב: {file_path}")

    # הצפנת הטקסט לקובץ
    print("התחלת הצפנת הטקסט לקובץ")
    try:
        #x, algorithm = switch_code(1, 'MSB', [50, 80], 'audio', 'encode', t_d, file_path)
        x, algorithm = decrypt_code(1, 'encode', file_path, t_d,file_type)
        print(f"השיטה הנבחרת להצפנה: {algorithm}")

        file_path = r'C:\Users\ariel\PycharmProjects\pythonProject1\Audio_c\sampleStego.wav'

        # שליחת הקובץ חזרה ללקוח
        with open(file_path, 'rb') as file:
            file_data = base64.b64encode(file.read()).decode('utf-8')
            emit('file_download', {'file': file_data}, binary=True)
            print("שליחת הקובץ חזרה ללקוח")

        # שליחת תגובה ללקוח
        emit('upload_response', {'message': 'קובץ הועלה בהצלחה'})
        print("תגובה נשלחה ללקוח")

        # מחיקת הקובץ לאחר העיבוד
        delete_file(file_path)
    except Exception as e:
        print(f"שגיאה בעיבוד הקובץ: {e}")


@socketio.on('decode')
def upload_file_d(data):
    print("-------------------------------------------------------------------------")
    file_data = data['file']
    user_id = data['user_id']
    file_type = data['option']
    # Define the filename
    if file_type == 'audio':
        filename = 'uploaded_file'+str(user_id)+'.wav'
    if file_type == 'image':
        filename = 'uploaded_file' + str(user_id) + '.png'
    # Save the file to the desired location
    if file_type=='image':
        file_path = os.path.join(r'C:\Users\ariel\PycharmProjects\pythonProject1\image_c', filename)
    elif file_type=='audio':
        file_path = os.path.join(r'C:\Users\ariel\PycharmProjects\pythonProject1\Audio_c', filename)
    with open(file_path, 'wb') as f:
        f.write(file_data)

    # Encode the text into the file
    #message_d,A = switch_code(1, 'MSB', [50,80], file_type, 'decode','',file_path)
    message_d, A = decrypt_code(1,'decode',file_path,'',file_type)
    print(message_d)
    # Emit a response back to the client
    emit('decode_response', {'message': message_d})

    # Delete the file after processing
    delete_file(file_path)



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


@socketio.on('get_key_company')
def get_key_company(data):
    company_id = data.get('company')
    file_type = data.get('file_type')
    p=createKeys(company_id,'company',file_type)
    emit('response', {'key':p})
@socketio.on('create_code')
def handle_create_code(data):
    print('Received data from client:', data)
    company_number = data.get('company')
    # algorithm_type = data.get('algorithmType')
    # pixel_range = data.get('pixelRange')
    file_type = data.get('file_type')
    print(company_number)
    print(file_type)
    Session = getSession()
    session = Session()

    try:
        company = session.query(Company).filter_by(id=company_number).first()
        if company is None:
            print(f'Error: Company with ID {company_number} not found')
            emit('response_code', {'message': f'Company with ID {company_number} not found'}, broadcast=True)
            return
        print("Company with ID ", company)

        # Convert algorithm type to bytes
        # code_bytes = json.dumps(algorithm_type,pixel_range).encode('utf-8')
        code_bytes = json.dumps(data.get('encryptedData')).encode('utf-8')
        print(code_bytes)
        if file_type == 'image':
            company.code_image = code_bytes
        elif file_type == 'audio':
            company.code_audio = code_bytes
        session.commit()
        emit('response_code', {'message': 'Data has been received and processed successfully'}, broadcast=True)
    except Exception as e:
        print(f'Error: {str(e)}')
        emit('response_code', {'message': f'Error: {str(e)}'}, broadcast=True)

# Function to insert JSON data into the Company table
def insert_company_from_json(json_data):
    try:
        company_name = json_data.get('company_name')
        code = json_data.get('code')
        Session = getSession()
        session = Session()
        # Convert code to bytes
        code_bytes = json.dumps(code).encode('utf-8')

        # Create a new company instance
        new_company = Company(company_name=company_name, code=code_bytes)

        # Add and commit the new company to the database
        session.add(new_company)
        session.commit()

        return {'message': 'Company inserted successfully'}
    except SQLAlchemyError as e:
        return {'message': f'Error: {str(e)}'}

from Rsa.decrypt import read_company_data
from Rsa.decrypt import decrypt_Text_Rsa, decrypt_num_Rsa

def decrypt_code(company_id,mode,path,text,file_type):
    Session = getSession()
    session = Session()

    try:
        company = session.query(Company).filter_by(id=company_id).first()
        if company is None:
            print(f'Error: Company with ID {company_id} not found')
            return
        code=''
        print("Company with ID ", company)
        if file_type =='image':
            code = company.get_code_image()
        elif file_type =='audio':
            code = company.get_code_audio()
        print(code)

        # פענוח המחרוזת כ JSON
        decoded_data = json.loads(code.decode("utf-8"))

        # חילוץ ושמירת הערכים במשתנים
        company_number = decoded_data["companyNumber"]
        algorithm_type_encrypted = decoded_data["algorithmTypeEncrypted"]
        pixel_range = decoded_data["pixelRange"]
        file_type = decoded_data["fileType"]
        print(algorithm_type_encrypted)
        print(pixel_range)
        key = read_company_data(1,file_type)
        print(key)
        algorithm_type_encrypted = decrypt_Text_Rsa(algorithm_type_encrypted,[key[1][0],key[2][0]])
        print(algorithm_type_encrypted)
        print(pixel_range)
        pixel_range = decrypt_num_Rsa(pixel_range, [key[1][0],key[2][0]])
        print(pixel_range)
        return switch_code(company_id, algorithm_type_encrypted, pixel_range, file_type,mode,text,path)
    except Exception as e:
        print(f'Error: {str(e)}')
