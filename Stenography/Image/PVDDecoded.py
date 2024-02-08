from PIL import Image
def decode_pvd(encoded_image_path):
    img = Image.open(encoded_image_path)
    width, height = img.size

    binary_secret_data = ''

    for y in range(height):
        for x in range(width):
            # Get the pixel values of the current and next pixels
            current_pixel = img.getpixel((x, y))
            next_pixel = img.getpixel((x + 1, y)) if x < width - 1 else current_pixel

            # Extract the least significant bit from each color component of the current pixel
            for color_channel in range(3):
                diff = next_pixel[color_channel] - current_pixel[color_channel]
                binary_secret_data += str(diff % 2)

    # Convert binary data to ASCII characters
    decoded_data = ''.join([chr(int(binary_secret_data[i:i+8], 2)) for i in range(0, len(binary_secret_data), 8)])

    return decoded_data
