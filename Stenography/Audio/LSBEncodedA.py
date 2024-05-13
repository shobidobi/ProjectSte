import wave

from Entity.e import getSession
from Stenography.Stenography import toid, Stenography

SOF="Ω"
class LsbEncodedA(Stenography):
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

    def transform_number(self, num):
        """
        Transform a single digit number into a tuple representing the corresponding range of values.

        :param num: Single digit number to transform.
        :return: Tuple representing the range of values corresponding to the input number.
        """
        if num == 1:
            return (12, 13)
        elif num == 2:
            return (14, 15)
        elif num == 3:
            return (16, 17)
        elif num == 4:
            return (0, 1)
        elif num == 5:
            return (2, 3)
        elif num == 6:
            return (4, 5)
        elif num == 7:
            return (6, 7)
        elif num == 8:
            return (8, 9)
        elif num == 9:
            return (10, 11)
        else:
            return (18, 19)

    def encode(self, audio_file, message):
        """
        Encode a message into a given audio file.

        :param audio_file: Path to the audio file.
        :param message: Message to encode.
        """
        print("\nEncoding Starts..")
        audio = wave.open(audio_file, mode="rb")
        frame_bytes = bytearray(list(audio.readframes(audio.getnframes())))
        message += SOF
        print(message)
        # message = message + int((len(frame_bytes)-(len(message)*8*8))/8) *'#'
        messarr = []
        ezer = [1, 0, 1, 1, 1, 2, 1, 3, 2, 0, 2, 1]
        flag = False
        p = 3
        index = 0
        for i in message:
            id = toid(i)
            p = 3
            flag = False
            if (index + 1) == len(message):
                p -= 2
            while id > 0:
                if (id // 10 == 0):
                    p -= 1
                    messarr.append(p)
                    flag = True
                # messarr.append(binary_representation(id%10))
                if (id % 10 > 3):
                    t = self.transform_number(id % 10)
                    if flag == False:
                        messarr.append(p)
                    messarr.append(ezer[t[0]])
                    messarr.append(ezer[t[1]])
                else:
                    if flag == False:
                        messarr.append(p)
                    messarr.append(0)
                    messarr.append(id % 10)
                id //= 10
            index += 1

        bits = list(map(int, ''.join([bin(ord(i)).lstrip('0b').rjust(8, '0') for i in message])))
        for i, bit in enumerate(messarr):
            frame_bytes[i] = (frame_bytes[i] & 252) | messarr[i]

        frame_modified = bytes(frame_bytes)
        for i in range(0, 20):
            print(frame_bytes[i])
        newAudio = wave.open(r'C:\Users\ariel\PycharmProjects\pythonProject1\Audio_c\sampleStego.wav', 'wb')
        newAudio.setparams(audio.getparams())
        newAudio.writeframes(frame_modified)

        newAudio.close()
        audio.close()
        print(" |---->successfully encoded inside sampleStego.wav")


audio_file_path = 'sampleStego.wav'
message = "156465"
# lsbEncodedA_i =LsbEncodedA()
# lsbEncodedA_i.encode(audio_file_path, message)
# decode()
