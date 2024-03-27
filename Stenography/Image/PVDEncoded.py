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
        elif str==" ":
            return 500
        else:
            print(f"'{char}' not found in database")
    return char_record[0]

def ret_pixel(id, p):
    """
    :param id: the digit to insert
    :param p: list of pixel values, where each pixel value is a list of RGB values
    :return: the updated pixel
    """
    delta = [0, 0, 0]
    for i in range(3):  # Assuming RGB values
        # Assuming p is a list of lists where each inner list represents RGB values
        delta[i] = p[1][i] - p[0][i]  # Subtract corresponding RGB values
        if id != 0:
            digit = id % 10
            delta[i]-=digit
            id = id // 10
    # Update the pixel values
    p[0][0] += delta[0]
    p[0][1] += delta[1]
    p[0][2] += delta[2]

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
        if (i+1)%2==0:
            lis=x
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
            list_of_six_pixels.clear()
            lis.clear()
            j+=1
            l-=1
            x.clear()
        i+=1
    new_image = create_image_from_pixels(pix, location, image.shape)
    cv2.imwrite("modified_image.png", new_image)
    n=cv2.imread("modified_image.png")
pvd("הקוד עובד",image_path)