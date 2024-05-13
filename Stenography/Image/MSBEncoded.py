import os

import cv2
import numpy as np

from Entity.Characthers import characther
from Entity.e import getSession
# image_path = r'C:\Users\ariel\PycharmProjects\pythonProject1\modified_image.png'
Session = getSession()
session = Session()
from Stenography.Stenography import *
class MSBEncoded(Stenography):
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

    def ret_pixel(self,digit, p, flag):
        """

        :param digit: the digit to insert
        :param p: list of pixel values
        :param flag: describes the encryption
        :return: the updated pixel
        """

        binary_string = bin(digit)[2:]  # המרת המספר לבינארי והוצאת הספרה '0b' הראשונה
        binary_list = [int(digit) for digit in binary_string]  # המרת המחרוזת הבינארית לרשימה של ספרות בינאריות
        binary_list.reverse()
        c = 4 - len(binary_list)
        for i in range(0, c):
            binary_list.append(0)
        L = [1, 2, 4, 8]
        l = [0, 0]
        l[0] = L[0] * binary_list[0] + L[1] * binary_list[1]  # 2
        l[1] = L[2] * binary_list[2] + L[3] * binary_list[3]  # 1
        m = [0, 0, 0]
        for i in range(0, 3):
            m[i] = self.binary_representation(p[i])
        m[2][1] = binary_list[0]
        m[2][0] = binary_list[1]
        m[1][1] = binary_list[2]
        m[1][0] = binary_list[3]
        m[0][1] = flag[0]
        m[0][0] = flag[1]
        p[0] = binary_to_integer(m[0])
        p[1] = binary_to_integer(m[1])
        p[2] = binary_to_integer(m[2])
        return p

    def Decomposing_a_number(self,id, p, flag):
        """
        :param id: The number identifier in the database
        :param p: the list of three pixel from the image
        :param flag: A flag to mark the current state
        :return: The updated list of pixels after encryption
        """
        i = 0
        x = []
        while id > 0:
            digit = id % 10
            if id // 10 == 0:
                print(p[i])
                flag[0] = 0
                x.append(self.ret_pixel(digit, p[i], [0, flag[1]]))
                print("-----" + str(x))
                break
            print(p[i])
            x.append(self.ret_pixel(digit, p[i], flag))
            print(x)
            id = int(id / 10)
            i += 1
        return x

    def encode(self,str, image_path, range_pixel):
        subtraction = range_pixel[1] - range_pixel[0]
        if subtraction < (len(str) * 3):
            range_pixel[1] += len(str) - subtraction
        image = cv2.imread(image_path)
        print(str)
        # יישור התמונה לרשימת פיקסלים
        pix, location = process_specific_pixels(image_path, range_pixel[0], range_pixel[1])
        index_in_pixels = 0
        x = []
        j = i = 0
        l = len(str)
        while i < len(pix) and j < len(str):
            x.append(pix[i])
            if (i + 1) % 3 == 0:
                print(l)
                if (l - 1) == 0:
                    list_of_three_pixels = self.Decomposing_a_number(toid(str[j]), x, [1, 0])
                    image[location[index_in_pixels][0]][location[index_in_pixels][1]] = list_of_three_pixels[0]
                    print(index_in_pixels + 1)
                    print(len(list_of_three_pixels))
                    print(image[location[index_in_pixels + 1][0]][location[index_in_pixels][1]])
                    if len(list_of_three_pixels) < 3:
                        if len(list_of_three_pixels) == 1:
                            list_of_three_pixels.append(x[1])
                        list_of_three_pixels.append(x[2])
                    image[location[index_in_pixels + 1][0]][location[index_in_pixels][1]] = list_of_three_pixels[1]
                    image[location[index_in_pixels + 2][0]][location[index_in_pixels][1]] = list_of_three_pixels[2]
                    break
                f = False
                if toid(str[j]) // 10 == 0:

                    list_of_three_pixels = self.Decomposing_a_number(toid(str[j]), x, [0, 1])
                else:
                    list_of_three_pixels = self.Decomposing_a_number(toid(str[j]), x, [1, 1])
                if len(list_of_three_pixels) < 3:
                    if len(list_of_three_pixels) == 1:
                        list_of_three_pixels.append(x[1])
                    list_of_three_pixels.append(x[2])
                image[location[index_in_pixels][0]][location[index_in_pixels][1]] = list_of_three_pixels[0]
                image[location[index_in_pixels + 1][0]][location[index_in_pixels][1]] = list_of_three_pixels[1]
                image[location[index_in_pixels + 2][0]][location[index_in_pixels][1]] = list_of_three_pixels[2]
                index_in_pixels += 3
                list_of_three_pixels.clear()
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

    def binary_representation(self,number):
        if number == 0:
            return [0]
        bits = []
        while number > 0:
            bits.append(number % 2)
            number //= 2
        i = 8 - len(bits)
        if i > 0:
            for i in range(i):
                bits.append(0)
        return bits[::-1]

# MSBEncoded=MSBEncoded()
# MSBEncoded.encode("arbkibibel",r"C:\Users\ariel\PycharmProjects\pythonProject1\redD.png",[50,80])

