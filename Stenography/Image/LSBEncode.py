from PIL import Image

# def encode_lsb(original_image_path, secret_data, output_image_path=None):
#     # Load the original image
#     img = Image.open(original_image_path)
#
#     # Convert secret data to binary
#     binary_secret_data = ''.join(format(ord(char), '08b') for char in secret_data)
#
#     data_index = 0
#
#     # Iterate over each pixel in the image
#     for i in range(img.width):
#         for j in range(img.height):
#             # Get the RGB values of the current pixel
#             pixel = list(img.getpixel((i, j)))
#
#             # Modify the least significant bit of each color component
#             for color_channel in range(3):
#                 if data_index < len(binary_secret_data):
#                     pixel[color_channel] = pixel[color_channel] & ~1 | int(binary_secret_data[data_index])
#                     data_index += 1
#
#             # Update the pixel in the image
#             img.putpixel((i, j), tuple(pixel))
#
#     # Save the encoded image
#     img.save(original_image_path)
#     return original_image_path

# Example usage
#encode_lsb("original_image.png", "Hello, World!", "encoded_image.png")
# from PIL import Image
#
# def encode_lsb(input_image_path, secret_data):
#     img = Image.open(input_image_path)
#     encoded = img.copy()
#     width, height = img.size
#     index = 0
#
#     for row in range(height):
#         for col in range(width):
#             r, g, b = img.getpixel((col, row))
#             if index < len(secret_data):
#                 ascii_val = ord(secret_data[index])
#                 r = r & 0xFE | ((ascii_val & 0x100) >> 8)
#                 g = g & 0xFE | ((ascii_val & 0x80) >> 7)
#                 b = b & 0xFE | ((ascii_val & 0x40) >> 6)
#                 encoded.putpixel((col, row), (r, g, b))
#                 index += 1
#             else:
#                 break
#     return encoded
import sys
import math
from os import path

import cv2
import numpy as np

# Embed secret in the n least significant bit.
# Lower n make picture less loss but lesser storage capacity.
BITS = 2

HIGH_BITS = 256 - (1 << BITS)
LOW_BITS = (1 << BITS) - 1
BYTES_PER_BYTE = math.ceil(8 / BITS)
FLAG = '%'


def insert(img_path, msg):
    img = cv2.imread(img_path, cv2.IMREAD_ANYCOLOR)
    # Save origin shape to restore image
    ori_shape = img.shape
    print(ori_shape)
    max_bytes = ori_shape[0] * ori_shape[1] // BYTES_PER_BYTE
    # Encode message with length
    msg = '{}{}{}'.format(len(msg), FLAG, msg)
    assert max_bytes >= len(
        msg), "Message greater than capacity:{}".format(max_bytes)
    data = np.reshape(img, -1)
    for (idx, val) in enumerate(msg):
        encode(data[idx * BYTES_PER_BYTE: (idx + 1) * BYTES_PER_BYTE], val)

    img = np.reshape(data, ori_shape)
    filename, _ = path.splitext(img_path)
    filename += '_lsb_embeded' + ".png"
    cv2.imwrite(filename, img)
    return filename


def encode(block, data):
    # returns the Unicode code from a given character
    data = ord(data)
    for idx in range(len(block)):
        block[idx] &= HIGH_BITS
        block[idx] |= (data >> (BITS * idx)) & LOW_BITS


if __name__ == '__main__':

    if len(sys.argv) == 3:
        img_path = sys.argv[1]
        msg = sys.argv[2]
    else:
        img_path = r'C:\Users\ariel\PycharmProjects\pythonProject1\redD.png'
        msg = 'maccabi haifa champion.'

    res_path = insert(img_path, msg)
    print("Successfully embedded.")
