import json
import math
l=[]
def decrypt_Text_Rsa(cyphertext,key,n):
    for i in cyphertext:
        l.append(chr(pow(i,key,n)))
    return l

def decrypt_with_key(data, key):
    return bytes([char ^ key for char in data])




