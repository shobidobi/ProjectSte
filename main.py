# connection = psycopg2.connect(
#     host="localhost", port="5432", database="master", user="postgres", password="123456")
from Stenography.Image.LSBDecoded import decode_lsb
if __name__ == "__main__":
    # connect()
    # encode_lsb(r"C:\Users\ariel\PycharmProjects\pythonProject1\1-red.png", "hey my name is red", "redD.png")
    decoded_data = decode_lsb(r"C:\Users\ariel\PycharmProjects\pythonProject1\redD.png")
    print(decoded_data)

