import wave
import wave
from Entity.Characthers import characther
from Entity.e import getSession
from Stenography.Stenography import Stenography, toid, tochar

Session = getSession()
session = Session()
class MSBDecodedA(Stenography):
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



    def binary_representation(self,number):
        """
        :param number: A number in decimal representation
        :return: The number in binary representation
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

    def decode(self,audio):
        # audio = wave.open("sampleStego.wav", mode='rb')
        audio = wave.open(audio, mode='rb')
        frame_bytes = bytearray(list(audio.readframes(audio.getnframes())))
        id = [0, 0, 0]
        t = [0, 0, 0, 0]
        mask = [8, 4, 2, 1]
        j = 2
        i = tmp = 1
        strs = ''
        l = 0
        three_byte = []
        while l < len(frame_bytes):
            three_byte.clear()
            for r in range(l, l + 3):
                three_byte.append(frame_bytes[r])
            t[3] = self.binary_representation(three_byte[2])[1]
            t[2] = self.binary_representation(three_byte[2])[0]
            t[1] = self.binary_representation(three_byte[1])[1]
            t[0] = self.binary_representation(three_byte[1])[0]
            id[j] = t[3] * mask[3] + t[2] * mask[2] + t[1] * mask[1] + t[0] * mask[0]
            j -= 1
            if self.binary_representation(three_byte[0])[1] == 0 and self.binary_representation(three_byte[0])[0] == 0:
                z = super().list_to_number(id)
                if z == 359:
                    return strs
                strs += tochar(z)
                return strs
            if self.binary_representation(three_byte[0])[1] == 0 and self.binary_representation(three_byte[0])[0] == 1:
                z = super().list_to_number(id)
                if z == 359:
                    return strs
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
                if 10 < z < 100:
                    l += 1

                three_byte.clear()
                continue

            if (i) % 3 == 0:
                z = super().list_to_number(id)
                if z == 359:
                    return strs
                strs +=tochar(z)
                tmp = 1
                id = [0, 0, 0]
                j = 2
                t = [0, 0, 0, 0]
                three_byte.clear()
            l += 3
            i += 1
        return ""
# MSBDecodedAI=MSBDecodedA()
# print(MSBDecodedAI.decode(r'C:\Users\ariel\PycharmProjects\pythonProject1\Audio_c\sampleStego.wav'))