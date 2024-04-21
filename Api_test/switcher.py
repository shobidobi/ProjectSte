from Stenography.Image.LSBEncode import lsb
from Stenography.Image.LSBDecoded import decode as lsb_decoded
from Stenography.Image.MSBEncoded import encode as msb_encode
from Stenography.Image.MSBDecoded import decode as msb_decoded
from Stenography.Image.PVDEncoded import pvd as pvd_encoded
from Stenography.Image.PVDDecoded import pvd as pvd_decoded
from Stenography.Audio.LSBEncodedA import encode as lsb_encode_a
from Stenography.Audio.LSBDncodedA import decode as lsb_decode_a
from Stenography.Audio.MSBEecodedA import encode as msb_encode_a
from Stenography.Audio.MSBDecodedA import decode as msb_decode_a
def switch_code(company_number,algorithm_type,pixel_range,file_type,mode,text,path):
    if algorithm_type=='LSB':
        if file_type=='image':
            if mode=='encode':
                return lsb(text,image_path=path,range_pixel=[pixel_range[0],pixel_range[1]]),algorithm_type
            else:
                return lsb_decoded(image_path=path,range_pix=[pixel_range[0],pixel_range[1]]),algorithm_type
        else:
            if mode=='encode':
                return lsb_encode_a(audio_file=path,message=text),algorithm_type
            else:
                return lsb_decode_a(audio='')
    if algorithm_type=='MSB':
        if file_type=='image':
            if mode=='encode':
                print(text)
                return msb_encode(text,image_path=path,range_pixel=[pixel_range[0],pixel_range[1]]),algorithm_type
            else:
                print("msb decode........")
                return msb_decoded(image_path=path,range_pixel=[pixel_range[0],pixel_range[1]]),algorithm_type
        else:
            if mode=='encode':
                return msb_encode_a(audio_file='',message=text),algorithm_type
            else:
                return msb_decode_a(audio=''),algorithm_type
    if algorithm_type=='PVD':
        if file_type=='image':
            if mode=='encode':
                return pvd_encoded(text,image_path=path,range_pixel=[pixel_range[0],pixel_range[1]+30]),algorithm_type
            else:
                return pvd_decoded(image_path=path),algorithm_type


import json


# def extract_fields_from_json(json_file,mode,text,user_id):
#     # פתיחת הקובץ והקריאה שלו
#     with open(json_file, 'r') as f:
#         data = json.load(f)
#
#     # חילוץ השדות מהמבנה ה-JSON
#     company_number = data.get("companyNumber")
#     algorithm_type = data.get("algorithmType")
#     pixel_range = data.get("pixelRange")
#     file_type = data.get("fileType")
#     switch_code(company_number,algorithm_type,pixel_range,file_type,mode,text)
#     # החזרת השדות
#     return company_number, algorithm_type, pixel_range, file_type
#
#
# # ניתן להשתמש בפונקציה כך:
# json_file = r"C:\Users\ariel\PycharmProjects\pythonProject1\Rsa\aa.json"  # שינה את זה לנתיב של הקובץ האמיתי
# company_number, algorithm_type, pixel_range, file_type = extract_fields_from_json(json_file)
#
# print("Company Number:", company_number)
# print("Algorithm Type:", algorithm_type)
# print("Pixel Range:", pixel_range)
# print("File Type:", file_type)
#
# def write_to_file(company_number, private_key):
#     with open("company_data.txt", "a") as f:
#         f.write(f"Company Number: {company_number}, Private Key: {private_key}\n")
#
# # לדוגמה:
# write_to_file(12345, "abc123")
# write_to_file(67890, "xyz789")
# def find_private_key(company_number):
#     with open("company_data.txt", "r") as f:
#         for line in f:
#             data = line.split(", ")
#             num = data[0].split(": ")[1]
#             if int(num) == company_number:
#                 private_key = data[1].split(": ")[1].strip()
#                 return private_key
#     return None
#
# # לדוגמה:
# company_number = 12345
# private_key = find_private_key(company_number)
# if private_key:
#     print(f"The private key for company number {company_number} is: {private_key}")
# else:
#     print(f"No private key found for company number {company_number}")
