#
# from PIL import Image
# def encode_msb(original_image_path, secret_data, output_image_path):
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
#             # Modify the most significant bit of each color component
#             for color_channel in range(3):
#                 if data_index < len(binary_secret_data):
#                     pixel[color_channel] = (pixel[color_channel] & 0b01111111) | (int(binary_secret_data[data_index]) << 7)
#                     data_index += 1
#
#             # Update the pixel in the image
#             img.putpixel((i, j), tuple(pixel))
#
#     # Save the encoded image
#     img.save(output_image_path)
#
# # Example usage
import sys
import sys
import math
from os import path

import cv2
import numpy as np

# Embed secret in the n most significant bit.
# Lower n make picture less loss but lesser storage capacity.
BITS = 2

HIGH_BITS = 256 - (1 << BITS)
LOW_BITS = (1 << BITS) - 1
BYTES_PER_BYTE = math.ceil(8 / BITS)
FLAG = '%'


def insert(img_path, msg):
    img = cv2.imread(img_path, cv2.IMREAD_ANYCOLOR)
    ori_shape = img.shape
    max_bytes = ori_shape[0] * ori_shape[1] // BYTES_PER_BYTE
    msg = '{}{}{}'.format(chr(len(msg)), FLAG, msg)
    assert max_bytes >= len(
        msg), "Message greater than capacity:{}".format(max_bytes)
    data = np.reshape(img, -1)
    for (idx, val) in enumerate(msg):
        encode(data[idx * BYTES_PER_BYTE: (idx + 1) * BYTES_PER_BYTE], val)
    img = np.reshape(data, ori_shape)
    filename, _ = path.splitext(img_path)
    filename += '_msb_embedded' + ".png"
    cv2.imwrite(filename, img)
    return filename


def encode(block, data):
    # returns the Unicode code from a given character
    data = ord(data)
    for idx in range(len(block)):
        block[idx] &= LOW_BITS
        block[idx] |= (data >> (BITS * (BYTES_PER_BYTE - idx - 1))) & HIGH_BITS


if __name__ == '__main__':

    if len(sys.argv) == 3:
        img_path = sys.argv[1]
        msg = sys.argv[2]
    else:
        img_path = r'C:\Users\ariel\PycharmProjects\pythonProject1\redD.png'
        msg = 'maccabi haifa champion.'

    res_path = insert(img_path, msg)
    print("Successfully embedded.")

