# from flask import Flask, request, jsonify, Blueprint
# from flask_socketio import SocketIO, emit
# import os
# from Stenography.Image.LSBEncode import lsb
# from Stenography.Image.LSBDecoded import decode
#
# app = Flask(__name__)
# socketio = SocketIO(app, cors_allowed_origins="*")
#
# file_route = Blueprint('file_route', __name__)
#
# def encode(text, file):
#     f = lsb(text, file)
#     print("the msg" + decode(file))
#
# def delete_file(file_path):
#     try:
#         os.remove(file_path)
#         print(f"File '{file_path}' deleted successfully.")
#     except Exception as e:
#         print(f"Error deleting file: {e}")
#
# import base64
# from io import BytesIO
#
# import base64
# from io import BytesIO
# import base64
#
# # פונקציה עבור השליחה של הקובץ ללקוח
# def send_file_to_client(file_path):
#     with open(file_path, 'rb') as file:
#         file_data = base64.b64encode(file.read()).decode('utf-8')
#         socketio.emit('file_download', {'file': file_data})
#
# @socketio.on('upload')
# def upload_file(data):
#     file_data = data['file']
#     text_value = data['text']
#
#     # Define the filename
#     filename = 'uploaded_file.png'
#
#     # Save the file to the desired location
#     file_path = os.path.join(r'C:\Users\ariel\PycharmProjects\pythonProject1\image_c', filename)
#     with open(file_path, 'wb') as f:
#         f.write(file_data)
#
#     # Encode the text into the file
#     encode(text_value, file_path)
#
#     # Emit a response back to the client
#     emit('upload_response', {'message': 'File uploaded successfully'})
#
#     # Delete the file after processing
#     delete_file(file_path)
#
# if __name__ == '__main__':
#     socketio.run(app, debug=True, allow_unsafe_werkzeug=True)
from flask import Flask, request, jsonify
from flask_socketio import SocketIO, emit
import os
import base64
from Stenography.Image.LSBEncode import lsb
from Stenography.Image.LSBDecoded import decode
from Stenography.Audio.LSBEncodedA import encode
from Stenography.Audio.LSBDncodedA import decode
import PIL
app = Flask(__name__)
socketio = SocketIO(app, cors_allowed_origins="*")

def encode(text, file):
    f = lsb(text, file)
    print("the msg" + decode(file))


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

    # Define the filename
    filename = 'uploaded_file.png'

    # Save the file to the desired location
    file_path = os.path.join(r'C:\Users\ariel\PycharmProjects\pythonProject1\image_c', filename)
    with open(file_path, 'wb') as f:
        f.write(file_data)

    # Encode the text into the file
    encode(text_value, file_path)

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

if __name__ == '__main__':
    socketio.run(app, debug=True, allow_unsafe_werkzeug=True)
