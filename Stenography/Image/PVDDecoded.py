import cv2
import numpy as np
from Entity.Characthers import characther
from Entity.e import getSession

Session = getSession()
session = Session()
SOF="Ω"

def extract_pixels(image_path):
    """
    :param image_path:The path to the image
    :return:The list of pixels in the image are represented in RGB
    """
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
    n_id=int(id)
    char_record = session.query(characther).filter_by(id=n_id).first()
    if char_record is not None:
        return char_record.get_char()
    if id==500:
        return " "
    if id>369 or id<1:
        return ""

def ret_id(p):

    """

    :param digit: the digit to insert
    :param p: list of pixel values
    :return: the updated pixel
    """
    delta = [0, 0, 0]
    for i in range(3):
        delta[i] = p[1][i] - p[0][i]
    id_c=delta[0]*1 + delta[1]*10 + delta[2]*100
    # binary_string = bin(digit)[2:]  # המרת המספר לבינארי והוצאת הספרה '0b' הראשונה
    # binary_list = [int(digit) for digit in binary_string]  # המרת המחרוזת הבינארית לרשימה של ספרות בינאריות
    # binary_list.reverse()
    # c=4-len(binary_list)
    # for i in range(0,c):
    #     binary_list.append(0)
    # L=[1,2,4,8]
    # l=[0,0]
    # l[0]=L[0]*binary_list[0]+L[1]*binary_list[1]#2
    # l[1]=L[2]*binary_list[2]+L[3]*binary_list[3]#1
    # m=[0,0,0]
    # m[0]=binary_representation(p[0])
    # m[1]=binary_representation(p[1])
    # m[2]=binary_representation(p[2])
    # m[2][7]=binary_list[0]
    # m[2][6] = binary_list[1]
    # m[1][7] = binary_list[2]
    # m[1][6] = binary_list[3]
    # m[0][7]=flag[0]
    # m[0][6]=flag[1]
    # p[0]=binary_to_integer(m[0])
    # p[1]=binary_to_integer(m[1])
    # p[2]=binary_to_integer(m[2])
    return id_c


def binary_to_integer(binary_list):
    """
    :param binary_list: A list of bits that represents a binary number
    :return: The number in decimal representation
    """
    result = 0
    for digit in binary_list:
        result = result * 2 + int(digit)
    return result
def binary_representation(number):
    """
    :param number: A number in decimal representation
    :return: The number in binary representation
    """
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

def create_image_from_pixels(pixels, pixel_locations, image_shape):
    """
    :param pixels: The list of pixels
    :param pixel_locations:The locations of the pixels in the image
    :param image_shape: Image size
    :return:The image with the updated pixels
    """
    # יצירת תמונה חדשה בגודל המתאים
    new_image = np.zeros(image_shape, dtype=np.uint8)

    # השמה של ערכי הפיקסלים לתמונה החדשה בהתאם למיקומם
    for pixel, location in zip(pixels, pixel_locations):
        x, y = location
        new_image[y, x] = pixel

    return new_image
def process_specific_pixels(image_path, start_pixel, end_pixel):
    """

    :param image_path: The path to the image
    :param start_pixel: index of the starting
    :param end_pixel: index of the ending
    :return: list of pixels in the image are represented in RGB with locations
    """
    # קריאת התמונה באמצעות OpenCV
    image = cv2.imread(image_path)

    # יישור התמונה לרשימת פיקסלים
    pixels = image.reshape((-1, 3))

    # רשימה ריקה לאחסון הפיקסלים
    processed_pixels = []

    # רשימה ריקה לאחסון המיקומים של הפיקסלים
    pixel_positions = []

    # עבודה עם פיקסלים מסוימים בטווח שניתן
    for i in range(start_pixel, end_pixel + 1):
        pixel = pixels[i]

        # הוספת הפיקסל לרשימה
        processed_pixels.append(pixel)

        # חישוב המיקום של הפיקסל בתמונה והוספתו לרשימה
        position = (i // image.shape[1], i % image.shape[1])
        pixel_positions.append(position)

    return processed_pixels, pixel_positions

def pvd(image_path):
    """
    The main encryption function at the end of the function saves the information in the copy
    :param str:The string to encrypt
    :param image_path:The path to the image where the information will be encrypted
    """
    str=""
    pix,location = extract_pixels(image_path)
    #pix, location=process_specific_pixels(image_path,50,110)
    i=0
    lis_of_six=[]
    while i<len(pix)-1:
        lis_of_six.append(pix[i])
        i+=1
        lis_of_six.append(pix[i])
        c=tochar(ret_id(lis_of_six))

        if c== "Ω":
            return str
        str+=tochar(ret_id(lis_of_six))
        lis_of_six.clear()
        i+=1


image_path = r'C:\Users\ariel\PycharmProjects\pythonProject1\image_c\modified_image.png'
print(pvd(image_path))