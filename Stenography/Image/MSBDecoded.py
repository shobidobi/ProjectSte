import cv2
from Entity.Characthers import characther
from Entity.e import getSession
image_path = r'C:\Users\ariel\PycharmProjects\pythonProject1\image_c\modified_image.png'
#image_path = r'C:\Users\ariel\Downloads\file (3).png'
from Stenography.Stenography import *

Session = getSession()
session = Session()
class MSBDecoded(Stenography):
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

    def decode(self,image_path, range_pixel):
        image = cv2.imread(image_path)
        print(range_pixel)
        # יישור התמונה לרשימת פיקסלים
        pixels, pixel_locations = process_specific_pixels(image_path, range_pixel[0], range_pixel[1])
        id = [0, 0, 0]
        t = [0, 0, 0, 0]
        mask = [8, 4, 2, 1]
        j = 2
        i = 1
        str_ret = ''
        l = 0
        while l < len(pixel_locations):
            pixel = image[pixel_locations[l][1]][pixel_locations[l][0]]
            t[3] = self.binary_representation(pixel[2])[1]
            t[2] = self.binary_representation(pixel[2])[0]
            t[1] = self.binary_representation(pixel[1])[1]
            t[0] = self.binary_representation(pixel[1])[0]
            id[j] = t[3] * mask[3] + t[2] * mask[2] + t[1] * mask[1] + t[0] * mask[0]
            j -= 1
            if self.binary_representation(pixel[0])[1] == 0 and self.binary_representation(pixel[0])[0] == 0:
                z = list_to_number(id)
                str_ret += tochar(z)
                return str_ret
            if self.binary_representation(pixel[0])[1] == 0 and self.binary_representation(pixel[0])[0] == 1:
                z = list_to_number(id)
                str_ret += tochar(z)
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
                str_ret += tochar(z)
                id = [0, 0, 0]
                j = 2
                t = [0, 0, 0, 0]
            l += 1
            i += 1
        return ""

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
# MSBDecoded=MSBDecoded()
# print(MSBDecoded.decode(image_path,[50,80]))

