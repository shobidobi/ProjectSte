from flask import Flask, request, make_response
from flask_cors import CORS
import os
import time
from Stenography.Image.LSBEncode import lsb
from Stenography.Image.LSBDecoded import decode
app = Flask(__name__)
CORS(app)
def encode(text,file):

    f=lsb(text,file)
    print("the msg"+decode(file))
def delete_file(file_path):
    try:
        os.remove(file_path)
        print(f"File '{file_path}' deleted successfully.")
    except Exception as e:
        print(f"Error deleting file: {e}")

@app.route('/upload', methods=['POST'])
def upload_file():
    uploaded_file = request.files['file']
    file_path = os.path.join(r'C:\Users\ariel\PycharmProjects\pythonProject1\image_c', uploaded_file.filename)
    new_path = file_path.replace("class ", "")
    uploaded_file.save(new_path)
    text_value = request.form['text']
    #print(text_value)
    print(text_value)
    print(new_path)
    encode(text_value,new_path)

    # מחיקת הקובץ
    print(uploaded_file.filename)
    text_value = request.form['text']
    print(text_value)
    # השתמש בקובץ ובטקסט כרצונך כאן
    response = make_response('File uploaded successfully')
    response.headers['Access-Control-Allow-Origin'] = '*'
    response.headers['Access-Control-Allow-Headers'] = 'Content-Type'
    response.headers['Access-Control-Allow-Methods'] = 'POST'
    delete_file(new_path)
    return response

if __name__ == '__main__':
    app.run(debug=True)
