import wave

from Entity.e import getSession
from Stenography.Stenography import list_to_number, tochar, Stenography


class LsbDecodedA(Stenography):
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
        Convert a decimal number to its binary representation.

        :param number: A number in decimal representation.
        :return: The number in binary representation as a list of bits.
        """
        if number == 0:
            return [0, 0, 0, 0, 0, 0, 0, 0]
        bits = []
        while number > 0:
            bits.append(number % 2)
            number //= 2
        # Add leading zeros if needed to ensure the result has 8 bits
        i = 8 - len(bits)
        if i > 0:
            for _ in range(i):
                bits.append(0)
        return bits[::-1]  # Reverse the list to get the correct binary representation

    def decode(self,audio):
        """
        Decode hidden information from an audio file.

        :param audio: Path to the audio file.
        :return: Decoded hidden information.
        """
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
            t[3] = self.binary_representation(three_byte[2])[7]
            t[2] = self.binary_representation(three_byte[2])[6]
            t[1] = self.binary_representation(three_byte[1])[7]
            t[0] = self.binary_representation(three_byte[1])[6]
            id[j] = t[3] * mask[3] + t[2] * mask[2] + t[1] * mask[1] + t[0] * mask[0]
            j -= 1
            if self.binary_representation(three_byte[0])[1] == 0 and self.binary_representation(three_byte[0])[0] == 0:
                z = list_to_number(id)
                if z == 359:
                    return strs
            if self.binary_representation(three_byte[0])[1] == 0 and self.binary_representation(three_byte[0])[0] == 1:
                z = list_to_number(id)
                strs += tochar(z)
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
                z = list_to_number(id)
                if z == 359:
                    return strs
                strs += tochar(z)
                tmp = 1
                id = [0, 0, 0]
                j = 2
                t = [0, 0, 0, 0]
                three_byte.clear()
            l += 3
            i += 1
        return ""

# lsb_decodeA=LsbDecodedA()
# print(lsb_decodeA.decode('sampleStego.wav'))