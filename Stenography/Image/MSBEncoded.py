

from PIL import Image

def encode_msb(original_image_path, secret_data, output_image_path):
    # Load the original image
    img = Image.open(original_image_path)

    # Convert secret data to binary
    binary_secret_data = ''.join(format(ord(char), '08b') for char in secret_data)

    data_index = 0

    # Iterate over each pixel in the image
    for i in range(img.width):
        for j in range(img.height):
            # Get the RGB values of the current pixel
            pixel = list(img.getpixel((i, j)))

            # Modify the most significant bit of each color component
            for color_channel in range(3):
                if data_index < len(binary_secret_data):
                    pixel[color_channel] = (pixel[color_channel] & 0b01111111) | (int(binary_secret_data[data_index]) << 7)
                    data_index += 1

            # Update the pixel in the image
            img.putpixel((i, j), tuple(pixel))

    # Save the encoded image
    img.save(output_image_path)

# Example usage
