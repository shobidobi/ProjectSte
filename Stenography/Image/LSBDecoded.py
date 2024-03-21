# from PIL import Image
#
# def decode_lsb(encoded_image_path):
#     # Load the encoded image
#     img = Image.open(encoded_image_path)
#
#     binary_data = ''
#
#     # Iterate over each pixel in the image
#     width, height = img.size
#     for i in range(width):
#         for j in range(height):
#             # Get the RGB values of the current pixel
#             pixel = list(img.getpixel((i, j)))
#
#             # Extract the least significant bit from each color component
#             for color_channel in range(3):
#                 binary_data += str(pixel[color_channel] & 1)
#
#     # Convert binary data to ASCII characters
#     decoded_data = ''
#     for i in range(0, len(binary_data), 8):
#         byte = binary_data[i:i+8]
#         if byte:
#             decoded_data += chr(int(byte, 2))
#
#     return decoded_data

# Example usage
# decoded_data = decode_lsb("encoded_image.png")
# print(decoded_data)
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
#             if index < len(secret_data):
#                 r, g, b = img.getpixel((col, row))
#                 ascii_val = ord(secret_data[index])
#                 r = (r & 0xFE) | ((ascii_val & 0x100) >> 8)
#                 g = (g & 0xFE) | ((ascii_val & 0x80) >> 7)
#                 b = (b & 0xFE) | ((ascii_val & 0x40) >> 6)
#                 encoded.putpixel((col, row), (r, g, b))
#                 index += 1
#             else:
#                 break
#     return encoded
#
# # def decode_lsb(encoded_image_path):
# #     img = Image.open(encoded_image_path)
# #     width, height = img.size
# #     secret_data = ''
# #     index = 0
# #
# #     for row in range(height):
# #         for col in range(width):
# #             r, g, b = img.getpixel((col, row))
# #             ascii_val = ((r & 1) << 8) | ((g & 1) << 7) | ((b & 1) << 6)
# #             if ascii_val != 0:
# #                 secret_data += chr(ascii_val)
# #                 index += 1
# #             else:
# #                 break
# #     return secret_data
import sys

import cv2
import math
import numpy as np

# Embed secret in the n least significant bit.
# Lower n make picture less loss but lesser storage capacity.
BITS = 2

LOW_BITS = (1 << BITS) - 1
BYTES_PER_BYTE = math.ceil(8 / BITS)
FLAG = '%'


def extract(path):
    img = cv2.imread(path, cv2.IMREAD_ANYCOLOR)
    data = np.reshape(img, -1)
    total = data.shape[0]
    res = ''
    idx = 0
    # Decode message length
    while idx < total // BYTES_PER_BYTE:
        ch = decode(data[idx * BYTES_PER_BYTE: (idx + 1) * BYTES_PER_BYTE])
        idx += 1
        if ch == FLAG:
            break
        res += ch
    end = int(res) + idx
    assert end <= total // BYTES_PER_BYTE, "Input image isn't correct."

    secret = ''
    while idx < end:
        secret += decode(data[idx * BYTES_PER_BYTE: (idx + 1) * BYTES_PER_BYTE])
        idx += 1
        # print(secret)
    return secret


def decode(block):
    val = 0
    for idx in range(len(block)):
        val |= (block[idx] & LOW_BITS) << (idx * BITS)
    return chr(val)


if __name__ == '__main__':
    if len(sys.argv) == 2:
        img_path = sys.argv[1]
    else:
        img_path = r'C:\Users\ariel\PycharmProjects\pythonProject1\redD_lsb_embeded.png'

    msg = extract(img_path)
    print(msg)