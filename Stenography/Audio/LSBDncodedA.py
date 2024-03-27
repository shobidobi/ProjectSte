import wave
from Entity.Characthers import characther
from Entity.e import getSession

Session = getSession()
session = Session()
def list_to_number(digits):
    number = 0
    for digit in digits:
        number = number * 10 + digit
    return number
def binary_representation(number):
    """
    :param number: A number in decimal representation
    :return: The number in binary representation
    """
    if number == 0:
        return [0,0,0,0,0,0,0,0]
    bits = []
    while number > 0:
        bits.append(number % 2)
        number //= 2
    i=8-len(bits)
    if i>0:
        for i in range(i):
            bits.append(0)
    return bits[::-1]
def toid(id):
        # מציאת התו במסד הנתונים
    print(id)
    n_id=int(id)
    char_record = session.query(characther).filter_by(id=n_id).first()

    # if char_record:
    #     print(f"ID of '': {char_record[0]}")
    # else:
    #     print(f"'' not found in database")
    if char_record is not None:
        return char_record.get_char()
    if char_record is None:
        return " "


def decode():
    audio = wave.open("sampleStego.wav", mode='rb')
    frame_bytes = bytearray(list(audio.readframes(audio.getnframes())))
    id = [0, 0, 0]
    t = [0, 0, 0, 0]
    mask = [8, 4, 2, 1]
    j = 2
    i = tmp = 1
    strs = ''
    l = 0
    three_byte=[]
    while l < len(frame_bytes):
        three_byte.clear()
        for r in range(l,l+3):
            three_byte.append(frame_bytes[r])
        t[3] = binary_representation(three_byte[2])[7]
        t[2] = binary_representation(three_byte[2])[6]
        t[1] = binary_representation(three_byte[1])[7]
        t[0] = binary_representation(three_byte[1])[6]
        id[j] = t[3] * mask[3] + t[2] * mask[2] + t[1] * mask[1] + t[0] * mask[0]
        j -= 1
        if binary_representation(three_byte[0])[7] == 0 and binary_representation(three_byte[0])[6] == 0:
            z = list_to_number(id)
            strs += toid(z)
            return strs
        if binary_representation(three_byte[0])[7] == 0 and binary_representation(three_byte[0])[6] == 1:
            z = list_to_number(id)
            strs += toid(z)
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
            l += 1+ tos
            if 10<z<100:
                l+=1

            three_byte.clear()
            continue

        if (i) % 3 == 0:
            z = list_to_number(id)
            strs += toid(z)
            tmp = 1
            id = [0, 0, 0]
            j = 2
            t = [0, 0, 0, 0]
            three_byte.clear()
        l += 3
        i += 1
    return ""
print(decode())