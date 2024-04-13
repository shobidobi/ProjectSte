import json
import base64


def json_to_base64(file_path):
    try:
        # קריאת נתוני הקובץ
        with open(file_path, 'rb') as file:
            data = file.read()

        # המרת הנתונים לבינארי Base64
        base64_data = base64.b64encode(data)

        return base64_data
    except Exception as e:
        print(f"An error occurred: {e}")
        return b''
#
# # דוגמה לשימוש:
# json_data = [
#     {
#         "companyNumber": 1,
#         "algorithmType": "LSB",
#         "pixelRange": [100, 200],
#         "fileType": "image"
#     },
#     {
#         "companyNumber": 2,
#         "algorithmType": "MSB",
#         "pixelRange": [50, 150],
#         "fileType": "text"
#     }
# ]
#

def base64_to_json(base64_data):
    try:
        json_bytes = base64.b64decode(base64_data)
        json_str = json_bytes.decode('utf-8')
        return json.loads(json_str)
    except Exception as e:
        print(f"An error occurred: {e}")
        return []

# # דוגמה לשימוש:
# base64_data = b'W3siY29tcGFueU51bWJlciI6IDEsICJhbGdvcml0aG1UeXBlIjogIkxTQiIsICJwaXhlbFJhbmdlIjogWzEwMCwgMjAwXSwgImZpbGVUeXBlIjogImltYWdlIn0sIHsiY29tcGFueU51bWJlciI6IDIsICJhbGdvcml0aG1UeXBlIjogIk1TQiIsICJwaXhlbFJhbmdlIjogWzUwLCAxNTBdLCAiZmlsZVR5cGUiOiAidGV4dCJ9XQ=='
# json_data = base64_to_json(base64_data)
# print(json_data)


def encrypt_Json_Rsa(json_file_path, public_key, n):
    # קריאת נתוני הקובץ JSON

    # הצפנת הנתונים בקובץ JSON
    encrypted_data = []
    for key, value in json_file_path.items():
        if isinstance(value, str):  # השוואה בין סוגי הנתונים
            encrypted_value = [pow(ord(char), public_key, n) for char in value]
            encrypted_data.append({key: encrypted_value})
        else:
            encrypted_data.append({key: value})  # נתון לא מסוג מחרוזת, אין להצפין

    # שמירת הנתונים המוצפנים בקובץ חדש
    encrypted_json_file_path = f'encrypted_{json_file_path["companyNumber"]}.json'


    with open(encrypted_json_file_path, 'w') as f:
        json.dump(encrypted_data, f)

# דוגמה לשימוש:
# נניח שיש לנו קובץ JSON בשם 'data.json'
# וקבועי RSA ציבוריים
# קריאת נתוני הקובץ JSON והמרתם לבינארי Base64
base64_data = json_to_base64("aa.json")

# פענוח הנתונים מבינארי Base64 למבנה JSON
json_data = base64_to_json(base64_data)

# הצפנת הנתונים בקובץ JSON
public_key = 65537
n = 123456789
encrypt_Json_Rsa(json_data, public_key, n)
def decrypt_Json_Rsa(encrypted_json_file_path, private_key, n):
    try:
        # קריאת הנתונים המוצפנים מהקובץ
        with open(encrypted_json_file_path, 'r') as f:
            encrypted_data = json.load(f)

        # פענוח הנתונים מהוצפנים
        decrypted_data = {}
        for item in encrypted_data:
            for key, value in item.items():
                if isinstance(value, list):  # בדיקה האם הערך מוצפן
                    decrypted_value = ''.join([chr(pow(char, private_key, n) % 1114111) for char in value])
                    decrypted_data[key] = decrypted_value
                else:
                    decrypted_data[key] = value

        return decrypted_data
    except Exception as e:
        print(f"An error occurred: {e}")
        return {}

# דוגמה לשימוש:
# נניח שיש לנו קובץ JSON מוצפן בשם 'encrypted_data.json'
# וקבועי RSA פרטיים
private_key = 123456789
n = 987654321
decrypted_data = decrypt_Json_Rsa('encrypted_1.json', private_key, n)
print(decrypted_data)
