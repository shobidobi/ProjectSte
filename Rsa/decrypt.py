import json
import math
l=[]
def decrypt_Text_Rsa(cyphertext,key,n):
    for i in cyphertext:
        l.append(chr(pow(i,key,n)))
    return l



import json
def decrypt_Json_Rsa(encrypted_json_file_path, private_key, n):
    # קריאת הנתונים המוצפנים מהקובץ
    with open(encrypted_json_file_path, 'r') as f:
        encrypted_data = json.load(f)

    # פענוח הנתונים מהצפנה RSA
    decrypted_data = {}
    for item in encrypted_data:
        for key, value in item.items():
            if isinstance(value, list):  # בדיקה אם הערך הוא רשימה של מספרים
                decrypted_value = ''.join([chr(pow(char, private_key[1], n)) for char in value])
                decrypted_data[key] = decrypted_value
            else:
                decrypted_data[key] = value

    return decrypted_data




