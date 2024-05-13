import os

import cv2
import numpy as np
from Entity.Characthers import characther
from Entity.e import getSession

image_path = r'C:\Users\ariel\PycharmProjects\pythonProject1\redD.png'
Session = getSession()
session = Session()
SOF="Ω"
import cv2
from Stenography.Stenography import *
class PVDEncoded(Stenography):
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

    def ret_pixel(self,id, p):
        """
        :param id: the digit to insert
        :param p: list of pixel values, where each pixel value is a list of RGB values
        :return: the updated pixel
        """
        delta = [0, 0, 0]
        for i in range(3):  # Assuming RGB values
            # Assuming p is a list of lists where each inner list represents RGB values
            delta[i] = p[1][i] - p[0][i]  # Subtract corresponding RGB values
            if id != 0:
                digit = id % 10
                delta[i] -= digit
                id = id // 10
        # Update the pixel values
        p[0][0] += delta[0]
        p[0][1] += delta[1]
        p[0][2] += delta[2]

        return p

    def create_image_from_pixels(self,pixels, pixel_locations, image_shape, image_path):
        """
        :param pixels: The list of pixels
        :param pixel_locations:The locations of the pixels in the image
        :param image_shape: Image size
        :return:The image with the updated pixels
        """
        # יצירת תמונה חדשה בגודל המתאים
        new_image = np.zeros(image_shape, dtype=np.uint8)
        pix, loc = extract_pixels(image_path)
        # השמה של ערכי הפיקסלים לתמונה החדשה בהתאם למיקומם
        for pixel, location in zip(pix, loc):
            x, y = location
            new_image[y, x] = pixel
        for pixel, location in zip(pixels, pixel_locations):
            x, y = location
            new_image[y, x] = pixel
        return new_image

    def pvd(self,str, image_path, range_pixel):
        """
        The main encryption function. Saves the information in a modified image.

        :param str: The string to encrypt.
        :param image_path: The path to the image where the information will be encrypted.
        :param range_pixel: Range of pixels to use for encryption.
        """

        str += SOF

        # Read the image
        image = cv2.imread(image_path)

        # Extract pixels
        pix, location = extract_pixels(image_path)

        index_in_pixels = 0
        x = []
        j = i = 0
        l = len(str)
        lis = []

        while i < len(pix) and j < len(str):
            x.append(pix[i])
            if (i + 1) % 2 == 0:
                lis = x
                list_of_six_pixels = self.ret_pixel(toid(str[j]), lis)

                # Assign values
                image[location[index_in_pixels][0]][location[index_in_pixels][1]] = list_of_six_pixels[0][0]
                image[location[index_in_pixels + 1][0]][location[index_in_pixels][1]] = list_of_six_pixels[0][1]
                image[location[index_in_pixels + 2][0]][location[index_in_pixels][1]] = list_of_six_pixels[0][2]
                index_in_pixels += 3
                image[location[index_in_pixels][0]][location[index_in_pixels][1]] = list_of_six_pixels[1][0]
                image[location[index_in_pixels + 1][0]][location[index_in_pixels][1]] = list_of_six_pixels[1][1]
                image[location[index_in_pixels + 2][0]][location[index_in_pixels][1]] = list_of_six_pixels[1][2]
                index_in_pixels += 3

                list_of_six_pixels.clear()
                lis.clear()
                j += 1
                l -= 1
                x.clear()
            i += 1

        print("sof steno")
        new_image = self.create_image_from_pixels(pix, location, image.shape, image_path)
        type_file = get_file_type(image_path)
        print(type_file)
        mod_path = "C:\\Users\\ariel\PycharmProjects\pythonProject1\image_c\modified_image" + "." + type_file
        print(mod_path)
        cv2.imwrite(mod_path, new_image)
# PVDEncoded=PVDEncoded()
# PVDEncoded.pvd("vbbcvbc",image_path=r"C:\Users\ariel\PycharmProjects\pythonProject1\redD.png",range_pixel=[50,110])