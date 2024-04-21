

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
    f = lsb(text, file)
    print("the msg" + lsb_d(file))


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
    print(text_value)
    user_id = data['user_id']
    t_d=decrypt_Text_Rsa(text_value,user_id)
    # Define the filename
    filename = 'uploaded_file.png'

    # Save the file to the desired location
    file_path = os.path.join(r'C:\Users\ariel\PycharmProjects\pythonProject1\image_c', filename)
    with open(file_path, 'wb') as f:
        f.write(file_data)

    # Encode the text into the file
    encode_s(t_d, file_path)

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

    # Define the filename
    filename = 'uploaded_file.png'
    # Save the file to the desired location
    file_path = os.path.join(r'C:\Users\ariel\PycharmProjects\pythonProject1\image_c', filename)
    with open(file_path, 'wb') as f:
        f.write(file_data)

    # Encode the text into the file
    message_d=decode(file_path)
    # Emit a response back to the client
    emit('decode_response', {'message': message_d})

    # Delete the file after processing
    delete_file(file_path)
