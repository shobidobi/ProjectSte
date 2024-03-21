import Entity.User
# import numpy as np
# from PIL import Image
# from scipy.fft import fft2, ifft2, fftshift, ifftshift
#
# def text_to_bin(text):
#     """Convert text to binary"""
#     binary_text = ''.join(format(ord(char), '08b') for char in text)
#     return binary_text
#
# def encode_dft(image_path, text):
#     binary_text = text_to_bin(text)
#
#     img = Image.open(image_path)
#     img_array = np.array(img)
#
#     # Encode text in high-frequency components
#     binary_index = 0
#     for i in range(20,50):  # Assuming 20 pixels
#         for j in range(img_array.shape[1]):
#             for k in range(img_array.shape[2]):
#                 if binary_index < len(binary_text):
#                     # Set the least significant bit to the corresponding bit of the binary text
#                     img_array[i, j, k] &= 0b1111111111111110  # Clear the least significant bit
#                     img_array[i, j, k] |= int(binary_text[binary_index])  # Set the least significant bit
#                     binary_index += 1
#
#     # Save the encoded image
#     img_encoded = Image.fromarray(img_array.astype('uint8'))
#     img_encoded.save("encoded_image_dft.png")
#
# # Example usage
# text_to_encode = "hello my name is ariel SOF"
# encode_dft("תמונה1.png", text_to_encode)




# import numpy as np
# from PIL import Image
# from scipy.fft import fft2, ifft2, fftshift, ifftshift
#
# def text_to_bin(text):
#     """Convert text to binary"""
#     binary_text = ''.join(format(ord(char), '08b') for char in text)
#     return binary_text
#
# def bin_to_text(binary_text):
#     """Convert binary to text"""
#     text = ''.join(chr(int(binary_text[i:i+8], 2)) for i in range(0, len(binary_text), 8))
#     return text
#
# def encode_dft(image_path, text):
#     binary_text = text_to_bin(text)
#
#     img = Image.open(image_path)
#     img_array = np.array(img)
#
#     # Compute 2D FFT
#     fft_result = fft2(img_array)
#     fft_result_shifted = fftshift(fft_result)
#
#     # Encode text in high-frequency components
#     binary_index = 0
#     for i in range(20):
#         for j in range(img_array.shape[1]):
#             for k in range(img_array.shape[2]):
#                 if binary_index < len(binary_text):
#                     if fft_result_shifted[i, j, k] > 0:
#                         fft_result_shifted[i, j, k] += int(binary_text[binary_index])
#                     else:
#                         fft_result_shifted[i, j, k] -= int(binary_text[binary_index])
#                     binary_index += 1
#
#     # Compute inverse FFT to get the encoded image
#     img_encoded_array = ifft2(ifftshift(fft_result_shifted)).real
#     img_encoded = Image.fromarray(img_encoded_array.astype('uint8'))
#     img_encoded.save("encoded_image_dft.png")
#
# # Example usage
# text_to_encode = "hello my name is ariel"
# encode_dft("תמונה1.png", text_to_encode)
#
# # Decoding
# img_encoded = Image.open("encoded_image_dft.png")
# img_encoded_array = np.array(img_encoded)
#
# # Retrieve text from high-frequency components
# binary_text = ''
# for i in range(20):
#     for j in range(img_encoded_array.shape[1]):
#         for k in range(img_encoded_array.shape[2]):
#             # Extract the least significant bit and append to binary_text
#             binary_text += str(img_encoded_array[i, j, k] & 1)
#
# # Convert binary text to ASCII
# decoded_text = bin_to_text(binary_text)
# print(decoded_text)
import numpy as np
from PIL import Image
from scipy.fft import fft2, ifft2, fftshift, ifftshift

def text_to_bin(text):
    """Convert text to binary"""
    binary_text = ''.join(format(ord(char), '08b') for char in text)
    return binary_text

def encode_dft(image_path, text):
    binary_text = text_to_bin(text)

    img = Image.open(image_path)
    img_array = np.array(img)

    # Perform FFT on the image
    img_fft = fft2(img_array)

    # Encode text in the real part of high-frequency components
    binary_index = 0
    for i in range(20, 50):  # Assuming 20 pixels
        for j in range(img_fft.shape[1]):
            for k in range(img_fft.shape[2]):
                if binary_index < len(binary_text):
                    # Set the real part of the high-frequency components to the corresponding bit of the binary text
                    img_fft[i, j, k] = complex(img_fft[i, j, k].real, int(binary_text[binary_index]))
                    binary_index += 1

    # Perform inverse FFT to get the encoded image
    img_encoded_array = ifft2(img_fft).real

    # Save the encoded image
    img_encoded = Image.fromarray(img_encoded_array.astype('uint8'))
    img_encoded.save("encoded_image_dft.png")

# Example usage
text_to_encode = "hello my name is ariel SOF"
encode_dft("תמונה1.png", text_to_encode)

