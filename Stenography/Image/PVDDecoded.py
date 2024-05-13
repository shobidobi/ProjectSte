import cv2
import numpy as np
from Entity.Characthers import characther
from Entity.e import getSession
from Stenography.Stenography import *
Session = getSession()
session = Session()
SOF="Ω"
class PVDDecoded(Stenography):
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

    def ret_id(self,p):

        """

        :param digit: the digit to insert
        :param p: list of pixel values
        :return: the updated pixel
        """
        delta = [0, 0, 0]
        for i in range(3):
            delta[i] = p[1][i] - p[0][i]
        id_c = delta[0] * 1 + delta[1] * 10 + delta[2] * 100
        return id_c

    def pvd(self,image_path):
        """
        The main encryption function at the end of the function saves the information in the copy
        :param str:The string to encrypt
        :param image_path:The path to the image where the information will be encrypted
        """
        str = ""
        pix, location = extract_pixels(image_path)
        # pix, location=process_specific_pixels(image_path,50,110)
        i = 0
        lis_of_six = []
        while i < len(pix) - 1:
            lis_of_six.append(pix[i])
            i += 1
            lis_of_six.append(pix[i])
            c = tochar(self.ret_id(lis_of_six))

            if c == "Ω":
                return str
            str += tochar(self.ret_id(lis_of_six))
            lis_of_six.clear()
            i += 1


image_path = r'C:\Users\ariel\PycharmProjects\pythonProject1\image_c\modified_image.png'
# pvd_instance = PVDDecoded()
# print(pvd_instance.pvd(image_path))
