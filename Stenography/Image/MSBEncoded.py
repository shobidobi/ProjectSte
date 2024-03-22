import cv2
import numpy as np
from Entity.Characthers import characther
from Entity.e import getSession

image_path = r'C:\Users\ariel\PycharmProjects\pythonProject1\redD.png'
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

def ret_pixel(id,p):
    """

    :param digit: the digit to insert
    :param p: list of pixel values
    :return: the updated pixel
    """
    delta=[0,0,0]
    for i in range(3):
        delta[i]=p[0][i]-p[1][i]
        if id !=0:
            digit=id%10
            delta[i]-=digit
            id=id//10
    p[0][0]+=delta[0]
    p[0][1]+=delta[1]
    p[0][2]+=delta[2]

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
    return p


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
def Decomposing_a_number(id,p,flag):
    """
    :param id: The number identifier in the database
    :param p: the list of three pixel from the image
    :param flag: A flag to mark the current state
    :return: The updated list of pixels after encryption
    """
    i=0
    x=[]
    while id>0:
        digit = id % 10
        if id//10==0:
            print(p[i])
            flag[0]=0
            x.append(ret_pixel(digit, p))
            print("-----"+str(x))
            break
        print(p[i])
        x.append(ret_pixel(digit, p))
        print(x)
        id = int(id/10)
        i+=1
    return x

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

def pvd(str,image_path):
    """
    The main encryption function at the end of the function saves the information in the copy
    :param str:The string to encrypt
    :param image_path:The path to the image where the information will be encrypted
    """
    str+=SOF
    image = cv2.imread(image_path)
    pix,location = extract_pixels(image_path)
    index_in_pixels=0
    x = []
    j=i=0
    l=len(str)
    lis=[]
    while i<len(pix) and j<len(str):
        x.append(pix[i])
        if (i+1)%3==0:
            lis.append(x)
        if (i+1)%6==0:
            list_of_six_pixels=ret_pixel(toid(str[j]),lis)

            #השמת ערכים
            image[location[index_in_pixels][0]][location[index_in_pixels][1]] = list_of_six_pixels[0][0]
            image[location[index_in_pixels+1][0]][location[index_in_pixels][1]] = list_of_six_pixels[0][1]
            image[location[index_in_pixels+2][0]][location[index_in_pixels][1]] = list_of_six_pixels[0][2]
            index_in_pixels+=3
            image[location[index_in_pixels][0]][location[index_in_pixels][1]] = list_of_six_pixels[1][0]
            image[location[index_in_pixels +1][0]][location[index_in_pixels][1]] = list_of_six_pixels[1][1]
            image[location[index_in_pixels + 2][0]][location[index_in_pixels][1]] = list_of_six_pixels[1][2]
            index_in_pixels += 3
            #------------------------------------------------------
            list_of_six_pixels.clear()
            lis.clear()
            j+=1
            l-=1
            x.clear()
        i+=2
    new_image = create_image_from_pixels(pix, location, image.shape)
    cv2.imwrite("modified_image.png", new_image)
    n=cv2.imread("modified_image.png")
