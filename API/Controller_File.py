from flask import Flask, request, make_response
from flask_cors import CORS
import os
import time
from Stenography.Image.LSBEncode import encode_lsb
from Stenography.Image.LSBDecoded import decode_lsb
app = Flask(__name__)
CORS(app)
def encode(file,text):

    f=encode_lsb(file,text)
    print(decode_lsb(file))
def image_to_binary(img):
    binary_image = []
    width, height = img.size
    pixels = img.load()
    for y in range(height):
        for x in range(width):
            pixel = pixels[x, y]
            binary_pixel = format(pixel, '08b')  # המרת הערך של הפיקסל לבינארי בעומק 8 ביט
            binary_image.append(binary_pixel)
    return binary_image
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
    encode(new_path, text_value)

    # המתנה לזמן מוגבל
    # time.sleep(10000000)  # לדוגמה, ממתין עשר דקות (3600 שניות)

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
    imgs = Image.open(r'C:\Users\ariel\PycharmProjects\pythonProject1\redD.png')
    app.run(debug=True)
