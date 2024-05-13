import json
import math
from Entity.Keys import get_key_by_user_id
l=[]
def modular_exponentiation(base, exponent, modulus):
    """
    Perform modular exponentiation.

    :param base: Base number.
    :param exponent: Exponent.
    :param modulus: Modulus.
    :return: Result of the modular exponentiation.
    """
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
    """
    Decrypt a ciphertext using RSA encryption.

    :param cyphertext: The ciphertext to decrypt.
    :param user_id: The user ID used as the private key.
    :return: The decrypted text.
    """
    # p = get_key_by_user_id(user_id)
    p = user_id
    print('decrypt_Text_Rsa')
    decrypted_text = ''.join(chr(modular_exponentiation(i, p[0], p[1])) for i in cyphertext)
    print(decrypted_text)
    return decrypted_text


def decrypt_num_Rsa(cyphertext, user_id):
    """
    Decrypt a ciphertext using RSA encryption and return numbers.

    :param cyphertext: The ciphertext to decrypt.
    :param user_id: The user ID used as the private key.
    :return: The decrypted numbers.
    """
    p = user_id
    print('decrypt_Text_Rsa')
    decrypted_text = [modular_exponentiation(i, p[0], p[1]) for i in cyphertext]
    print(decrypted_text)
    return decrypted_text


def decrypt_Text_Rsa_user(cyphertext, user_id):
    """
    Decrypt a ciphertext using RSA encryption with user-specific private key.

    :param cyphertext: The ciphertext to decrypt.
    :param user_id: The user ID to fetch the private key.
    :return: The decrypted text.
    """
    p = get_key_by_user_id(user_id)
    decrypted_text = ''.join(chr(modular_exponentiation(i, p[0], p[1])) for i in cyphertext)
    print(decrypted_text)
    return decrypted_text


def decrypt_with_key(data, key):
    """
    Decrypt data using a given key.

    :param data: The data to decrypt.
    :param key: The key used for decryption.
    :return: The decrypted data.
    """
    return bytes([char ^ key for char in data])


def read_company_data(_company_number, file_type):
    """
    Read company data from a file.

    :param _company_number: The company number.
    :param file_type: The file type.
    :return: Company data.
    """
    company_data = []
    print(_company_number, file_type)
    file_path = r"C:\Users\ariel\PycharmProjects\pythonProject1\Api_test\company_data.txt"
    with open(file_path, 'r') as file:
        for line in file:
            # Split the line by comma
            parts = line.split(',')
            print(len(parts))
            print(parts)
            # Get company and private key values
            company_number = int(parts[0].split(':')[1])
            private_key_str = parts[1].split(':')[1].strip()
            n_str = parts[2].split(':')[1].strip()
            file_type_str = parts[3].split(':')[1].strip()

            # Check if there are two numbers in the private key
            if ',' in private_key_str:
                # Split the string into two numbers and convert them to integers
                private_key = list(map(int, private_key_str.strip('()').split(',')))
            else:
                # If there's only one value, convert it to an integer
                private_key = [int(private_key_str)]
                n = [int(n_str)]

            if company_number == _company_number and file_type_str == file_type:
                company_data.append((company_number, private_key, n, file_type_str))
    return company_data.pop()
