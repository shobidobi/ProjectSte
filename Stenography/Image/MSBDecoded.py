# from PIL import Image
#
# def decode_msb(encoded_image_path):
#     # Load the encoded image
#     img = Image.open(encoded_image_path)
#
#     binary_data = ''
#
#     # Iterate over each pixel in the image
#     for i in range(img.width):
#         for j in range(img.height):
#             # Get the RGB values of the current pixel
#             pixel = list(img.getpixel((i, j)))
#
#             # Extract the most significant bit from each color component
#             for color_channel in range(3):
#                 binary_data += str(pixel[color_channel] >> 7)
#
#     # Convert binary data to ASCII characters
#     decoded_data = ''.join([chr(int(binary_data[i:i+8], 2)) for i in range(0, len(binary_data), 8)])
#
#     return decoded_data
#
import math
from os import path

import cv2
import numpy as np

import cv2
import numpy as np

BITS = 2
HIGH_BITS = 256 - (1 << BITS)
LOW_BITS = (1 << BITS) - 1
BYTES_PER_BYTE = 8 // BITS
FLAG = '%'

def extract(img_path):
    img = cv2.imread(img_path, cv2.IMREAD_ANYCOLOR)
    data = np.reshape(img, -1)
    msg_length = extract_msg_length(data)
    msg = ''
    for idx in range(msg_length):
        msg += chr(extract_byte(data[idx * BYTES_PER_BYTE: (idx + 1) * BYTES_PER_BYTE]))
    return msg

def extract_msg_length(data):
    length_str = ''
    for byte in data[:BYTES_PER_BYTE]:
        length_str += chr(byte & LOW_BITS)
    print("length_str:", length_str)
    length, _, _ = length_str.partition(FLAG)
    return int(length)

def extract_byte(block):
    byte = 0
    for idx, val in enumerate(block):
        byte |= (val & HIGH_BITS) >> (BITS * (BYTES_PER_BYTE - idx - 1))
    return byte

if __name__ == '__main__':
    img_path = r'C:\Users\ariel\PycharmProjects\pythonProject1\redD_msb_embedded.png'
    msg = extract(img_path)
    print("Extracted message:", msg)


