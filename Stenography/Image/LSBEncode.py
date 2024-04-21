import os

import cv2
import numpy as np
from Entity.Characthers import characther
from Entity.e import getSession

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


# image_path = r'C:\Users\ariel\PycharmProjects\pythonProject1\redD.png'
Session = getSession()
session = Session()

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

def ret_pixel(digit,p,flag):
    """

    :param digit: the digit to insert
    :param p: list of pixel values
    :param flag: describes the encryption
    :return: the updated pixel
    """

    binary_string = bin(digit)[2:]  # המרת המספר לבינארי והוצאת הספרה '0b' הראשונה
    binary_list = [int(digit) for digit in binary_string]  # המרת המחרוזת הבינארית לרשימה של ספרות בינאריות
    binary_list.reverse()
    c=4-len(binary_list)
    for i in range(0,c):
        binary_list.append(0)
    L=[1,2,4,8]
    l=[0,0]
    l[0]=L[0]*binary_list[0]+L[1]*binary_list[1]#2
    l[1]=L[2]*binary_list[2]+L[3]*binary_list[3]#1
    m=[0,0,0]
    for i in range(0,3):
        m[i] = binary_representation(p[i])
    m[2][7]=binary_list[0]
    m[2][6] = binary_list[1]
    m[1][7] = binary_list[2]
    m[1][6] = binary_list[3]
    m[0][7]=flag[0]
    m[0][6]=flag[1]
    p[0]=binary_to_integer(m[0])
    p[1]=binary_to_integer(m[1])
    p[2]=binary_to_integer(m[2])
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
            x.append(ret_pixel(digit,p[i],[0,flag[1]]))
            print("-----"+str(x))
            break
        print(p[i])
        x.append(ret_pixel(digit,p[i],flag))
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
def get_file_type(file_path):
    # משיגים את סיומת הקובץ
    file_extension = os.path.splitext(file_path)[1]

    # מסודרים את הסוג של הקובץ לפי הסיומת
    if file_extension == '':
        file_type = 'No extension'
    elif file_extension == '.txt':
        file_type = 'txt'
    elif  file_extension == '.jpeg':
        file_type = 'jpeg'
    elif file_extension == '.jpg':
        file_type = 'jpg'
    elif file_extension == '.png':
        file_type = 'png'
    elif file_extension == '.pdf':
        file_type = 'pdf'
    else:
        file_type = 'Unknown'

    return file_type
def lsb(str,image_path,range_pixel):
    """
    The main encryption function at the end of the function saves the information in the copy
    :param str:The string to encrypt
    :param image_path:The path to the image where the information will be encrypted
    """
    image = cv2.imread(image_path)
    # pix,location = extract_pixels(image_path)
    pix,location=process_specific_pixels(image_path,range_pixel[0],range_pixel[1])
    index_in_pixels=0
    x = []
    j=i=0
    l=len(str)
    while i<len(pix) and j<len(str):
        x.append(pix[i])
        if (i+1)%3==0:
            print(l)
            if (l-1)==0:
                list_of_three_pixels = Decomposing_a_number(toid(str[j]), x,[1,0])
                image[location[index_in_pixels][0]][location[index_in_pixels][1]] = list_of_three_pixels[0]
                print(index_in_pixels+1)
                print(len(list_of_three_pixels))
                print(image[location[index_in_pixels + 1][0]][location[index_in_pixels][1]])
                if len(list_of_three_pixels)<3:
                    if len(list_of_three_pixels)==1:
                        list_of_three_pixels.append(x[1])
                    list_of_three_pixels.append(x[2])
                image[location[index_in_pixels + 1][0]][location[index_in_pixels][1]] = list_of_three_pixels[1]
                image[location[index_in_pixels + 2][0]][location[index_in_pixels][1]] = list_of_three_pixels[2]
                break
            f=False
            if toid(str[j])//10==0 :

                list_of_three_pixels=Decomposing_a_number(toid(str[j]), x, [0, 1])
            else:
                list_of_three_pixels=Decomposing_a_number(toid(str[j]), x, [1, 1])
            if len(list_of_three_pixels) < 3:
                if len(list_of_three_pixels) == 1:
                    list_of_three_pixels.append(x[1])
                list_of_three_pixels.append(x[2])
            image[location[index_in_pixels][0]][location[index_in_pixels][1]] = list_of_three_pixels[0]
            image[location[index_in_pixels+1][0]][location[index_in_pixels][1]] = list_of_three_pixels[1]
            image[location[index_in_pixels+2][0]][location[index_in_pixels][1]] = list_of_three_pixels[2]
            index_in_pixels+=3
            list_of_three_pixels.clear()
            j+=1
            l-=1
            x.clear()
        i+=1
    print("sof steno")
    new_image = create_image_from_pixels(pix, location, image.shape)
    type_file=get_file_type(image_path)
    print(type_file)
    mod_path="C:\\Users\\ariel\PycharmProjects\pythonProject1\image_c\modified_image"+"."+type_file
    print(mod_path)
    cv2.imwrite(mod_path,new_image)

#lsb("ariel",r"C:\Users\ariel\PycharmProjects\pythonProject1\redD.png",[50,80])