import random
import json
from Entity.Keys import update_or_create_key
from Entity.e import getSession
import math
def gcd_extended(a, b):
    if a == 0:
        return {'gcd': b, 'x': 0, 'y': 1}

    gcd_info = gcd_extended(b % a, a)
    x = gcd_info['y'] - (b // a) * gcd_info['x']
    y = gcd_info['x']

    return {'gcd': gcd_info['gcd'], 'x': x, 'y': y}


def find_numbers_with_modulo_one(n):
    pairs = []
    for i in range(10, n):
        gcd_info = gcd_extended(i, n)
        if gcd_info['gcd'] == 1:
            inverse = (gcd_info['x'] % n + n) % n

            pairs.append([i, inverse])
            if len(pairs) == 10:
                return pairs[-1]
    return pairs


def is_prime(number):
    if number <= 1:
        return False
    if number <= 3:
        return True

    if number % 2 == 0 or number % 3 == 0:
        return False
    i = 5
    while i * i <= number:
        if number % i == 0 or number % (i + 2) == 0:
            return False
        i += 6
    return True


def generate_prime(_min,_max):
    prime=random.randint(_min, _max)
    while not is_prime(prime):
        prime=random.randint(_min, _max)
    return prime

def mod_inverse(number,mod):
    for d in range(3,mod):
        if (d*number) % mod == 1:
            return d

def get_random_prime_in_range(start, end):
    prime_found = False
    random_prime=0
    while not prime_found:
        random_prime = random.randint(start, end)
        if is_prime(random_prime):
            prime_found = True

    return random_prime

def createKeys(id,Asks,file_type=''):
    print("Generating keys...")
    p= generate_prime(1000, 5000)
    q= generate_prime(1000, 5000)
    while p==q:
        p= generate_prime(1000, 5000)
    n=p*q
    phi = (p-1)*(q-1)
    e=random.randint(5,phi)
    print("Generated")
    while math.gcd(e,phi)!=1:
        e=random.randint(5,phi)
    d=mod_inverse(e,phi)
    print("Generated    d")
    private_key=(d,n)
    print(private_key)
    if Asks=='user':
        update_or_create_key(id,private_key)
    if Asks=='company':
        write_to_file(id,private_key,file_type)
    public_key = (e, n)
    print(public_key)
    return public_key

def encrypt_Text_Rsa(plaintext):
    keys,n = createKeys()
    cypher_text = []
    for i in plaintext:
        cypher_text.append(pow(ord(i), keys[0], n))
    return cypher_text

def encrypt_Json_Rsa(data, key):
    return bytes([char ^ key for char in data])


def json_file_to_binary(json_file_path):
    with open(json_file_path, 'r') as file:
        json_data = json.load(file)  # קריאת הנתונים מהקובץ JSON

    # המרת נתוני JSON למחרוזת בתצורת בינארית
    binary_data = json.dumps(json_data).encode('utf-8')

    return binary_data





def write_to_file(company_number, private_key, file_type):
    with open("company_data.txt", "a") as f:
        f.write(f"Company Number: {company_number}, Private Key: {private_key[0]},n:{private_key[1]},file_type:{file_type}\n")


