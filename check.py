# import cv2
# import numpy as np
#
# def read_bit(data):
#     newd = []
#     for i in data:
#         newd.append(format(ord(i), '08b'))
#     return newd
#
# def encode_img(img, data):
#     datalist = read_bit(data)
#     datalen = len(datalist)
#     height, width = img.shape[:2]
#     pix = []
#     for i in range(8 * datalen):
#         pix.append(img[i // width, i % width])
#
#     pix2 = []
#     for i in range(datalen):
#         for j in range(0, 8):
#             if datalist[i][j] == '0':
#                 pix2.append(pix[j] & 254)
#             else:
#                 pix2.append(pix[j] | 1)
#     return pix2
#
# def encode_enc(img, data, start_x, start_y):
#     x, y = start_x, start_y
#     height, width = img.shape[:2]
#     for Pix_val in encode_img(img, data):
#         if x >= width:
#             break
#         img[x, y] = Pix_val
#         x += 1
#         if x == width:
#             x = 0
#             y += 1
#
# def hideMSB1(filename, message, start_x, start_y):
#     img = cv2.imread(filename, cv2.IMREAD_GRAYSCALE)
#     message += '@@'
#     encode_enc(img, message, start_x, start_y)
#     cv2.imwrite("HiddenFiles/Hide-" + filename, img)
#     print("Completed!")
#
# # דוגמה לשימוש:
# hideMSB1(r'C:\Users\ariel\PycharmProjects\pythonProject1\redD.png', "Secret message", 0, 0)
# print(256<<295)
# l=[]
# for i in range(1,359):
#     l.append(i)
#
# print(l)
# str="Ω"
import cv2
import numpy as np

from Entity.Characthers import characther
from Entity.e import getSession


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


# דוגמה לשימוש:
# image_path = r'C:\Users\ariel\PycharmProjects\pythonProject1\redD.png'
image_path = r'C:\Users\ariel\PycharmProjects\pythonProject1\redD.png'

pixels = extract_pixels(image_path)
print("First 10 pixels:", pixels[:10])  # מדפיס את רשימת הפיקסלים של התמונה


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
        new_pixel = [value & 0b00000011 for value in pixel]
        lowest_2_bits_pixels.append(new_pixel)
    # num_rows, num_cols = image.shape[:2]
    # for i, pixel in enumerate(pixels):
    #     row = i // num_cols  # מחלק את האינדקס על מספר העמודות לקבלת השורה
    #     col = i % num_cols  # מחשב את השארית בחלוקת האינדקס על מספר העמודות לקבלת העמודה
    #     print(f"Pixel at row {row}, column {col}")
    return lowest_2_bits_pixels

#pixels = extract_lowest_2_bits(image_path)


print("First 10 pixels:", pixels[:])  # מדפיס את רשימת הפיקסלים של התמונה


# def process_specific_pixels(image_path, start_pixel, end_pixel):
#     # קריאת התמונה באמצעות OpenCV
#     image = cv2.imread(image_path)
#
#     # יישור התמונה לרשימת פיקסלים
#     pixels = image.reshape((-1, 3))
#
#     # עבודה עם פיקסלים מסוימים בטווח שניתן
#     for i in range(start_pixel, end_pixel + 1):
#         pixel = pixels[i]
#         # כאן תוכל להוסיף את העיבוד הרצוי שלך על פיקסל זה
#         print("Pixel", i, ":", pixel)
# process_specific_pixels(image_path,50,80)
Session = getSession()
session = Session()


def toid(str):
    for char in str:
        # מציאת התו במסד הנתונים
        char_record = session.query(characther.id).filter_by(char=char).first()
        if char_record:
            print(f"ID of '{char}': {char_record[0]}")
        else:
            print(f"'{char}' not found in database")
            return 500
    return char_record[0]

def extract_lowest_2_bitsper(pixel):
    # קריאת התמונה באמצעות OpenCV

    # יצירת רשימה חדשה שבה מופיעים רק שני הביטים הנמוכים של כל ערך RGB
    lowest_2_bits_pixels = []
    new_pixel = [value & 0b00000011 for value in pixel]
    lowest_2_bits_pixels.append(new_pixel)
    # num_rows, num_cols = image.shape[:2]
    # for i, pixel in enumerate(pixels):
    #     row = i // num_cols  # מחלק את האינדקס על מספר העמודות לקבלת השורה
    #     col = i % num_cols  # מחשב את השארית בחלוקת האינדקס על מספר העמודות לקבלת העמודה
    #     print(f"Pixel at row {row}, column {col}")
    return lowest_2_bits_pixels
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
    # i=0
    l=[0,0]
    l[0]=L[0]*binary_list[0]+L[1]*binary_list[1]#2
    l[1]=L[2]*binary_list[2]+L[3]*binary_list[3]#1
    # p[2]-=l[0]
    # p[1] -= l[1]
    m=[0,0,0]
    np=extract_lowest_2_bitsper(p)
    m[0]=binary_representation(p[0])
    m[1]=binary_representation(p[1])
    m[2]=binary_representation(p[2])
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
def Decomposing_a_number(id,p,flag):
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

# def create_image_from_pixels(pixels, pixel_locations, image_shape):
#     # יצירת תמונה חדשה בגודל המתאים
#     new_image = np.zeros(image_shape, dtype=np.uint8)
#
#     # השמה של ערכי הפיקסלים לתמונה החדשה בהתאם למיקומם
#     for pixel, location in zip(pixels, pixel_locations):
#         x, y = location
#         new_image[y, x] = pixel
#
#     return new_image
def create_image_from_pixels(pixels, pixel_locations, image_shape):
    # יצירת תמונה חדשה בגודל המתאים
    new_image = np.zeros(image_shape, dtype=np.uint8)

    # השמה של ערכי הפיקסלים לתמונה החדשה בהתאם למיקומם
    for pixel, location in zip(pixels, pixel_locations):
        x, y = location
        new_image[y, x] = pixel

    return new_image


def lsb(str):
    image = cv2.imread(image_path)
    pix,location = extract_pixels(image_path)
    z=0
    loc=[]
    x = []
    j=i=0
    l=len(str)
    while i<len(pix) and j<len(str):
        x.append(pix[i])
        if (i+1)%3==0:
            print(l)
            if (l-1)==0:
                loc = Decomposing_a_number(toid(str[j]), x,[1,0])
                image[location[z][0]][location[z][1]] = loc[0]
                print(z+1)
                print(len(loc))
                print(image[location[z + 1][0]][location[z][1]])
                if len(loc)<3:
                    if len(loc)==1:
                        loc.append(x[1])
                    loc.append(x[2])
                image[location[z + 1][0]][location[z][1]] = loc[1]
                image[location[z + 2][0]][location[z][1]] = loc[2]
                break
            f=False
            if toid(str[j])//10==0 :

                loc=Decomposing_a_number(toid(str[j]), x, [0, 1])
            else:
                loc=Decomposing_a_number(toid(str[j]), x, [1, 1])
            if len(loc) < 3:
                if len(loc) == 1:
                    loc.append(x[1])
                loc.append(x[2])
            image[location[z][0]][location[z][1]] = loc[0]
            image[location[z+1][0]][location[z][1]] = loc[1]

            image[location[z+2][0]][location[z][1]] = loc[2]
            tos=0

            z+=3
            loc.clear()
            j+=1
            l-=1
            x.clear()
        i+=1
    image_shape = (len(pix[0]), len(pix), 3)
    new_image = create_image_from_pixels(pix, location, image.shape)
    cv2.imwrite("modified_image.png", new_image)
    n=cv2.imread("modified_image.png")
    print(n.shape)


lsb("ما يتم حفظه بالفعل")

pixels, pixel_locations = extract_pixels(image_path)
print("Pixel values:", type(pixels))
#print("Pixel locations:", type(pixel_locations))






