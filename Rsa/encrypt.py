import random
import json
from Entity.Keys import update_or_create_key
from Entity.e import getSession
import math

def gcd_extended(a, b):
    """
    Extended Euclidean Algorithm to find the gcd and the coefficients x, y such that ax + by = gcd(a, b).

    :param a: The first number.
    :param b: The second number.
    :return: A dictionary containing the gcd, x, and y.
    """
    if a == 0:
        return {'gcd': b, 'x': 0, 'y': 1}

    gcd_info = gcd_extended(b % a, a)
    x = gcd_info['y'] - (b // a) * gcd_info['x']
    y = gcd_info['x']

    return {'gcd': gcd_info['gcd'], 'x': x, 'y': y}

def find_numbers_with_modulo_one(n):
    """
    Find pairs of numbers less than n that are coprime with n.

    :param n: The number.
    :return: A list of pairs of coprime numbers.
    """
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
    """
    Check if a number is prime.

    :param number: The number to check.
    :return: True if the number is prime, False otherwise.
    """
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

def generate_prime(_min, _max):
    """
    Generate a random prime number within the given range.

    :param _min: The minimum value for the prime number.
    :param _max: The maximum value for the prime number.
    :return: A prime number within the given range.
    """
    prime = random.randint(_min, _max)
    while not is_prime(prime):
        prime = random.randint(_min, _max)
    return prime

def mod_inverse(number, mod):
    """
    Calculate the modular inverse of a number.

    :param number: The number.
    :param mod: The modulus.
    :return: The modular inverse.
    """
    for d in range(3, mod):
        if (d * number) % mod == 1:
            return d

def get_random_prime_in_range(start, end):
    """
    Get a random prime number within the given range.

    :param start: The start of the range.
    :param end: The end of the range.
    :return: A random prime number within the range.
    """
    prime_found = False
    random_prime = 0
    while not prime_found:
        random_prime = random.randint(start, end)
        if is_prime(random_prime):
            prime_found = True
    return random_prime

def createKeys(id, Asks, file_type=''):
    """
    Create RSA public and private keys.

    :param id: The identifier.
    :param Asks: The type of key to generate (user or company).
    :param file_type: The type of file (optional, for company keys).
    :return: The public key.
    """
    print("Generating keys...")
    p = generate_prime(1000, 5000)
    q = generate_prime(1000, 5000)
    while p == q:
        p = generate_prime(1000, 5000)
    n = p * q
    phi = (p - 1) * (q - 1)
    e = random.randint(5, phi)
    print("Generated")
    while math.gcd(e, phi) != 1:
        e = random.randint(5, phi)
    d = mod_inverse(e, phi)
    print("Generated    d")
    private_key = (d, n)
    print(private_key)
    if Asks == 'user':
        update_or_create_key(id, private_key)
    if Asks == 'company':
        write_to_file(id, private_key, file_type)
    public_key = (e, n)
    print(public_key)
    return public_key

def encrypt_Text_Rsa(plaintext):
    """
    Encrypt plaintext using RSA encryption.

    :param plaintext: The plaintext to encrypt.
    :return: The ciphertext.
    """
    keys, n = createKeys()
    cypher_text = []
    for i in plaintext:
        cypher_text.append(pow(ord(i), keys[0], n))
    return cypher_text

def encrypt_Json_Rsa(data, key):
    """
    Encrypt JSON data using RSA encryption.

    :param data: The JSON data to encrypt.
    :param key: The RSA key.
    :return: The encrypted data.
    """
    return bytes([char ^ key for char in data])

def json_file_to_binary(json_file_path):
    """
    Convert JSON file to binary format.

    :param json_file_path: The path to the JSON file.
    :return: The binary data.
    """
    with open(json_file_path, 'r') as file:
        json_data = json.load(file)
    binary_data = json.dumps(json_data).encode('utf-8')
    return binary_data

def write_to_file(company_number, private_key, file_type):
    """
    Write company data to a file.

    :param company_number: The company number.
    :param private_key: The private key.
    :param file_type: The file type.
    """
    with open("company_data.txt", "a") as f:
        f.write(f"Company Number: {company_number}, Private Key: {private_key[0]}, n: {private_key[1]}, file_type: {file_type}\n")
