from PIL import Image

def decode_lsb(encoded_image_path):
    # Load the encoded image
    img = Image.open(encoded_image_path)

    binary_data = ''

    # Iterate over each pixel in the image
    for i in range(img.width):
        for j in range(img.height):
            # Get the RGB values of the current pixel
            pixel = list(img.getpixel((i, j)))

            # Extract the least significant bit from each color component
            for color_channel in range(3):
                binary_data += str(pixel[color_channel] & 1)

    # Convert binary data to ASCII characters
    decoded_data = ''.join([chr(int(binary_data[i:i+8], 2)) for i in range(0, len(binary_data), 8)])

    return decoded_data

# Example usage
# decoded_data = decode_lsb("encoded_image.png")
# print(decoded_data)
