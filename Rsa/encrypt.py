import random
from decrypt import decrypt_Text_Rsa
import json

def gcd_extended(a, b):
    if a == 0:
        return {'gcd': b, 'x': 0, 'y': 1}

    gcd_info = gcd_extended(b % a, a)
    x = gcd_info['y'] - (b // a) * gcd_info['x']
    y = gcd_info['x']

    return {'gcd': gcd_info['gcd'], 'x': x, 'y': y}


def find_numbers_with_modulo_one(n):
    pairs = []
    for i in range(10000, n):
        gcd_info = gcd_extended(i, n)
        if gcd_info['gcd'] == 1:
            inverse = (gcd_info['x'] % n + n) % n
            if i > 100 and inverse > 100:
                pairs.append([i, inverse])
                if len(pairs) == 10:
                    return pairs[-1]
    return pairs


def is_prime(number):
    if number <= 1:
        return False
    if number <= 3:
        return True

    if number % 2 == 0 or number % 3 == 0:
        return False

    i = 5
    while i * i <= number:
        if number % i == 0 or number % (i + 2) == 0:
            return False
        i += 6

    return True


def get_random_prime_in_range(start, end):
    prime_found = False
    random_prime=0
    while not prime_found:
        random_prime = random.randint(start, end)
        if is_prime(random_prime):
            prime_found = True

    return random_prime

def createKeys():
    num_one = get_random_prime_in_range(100000, 1000000000)
    num_two = get_random_prime_in_range(100000, 1000000000)
    n = (num_one) * (num_two)
    mult = (num_one - 1) * (num_two - 1)
    return find_numbers_with_modulo_one(mult),n

num_one = get_random_prime_in_range(10000000, 1000000000000)
num_two = get_random_prime_in_range(1000, 1000000000000)
print("end prime")
mult = (num_one - 1) * (num_two - 1)
print(mult)
results = find_numbers_with_modulo_one(mult)
print(results)


def encrypt_Text_Rsa(plaintext):
    keys,n = createKeys()
    cypher_text = []
    for i in plaintext:
        cypher_text.append(pow(ord(i), keys[0], n))
    return cypher_text

def encrypt_Json_Rsa(data, key):
    return bytes([char ^ key for char in data])



from Entity.e import getSession

Session = getSession()
session = Session()


# יצירת המפתחות
keys, n = createKeys()




# update_company_code.py
from flask import Flask, request, jsonify, current_app

app = Flask(__name__)


from decrypt import decrypt_Json_Rsa
# קריאת הקובץ JSON והצפנתו
encrypt_Json_Rsa('aa.json', keys, n)
print("n:"+str(n))
print("key"+str(keys[1]))
decrypt_Json_Rsa("encrypted_aa.json", keys, n)
# app.py

from flask import Flask
from Entity.e import db
from Entity import Company
app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql://postgres:key@localhost:5432/login'
def json_file_to_binary(json_file_path):
    with open(json_file_path, 'r') as file:
        json_data = json.load(file)  # קריאת הנתונים מהקובץ JSON

    # המרת נתוני JSON למחרוזת בתצורת בינארית
    binary_data = json.dumps(json_data).encode('utf-8')

    return binary_data

# איתחול עם עצם היישום של Flask SQLAlchemy
db.init_app(app)



def update_code_for_company(binary_data):
    
    company = session.query(Company).filter(Company.id == 1).one()
    if company:
        company.code = binary_data
        session.commit()
        print('Code updated successfully for company with id 1')
    else:
        print('Company with id 1 not found')

json_file_path = 'encrypted_aa.json'  # שינה זאת לנתיב המדויק של קובץ ה-JSON שלך
binary_data = json_file_to_binary(json_file_path)
update_code_for_company(binary_data)




# דוגמה לשימוש:



# sentences = [
#     "The sun is shining brightly today.",
#     "I love walking in the rain.",
#     "She plays the piano beautifully.",
#     "He enjoys reading mystery novels.",
#     "My favorite color is blue.",
#     "We went hiking in the mountains last weekend.",
#     "The cat is sleeping on the couch.",
#     "Learning a new language can be challenging but rewarding.",
#     "Coffee is my morning ritual.",
#     "The flowers in the garden are blooming.",
#     "Music has a powerful effect on our emotions.",
#     "The sky is clear and the stars are shining.",
#     "I enjoy spending time with my family.",
#     "Cooking is a relaxing activity for me.",
#     "The children are playing in the park.",
#     "Exercise is important for maintaining good health.",
#     "She is studying hard for her exams.",
#     "Reading books expands your knowledge.",
#     "We are planning a trip to Europe next summer.",
#     "The birds are chirping outside my window.",
#     "I prefer tea over coffee.",
#     "He is passionate about environmental conservation.",
#     "The movie we watched last night was fantastic.",
#     "Time flies when you're having fun.",
#     "She is wearing a beautiful dress to the party.",
#     "The beach is my favorite place to relax.",
#     "Dogs are loyal companions.",
#     "Mathematics is a fascinating subject.",
#     "I need to buy groceries after work.",
#     "The sunset looks breathtaking from here.",
#     "She is talented at playing the guitar.",
#     "Laughter is the best medicine.",
#     "The city lights are dazzling at night.",
#     "Reading poetry soothes the soul.",
#     "He is a talented artist.",
#     "Science fiction movies are my favorite genre.",
#     "I love exploring new places.",
#     "She has a great sense of humor.",
#     "The smell of fresh bread baking is heavenly.",
#     "We are going camping next weekend.",
#     "Learning to cook is an important life skill.",
#     "The sound of rain is calming.",
#     "He is a skilled carpenter.",
#     "The museum exhibits were fascinating.",
#     "She has a beautiful singing voice.",
#     "Walking barefoot in the grass feels wonderful.",
#     "I enjoy watching documentaries about nature.",
#     "Gardening is a therapeutic activity.",
#     "The moonlight reflects off the water.",
#     "He is a dedicated teacher.",
#     "The aroma of coffee fills the room.",
#     "Yoga helps me relax and unwind.",
#     "She is passionate about helping others.",
#     "The sound of waves crashing on the shore is soothing.",
#     "He is a talented chef.",
#     "Spending time outdoors improves my mood.",
#     "The scent of flowers fills the air.",
#     "She is an avid reader.",
#     "The stars are twinkling in the night sky.",
#     "Writing poetry is a creative outlet.",
#     "The sound of birds chirping wakes me up in the morning.",
#     "He enjoys playing soccer with his friends.",
#     "The smell of freshly cut grass reminds me of summer.",
#     "Painting allows me to express myself artistically.",
#     "She is a dedicated volunteer at the local shelter.",
#     "The fresh air in the countryside is invigorating.",
#     "He is passionate about photography.",
#     "Watching a movie marathon is a fun way to spend the weekend.",
#     "She is a skilled dancer.",
#     "The sound of children laughing is contagious.",
#     "Reading a good book is like escaping to another world.",
#     "He enjoys solving puzzles in his free time.",
#     "The smell of rain on the pavement is nostalgic.",
#     "Cycling through the countryside is a peaceful activity.",
#     "She is a talented pianist.",
#     "The sound of thunder in the distance is ominous.",
#     "Cooking a homemade meal from scratch...",
#     # Add more sentences as needed
# ]
# for i in sentences:
#     flag=encryptRsa(i)==i
#     if not flag:
#         print("errrrrr")
#         break
#     print(i)
plaintext = "abcdefghijklmnop"
encrypt_Text_Rsa(plaintext)
# plaintext = "אריאל"
e,n,keys=encrypt_Text_Rsa(plaintext)
print(decrypt_Text_Rsa(e,keys[1],n))



