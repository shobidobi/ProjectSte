import cv2
from Entity.Characthers import characther
from Entity.e import getSession
image_path = r'C:\Users\ariel\PycharmProjects\pythonProject1\modified_image.png'
Session = getSession()
session = Session()

def binary_representation(number):
    if number == 0:
        return [0]
    bits = []
    while number > 0:
        bits.append(number % 2)
        number //= 2
    i=8-len(bits)
    if i>0:
        for i in range(i):
            bits.append(0)
    return bits[::-1]
def decode(image_path):
    image = cv2.imread(image_path)

    # יישור התמונה לרשימת פיקסלים
    pixels, pixel_locations = extract_pixels(image_path)
    id=[0,0,0]
    t=[0,0,0,0]
    mask=[8,4,2,1]
    j=2
    i=1
    str_ret= ''
    l=0
    while l<len(pixel_locations):
        pixel=image[pixel_locations[l][1]][pixel_locations[l][0]]
        t[3]=binary_representation(pixel[2])[1]
        t[2]=binary_representation(pixel[2])[0]
        t[1]=binary_representation(pixel[1])[1]
        t[0]=binary_representation(pixel[1])[0]
        id[j]=t[3]*mask[3]+t[2]*mask[2]+t[1]*mask[1]+t[0]*mask[0]
        j-=1
        if binary_representation(pixel[0])[1]==0 and binary_representation(pixel[0])[0]==0:

            z = list_to_number(id)
            str_ret += tochar(z)
            return str_ret
        if binary_representation(pixel[0])[1]==0 and binary_representation(pixel[0])[0]==1:
            z = list_to_number(id)
            str_ret += tochar(z)
            tos=0
            if z<100:
                tos+=1
                if z<10:
                    tos+=1
            id=[0,0,0]
            j = 2
            t = [0, 0, 0, 0]
            i+=1+tos
            l+=1+tos
            continue

        if (i)%3==0:
            z=list_to_number(id)
            str_ret+=tochar(z)
            id=[0,0,0]
            j=2
            t=[0,0,0,0]
        l+=1
        i+=1
    return ""

def list_to_number(digits):
    number = 0
    for digit in digits:
        number = number * 10 + digit
    return number
def extract_lowest_2_bits(image_path):
    # קריאת התמונה באמצעות OpenCV
    image = cv2.imread(image_path)

    # יישור התמונה לרשימת פיקסלים
    pixels = image.reshape(
        (-1, 3))  # משנה את הצורה של התמונה ל־(-1, 3), כאשר -1 מציין ל-Python להתאים את המידות באופן אוטומטי
    # לכמות הפיקסלים, ו־3 מציין את הגודל של כל פיקסל (RGB)

    # יצירת רשימה חדשה שבה מופיעים רק שני הביטים הנמוכים של כל ערך RGB
    lowest_2_bits_pixels = []
    for pixel in pixels:
        new_pixel = [value & 0b11000000 for value in pixel]
        lowest_2_bits_pixels.append(new_pixel)
    return lowest_2_bits_pixels
def extract_pixels(image_path):
    # קריאת התמונה באמצעות OpenCV
    image = cv2.imread(image_path)

    # יישור התמונה לרשימת פיקסלים
    pixels = image.reshape((-1, 3))  # משנה את הצורה של התמונה ל־(-1, 3), כאשר -1 מציין ל-Python להתאים את המידות באופן אוטומטי
                                      # לכמות הפיקסלים, ו־3 מציין את הגודל של כל פיקסל (RGB)
    locations = []  # רשימה שבה נשמור את מיקומי הפיקסלים

    # מציבים מיקומי פיקסלים ברשימה
    height, width, _ = image.shape  # מקבלים את גובה ורוחב התמונה
    for y in range(height):
        for x in range(width):
            locations.append((x, y))

    return pixels.tolist(), locations

def tochar(id):

    print(id)
    n_id=int(id)
    char_record = session.query(characther).filter_by(id=n_id).first()
    if char_record is not None:
        return char_record.get_char()
    if char_record is None:
        return " "


print(decode(image_path))

def binary_to_integer(binary_list):
    result = 0
    for digit in binary_list:
        result = result * 2 + int(digit)
    return result
def binary_representation(number):
    if number == 0:
        return [0]
    bits = []
    while number > 0:
        bits.append(number % 2)
        number //= 2
    i=8-len(bits)
    if i>0:
        for i in range(i):
            bits.append(0)
    return bits[::-1]


