import cv2
import numpy as np

def text_to_bin(text):
    binary_text = ''.join(format(ord(char), '08b') for char in text)
    return binary_text

def hide_text_in_image(image_path, secret_text, output_path):
    # Read the image
    img = cv2.imread(image_path)

    # Convert the secret text to binary
    binary_text = text_to_bin(secret_text)

    # Flatten the image's Y channel values
    img_yuv = cv2.cvtColor(img, cv2.COLOR_BGR2YUV)
    y_channel = img_yuv[:,:,0].flatten()

    # Embed the binary text into the Y channel values
    for i in range(len(binary_text)):
        if i < len(y_channel):
            y_channel[i] = (y_channel[i] & 0b11111110) | int(binary_text[i])

    # Reshape and update the image
    img_yuv[:,:,0] = y_channel.reshape(img.shape[:2])
    img_encoded = cv2.cvtColor(img_yuv, cv2.COLOR_YUV2BGR)

    # Save the encoded image
    cv2.imwrite(output_path, img_encoded)

# Example usage
hide_text_in_image("image3.png", "Hello, steganography!", "encoded_image.jpg")
