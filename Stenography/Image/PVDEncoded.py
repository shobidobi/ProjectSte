from PIL import Image

def encode_pvd(original_image_path, secret_data, output_image_path):
    img = Image.open(original_image_path)
    width, height = img.size

    # Convert secret data to binary
    binary_secret_data = ''.join(format(ord(char), '08b') for char in secret_data)
    data_index = 0

    for y in range(height):
        for x in range(width):
            # Get the pixel values of the current and next pixels
            current_pixel = img.getpixel((x, y))
            next_pixel = img.getpixel((x + 1, y)) if x < width - 1 else current_pixel

            # Extract the least significant bit from each color component of the current pixel
            for color_channel in range(3):
                if data_index < len(binary_secret_data):
                    diff = next_pixel[color_channel] - current_pixel[color_channel]
                    if diff % 2 != int(binary_secret_data[data_index]):
                        if diff == 0 and next_pixel[color_channel] < 255:
                            next_pixel = tuple(next_pixel[i] + 1 if i == color_channel else next_pixel[i] for i in range(3))
                        elif diff == 0 and next_pixel[color_channel] == 255:
                            current_pixel = tuple(current_pixel[i] - 1 if i == color_channel else current_pixel[i] for i in range(3))
                        elif diff != 0 and next_pixel[color_channel] > 0:
                            next_pixel = tuple(next_pixel[i] - 1 if i == color_channel else next_pixel[i] for i in range(3))
                        else:
                            current_pixel = tuple(current_pixel[i] + 1 if i == color_channel else current_pixel[i] for i in range(3))
                        img.putpixel((x, y), current_pixel)
                        img.putpixel((x + 1, y), next_pixel)
                    data_index += 1

    img.save(output_image_path)


# Example usage
encode_pvd(r'C:\Users\ariel\PycharmProjects\pythonProject1\redD.png', "Hello, World!", "encoded_image_pvd.png")
