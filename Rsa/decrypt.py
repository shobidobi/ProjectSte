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
    p = get_key_by_user_id(user_id)
    #print(ord(cyphertext[0]))
    #print((modular_exponentiation((cyphertext[0]), p[0], p[1])))
    #print(p[0])
    decrypted_text = ''.join(chr(modular_exponentiation(i, p[0], p[1])) for i in cyphertext)
    print(decrypted_text)
    return decrypted_text


def decrypt_with_key(data, key):
    return bytes([char ^ key for char in data])



