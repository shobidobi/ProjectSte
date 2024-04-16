#
# import json
#
# def json_to_bytes(json_file_path):
#     try:
#         # פתיחת הקובץ JSON וקריאת הנתונים
#         with open(json_file_path, 'r') as file:
#             json_data = json.load(file)
#
#         # המרת הנתונים למחרוזת בתצורת JSON
#         json_string = json.dumps(json_data)
#
#         # המרת המחרוזת לבינארי
#         binary_data = json_string.encode('utf-8')
#
#         return binary_data
#     except Exception as e:
#         print("An error occurred:", e)
#         return None
#
# def encrypt_with_key(data, key):
#     return bytes([char ^ key for char in data])
#
# # דוגמה לשימוש בפונקציה:
# json_file_path = "aa.json"
# bytes_data = json_to_bytes(json_file_path)
# print("Bytes data:", bytes_data)
#
# # הצפנת כל בית בבית עם המפתח
# key = 42
# encrypted_data = encrypt_with_key(bytes_data, key)
# print("Encrypted data:", encrypted_data)
#
# def decrypt_with_key(data, key):
#     return bytes([char ^ key for char in data])
#
# # דוגמה לשימוש בפונקציה:
# decrypted_data = decrypt_with_key(encrypted_data, key)
# print("Decrypted data:", decrypted_data.decode('utf-8'))
#
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
def check_user_info(username, password):
    print("---------------------------------------------")
    try:
        # Create session
        Session = getSession()
        session = Session()
        print("---------------------------------------------")
        # Query user by username
        user = session.query(Users).filter_by(user_name=username).first()
        if user is None:
            return log[1]
        print("---------------------------------------------")
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
check_user_info("alon", "565632")