
import wave
from Entity.Characthers import characther
from Entity.e import getSession

Session = getSession()
session = Session()
def toid(str):
    """
    :param str: A character to check an ID in the database
    :return: id of the character
    """
    for char in str:
        # מציאת התו במסד הנתונים
        char_record = session.query(characther.id).filter_by(char=char).first()
        if char_record:
            print(f"ID of '{char}': {char_record[0]}")
        else:
            print(f"'{char}' not found in database")
            return 500
    return char_record[0]
def binary_representation(number):
    """
    :param number: A number in decimal representation
    :return: The number in binary representation
    """
    if number == 0:
        return [0,0]
    bits = []
    while number > 0:
        bits.append(number % 2)
        number //= 2
    i=8-len(bits)
    # if i>0:
    #     for i in range(i):
    #         bits.append(0)
    return bits[::-1]
SOF="Ω"
def transform_number(num):
    if num == 4:
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
        return "מספר לא תקין"
def encode(audio_file,message):
	print("\nEncoding Starts..")
	audio = wave.open(audio_file,mode="rb")
	frame_bytes = bytearray(list(audio.readframes(audio.getnframes())))
	message+=SOF
	print(message)
	# message = message + int((len(frame_bytes)-(len(message)*8*8))/8) *'#'
	messarr=[]
	ezer=[1,0,1,1,1,2,1,3,2,0,2,1]
	flag=False
	p=3
	index=0
	for i in message:
		id=toid(i)
		p=3
		flag=False
		if (index+1)==len(message):
			p-=2
		while id>0:
			if(id//10==0):
				p-=1
				messarr.append(p)
				flag=True
			# messarr.append(binary_representation(id%10))
			if(id%10>3):
				t=transform_number(id%10)
				if flag==False:
					messarr.append(p)
				messarr.append(ezer[t[0]])
				messarr.append(ezer[t[1]])
			else:
				if flag == False:
					messarr.append(p)
				messarr.append(0)
				messarr.append(id % 10)
			id//=10
		index += 1

	bits = list(map(int, ''.join([bin(ord(i)).lstrip('0b').rjust(8,'0') for i in message])))
	for i, bit in enumerate(messarr):
	    frame_bytes[i] = (frame_bytes[i] & 252) | messarr[i]

	frame_modified = bytes(frame_bytes)
	for i in range(0,20):
		print(frame_bytes[i])
	newAudio =  wave.open('sampleStego.wav', 'wb')
	newAudio.setparams(audio.getparams())
	newAudio.writeframes(frame_modified)

	newAudio.close()
	audio.close()
	print(" |---->succesfully encoded inside sampleStego.wav")

# def decode():
# 	print("\nDecoding Starts..")
# 	audio = wave.open("sampleStego.wav", mode='rb')
# 	frame_bytes = bytearray(list(audio.readframes(audio.getnframes())))
# 	extracted = [frame_bytes[i] & 1 for i in range(len(frame_bytes))]
# 	string = "".join(chr(int("".join(map(str,extracted[i:i+8])),2)) for i in range(0,len(extracted),8))
# 	decoded = string.split("###")[0]
# 	print("Sucessfully decoded: "+decoded)
# 	audio.close()
#
# def decode():
# 	print("\nDecoding Starts..")
# 	audio = wave.open("sampleStego.wav", mode='rb')
# 	frame_bytes = bytearray(list(audio.readframes(audio.getnframes())))
# 	extracted = [frame_bytes[i] & 1 for i in range(len(frame_bytes))]
# 	string = "".join(chr(int("".join(map(str,extracted[i:i+8])),2)) for i in range(0,len(extracted),8))
# 	decoded = string.split("###")[0]
# 	print("Sucessfully decoded: "+decoded)
# 	audio.close()
audio_file_path = r'C:\Users\ariel\PycharmProjects\pythonProject1\Audio_c\0cdaa711-c15c-4dcb-bfe5-54e8e13fb8a2.wav'
message = "aaaa"
encode(audio_file_path, message)
# decode()
def list_to_number(digits):
    number = 0
    for digit in digits:
        number = number * 10 + digit
    return number
