import os
import cv2
from Entity.Characthers import characther
from Entity.e import getSession

Session = getSession()
session = Session()
def toid(str):
    """
    :param str: A character to check an ID in the database
    :return: id of the character
    """
    char_record=0
    for char in str:
        # מציאת התו במסד הנתונים
        char_record = session.query(characther.id).filter_by(char=char).first()
        if char_record:
            print(f"ID of '{char}': {char_record[0]}")
        else:
            print(f"'{char}' not found in database")
            return 500
    return char_record[0]
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
def binary_to_integer(binary_list):
    """
    :param binary_list: A list of bits that represents a binary number
    :return: The number in decimal representation
    """
    result = 0
    for digit in binary_list:
        result = result * 2 + int(digit)
    return result
def get_file_type(file_path):
    """
    Determines the type of a file based on its extension.
    :param file_path: The path to the file.
    :return: The type of the file (txt, jpeg, jpg, png, pdf, or Unknown if the extension is not recognized).
    """
    # Retrieve the file extension
    file_extension = os.path.splitext(file_path)[1]

    # Arrange the file type based on the extension
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
    """
    Retrieves a character based on its ID.
    :param id: The ID of the character.
    :return: The character corresponding to the ID, or a space if the character is not found.
    """
    print(id)
    n_id = int(id)
    char_record = session.query(characther).filter_by(id=n_id).first()
    if char_record is not None:
        return char_record.get_char()
    if char_record is None:
        return " "

def list_to_number(digits):
    """
    Converts a list of digits into a number.
    :param digits: The list of digits.
    :return: The converted number.
    """
    number = 0
    for digit in digits:
        number = number * 10 + digit
    return number


class Stenography:
    def toid(self,str):
        """
        :param str: A character to check an ID in the database
        :return: id of the character
        """
        char_record = 0
        for char in str:
            # מציאת התו במסד הנתונים
            char_record = session.query(characther.id).filter_by(char=char).first()
            if char_record:
                print(f"ID of '{char}': {char_record[0]}")
            else:
                print(f"'{char}' not found in database")
                return 500
        return char_record[0]

    def process_specific_pixels(self,image_path, start_pixel, end_pixel):
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

    def binary_to_integer(self,binary_list):
        """
        :param binary_list: A list of bits that represents a binary number
        :return: The number in decimal representation
        """
        result = 0
        for digit in binary_list:
            result = result * 2 + int(digit)
        return result

    def get_file_type(self,file_path):
        """
        Determines the type of file based on its extension.
        :param file_path: The path to the file.
        :return: The type of the file (txt, jpeg, jpg, png, pdf, or Unknown if the extension is not recognized).
        """
        # Retrieve the file extension
        file_extension = os.path.splitext(file_path)[1]

        # Arrange the file type based on the extension
        if file_extension == '':
            file_type = 'No extension'
        elif file_extension == '.txt':
            file_type = 'txt'
        elif file_extension == '.jpeg':
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

    def extract_pixels(self,image_path):
        """
        :param image_path:The path to the image
        :return:The list of pixels in the image are represented in RGB
        """
        # קריאת התמונה באמצעות OpenCV
        image = cv2.imread(image_path)

        # יישור התמונה לרשימת פיקסלים
        pixels = image.reshape(
            (-1, 3))  # משנה את הצורה של התמונה ל־(-1, 3), כאשר -1 מציין ל-Python להתאים את המידות באופן אוטומטי
        # לכמות הפיקסלים, ו־3 מציין את הגודל של כל פיקסל (RGB)
        locations = []  # רשימה שבה נשמור את מיקומי הפיקסלים

        # מציבים מיקומי פיקסלים ברשימה
        height, width, _ = image.shape  # מקבלים את גובה ורוחב התמונה
        for y in range(height):
            for x in range(width):
                locations.append((x, y))

        return pixels.tolist(), locations

    def tochar(self,id):
        """
        Retrieves a character based on its ID.
        :param id: The ID of the character.
        :return: The character corresponding to the ID, or a space if the character is not found.
        """
        print(id)
        n_id = int(id)
        char_record = session.query(characther).filter_by(id=n_id).first()
        if char_record is not None:
            return char_record.get_char()
        if char_record is None:
            return " "

    def list_to_number(self,digits):
        """
        Converts a list of digits into a number.
        :param digits: The list of digits.
        :return: The converted number.
        """
        number = 0
        for digit in digits:
            number = number * 10 + digit
        return number
