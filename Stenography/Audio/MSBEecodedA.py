import wave

from Entity.e import getSession
from Stenography.Stenography import toid, Stenography

SOF="Ω"

class MSBEecodedA(Stenography):
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

    def transform_number(self,num):
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

    def encode(self,audio_file, message):
        print("\nEncoding Starts..")
        audio = wave.open(audio_file, mode="rb")
        frame_bytes = bytearray(list(audio.readframes(audio.getnframes())))
        message += SOF
        print(message)
        # message = message + int((len(frame_bytes)-(len(message)*8*8))/8) *'#'
        messarr = []
        ezer = [64, 0, 64, 64, 64, 128, 64, 192, 128, 0, 128, 64, 0, 64, 0, 128, 0, 192, 0, 0]
        flag = False
        p = 192
        dup = 0
        index = 0
        for i in message:
            id = toid(i)
            dup = id
            p = 192
            flag = False
            if (index + 1) == len(message):
                if id < 100:
                    p -= 64
            while id > 0:
                if (id // 10 == 0):
                    if dup < 100:
                        p -= 64
                    elif dup > 100:
                        p -= 128
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
                    t = self.transform_number(id % 10)
                    if flag == False:
                        messarr.append(p)
                    messarr.append(ezer[t[0]])
                    messarr.append(ezer[t[1]])
                id //= 10
            index += 1

        bits = list(map(int, ''.join([bin(ord(i)).lstrip('0b').rjust(8, '0') for i in message])))
        for i, bit in enumerate(messarr):
            frame_bytes[i] = (frame_bytes[i] & 63) | messarr[i]

        frame_modified = bytes(frame_bytes)
        for i in range(0, 20):
            print(frame_bytes[i])
        # newAudio =  wave.open('sampleStego.wav', 'wb')
        # newAudio.setparams(audio.getparams())
        # newAudio.writeframes(frame_modified)
        newAudio = wave.open(r'C:\Users\ariel\PycharmProjects\pythonProject1\Audio_c\sampleStego.wav', 'wb')
        newAudio.setparams(audio.getparams())
        newAudio.writeframes(frame_modified)

        newAudio.close()
        audio.close()
        print(" |---->succesfully encoded inside sampleStego.wav")



audio_file_path = 'sampleStego.wav'
message = "nvdsjvljnxn"
# MSBEecodedAi=MSBEecodedA()
# MSBEecodedAi.encode(audio_file_path, message)

