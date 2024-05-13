import os
from Stenography.Stenography import *
import cv2
from Entity.e import getSession
Session = getSession()
session = Session()

class LSBDecoded(Stenography):
    _instance = None

    def __new__(cls, *args, **kwargs):
        if not cls._instance:
            cls._instance = super().__new__(cls)
        return cls._instance

    def __init__(self):
        if not hasattr(self, 'initialized'):
            super().__init__()
            self.Session = getSession()
            self.session = self.Session()
            self.initialized = True

    def decode(self, image_path, range_pix):
        """
        Decode a message from a given image file.

        :param image_path: Path to the image file.
        :param range_pix: Range of pixel locations where the message is encoded.
        :return: Decoded message.
        """
        type_file = get_file_type(image_path)
        mod_path = "C:\\Users\\ariel\PycharmProjects\pythonProject1\image_c\modified_image" + "." + type_file
        image_path = mod_path
        image = cv2.imread(image_path)

        # Align the image to a list of pixels
        # pixels, pixel_locations = extract_pixels(image_path)
        pixels, pixel_locations = process_specific_pixels(image_path, range_pix[0], range_pix[1])
        id = [0, 0, 0]
        t = [0, 0, 0, 0]
        mask = [8, 4, 2, 1]
        j = 2
        i = tmp = 1
        strs = ''
        l = 0
        while l < len(pixel_locations):
            pixel = image[pixel_locations[l][1]][pixel_locations[l][0]]
            t[3] = self.binary_representation(pixel[2])[7]
            t[2] = self.binary_representation(pixel[2])[6]
            t[1] = self.binary_representation(pixel[1])[7]
            t[0] = self.binary_representation(pixel[1])[6]
            id[j] = t[3] * mask[3] + t[2] * mask[2] + t[1] * mask[1] + t[0] * mask[0]
            j -= 1
            if self.binary_representation(pixel[0])[7] == 0 and self.binary_representation(pixel[0])[6] == 0:
                z = list_to_number(id)
                strs += tochar(z)
                return strs
            if self.binary_representation(pixel[0])[7] == 0 and self.binary_representation(pixel[0])[6] == 1:
                z = list_to_number(id)
                strs += tochar(z)
                ttt = len(strs)
                tos = 0
                if z < 100:
                    tos += 1
                    if z < 10:
                        tos += 1
                id = [0, 0, 0]
                j = 2
                t = [0, 0, 0, 0]
                i += 1 + tos
                l += 1 + tos
                continue

            if (i) % 3 == 0:
                z = list_to_number(id)
                strs += tochar(z)
                tmp = 1
                id = [0, 0, 0]
                j = 2
                t = [0, 0, 0, 0]
            l += 1
            i += 1
        return ""

    def binary_representation(self, number):
        """
        Get the binary representation of a number as a list of bits.

        :param number: Number to convert.
        :return: List representing the binary representation of the number.
        """
        if number == 0:
            return [0, 0, 0, 0, 0, 0, 0, 0]
        bits = []
        while number > 0:
            bits.append(number % 2)
            number //= 2
        i = 8 - len(bits)
        if i > 0:
            for i in range(i):
                bits.append(0)
        return bits[::-1]

# LsbDecoded = LSBDecoded()
# print(LSBDecoded.decode(self=LsbDecoded,image_path=r"C:\Users\ariel\PycharmProjects\pythonProject1\image_c\modified_image.png",range_pix=[50,80]))
