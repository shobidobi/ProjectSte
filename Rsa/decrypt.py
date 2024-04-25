import json
import math
from Entity.Keys import get_key_by_user_id
l=[]
def modular_exponentiation(base, exponent, modulus):
    if modulus == 1:
        return 0
    result = 1
    base = base % modulus
    while exponent > 0:
        if exponent % 2 == 1:
            result = (result * base) % modulus
        exponent = exponent // 2
        base = (base * base) % modulus
    return result


def decrypt_Text_Rsa(cyphertext, user_id):
    #p = get_key_by_user_id(user_id)
    p=user_id
    print('decrypt_Text_Rsa')
    decrypted_text = ''.join(chr(modular_exponentiation(i, p[0], p[1])) for i in cyphertext)
    print(decrypted_text)
    return decrypted_text
def decrypt_num_Rsa(cyphertext, user_id):
    p = user_id
    print('decrypt_Text_Rsa')
    decrypted_text = [modular_exponentiation(i, p[0], p[1]) for i in cyphertext]
    print(decrypted_text)
    return decrypted_text

# def decrypt_Text_Rsa(cyphertext, user_id):
#     p = user_id
#     print('decrypt_Text_Rsa')
#     decrypted_text = ''.join(chr(i) for i in cyphertext)
#     print(decrypted_text)
#     return decrypted_text


def decrypt_Text_Rsa_user(cyphertext, user_id):
    p = get_key_by_user_id(user_id)
    #print(ord(cyphertext[0]))
    #print((modular_exponentiation((cyphertext[0]), p[0], p[1])))
    #print(p[0])
    decrypted_text = ''.join(chr(modular_exponentiation(i, p[0], p[1])) for i in cyphertext)
    print(decrypted_text)
    return decrypted_text
def decrypt_with_key(data, key):
    return bytes([char ^ key for char in data])

def read_company_data(_company_number,file_type):
    company_data = []
    print(_company_number,file_type)
    file_path = r"C:\Users\ariel\PycharmProjects\pythonProject1\Api_test\company_data.txt"
    with open(file_path, 'r') as file:
        for line in file:
            # פיצול השורה לפי הפסיק
            parts = line.split(',')
            print(len(parts))
            print(parts)
            # קבלת ערכי החברה והמפתח הפרטי
            company_number = int(parts[0].split(':')[1])
            private_key_str = parts[1].split(':')[1].strip()
            n_str = parts[2].split(':')[1].strip()
            file_type_str=parts[3].split(':')[1].strip()

            # בדיקה אם יש שני מספרים במפתח הפרטי
            if ',' in private_key_str:
                # פיצול המחרוזת לשני מספרים והמרתם למספרים שלמים
                private_key = list(map(int, private_key_str.strip('()').split(',')))
            else:
                # אם יש רק ערך אחד, המרתו למספר שלם
                private_key = [int(private_key_str)]
                n = [int(n_str)]

            if company_number ==_company_number and file_type_str==file_type:
                company_data.append((company_number, private_key, n,file_type_str))
        return company_data.pop()

