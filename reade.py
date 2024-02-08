import numpy as np
from PIL import Image
from scipy.fft import fft2, ifft2, fftshift, ifftshift

# def bin_to_text(binary_text):
#     """Convert binary to text"""
#     text = ''.join([chr(int(binary_text[i:i + 8], 2)) for i in range(0, len(binary_text), 8)])
#     return text
#
# def decode_dft(image_path):
#     img = Image.open(image_path)
#     img_array = np.array(img)
#
#     # Initialize binary text
#     binary_text = ''
#
#     # Define the pixel range (20-50)
#     start_pixel = 20
#     end_pixel = 50
#
#     # Decode text until the word "SOF" is found or the end of the specified pixel range is reached
#     for i in range(start_pixel, min(end_pixel, img_array.shape[0])):
#         for j in range(img_array.shape[1]):
#             for k in range(img_array.shape[2]):
#                 # Append the least significant bit to the binary text
#                 binary_text += str(img_array[i, j, k] & 1)
#
#                 # Check if the decoded text contains "SOF"
#                 if len(binary_text) >= 8 * len("SOF") and bin_to_text(binary_text)[-len("SOF"):] == "SOF":
#                     return bin_to_text(binary_text)
#
#     # If the word "SOF" is not found, return the entire decoded text
#     return bin_to_text(binary_text)
#
# # Example usage
# decoded_text = decode_dft("encoded_image_dft.png")
# print(decoded_text)

# def decode_dft(encoded_image_path):
#     # Load the encoded image
#     img_encoded = Image.open(encoded_image_path)
#     img_encoded_array = np.array(img_encoded)
#
#     # Perform FFT on the encoded image
#     img_fft_encoded = fft2(img_encoded_array)
#
#     # Extract the binary text from the real part of high-frequency components
#     decoded_text = ""
#     for i in range(20, 50):  # Assuming 20 pixels
#         for j in range(img_fft_encoded.shape[1]):
#             for k in range(img_fft_encoded.shape[2]):
#                 decoded_text += str(int(img_fft_encoded[i, j, k].real) & 1)
#
#     # Convert binary text to ASCII
#     decoded_text = ''.join([chr(int(decoded_text[i:i+8], 2)) for i in range(0, len(decoded_text), 8)])
#
#     return decoded_text
#
# # Example usage for decoding
# decoded_text = decode_dft("encoded_image_dft.png")
# print(decoded_text)
import numpy as np
from PIL import Image
from scipy.fft import fft2, ifft2, fftshift, ifftshift

def decode_dft(encoded_image_path, message_length):
    # Load the encoded image
    img_encoded = Image.open(encoded_image_path)
    img_encoded_array = np.array(img_encoded)

    # Perform FFT on the encoded image
    img_fft_encoded = fft2(img_encoded_array)

    # Extract the real part of the central frequency components
    extracted_bits = ""
    for i in range(img_fft_encoded.shape[0]//2 - 5, img_fft_encoded.shape[0]//2 + 5):
        for j in range(img_fft_encoded.shape[1]//2 - 5, img_fft_encoded.shape[1]//2 + 5):
            for k in range(img_fft_encoded.shape[2]):
                # Use complex values to store the information
                extracted_bits += str(int(img_fft_encoded[i, j, k].real) & 1)
                extracted_bits += str(int(img_fft_encoded[i, j, k].imag) & 1)

    # Convert binary text to ASCII
    decoded_text = ''.join([chr(int(extracted_bits[i:i+8], 2)) for i in range(0, len(extracted_bits), 8)])

    return decoded_text[:message_length]

# Example usage for decoding
decoded_text = decode_dft("encoded_image_dft.png", message_length=30)
print(decoded_text)
