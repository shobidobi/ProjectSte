class UserViewObject:
    def __init__(self, username, user_id, access_key, company_number):
        self.username = username
        self.user_id = user_id
        self.access_key = access_key
        self.company_number = company_number

    def to_dict(self):
        return {
            'username': self.username,
            'user_id': self.user_id,
            'access_key': self.access_key,
            'company_number': self.company_number
        }

    @classmethod
    def from_dict(cls, data):
        return cls(
            data['username'],
            data['user_id'],
            data['access_key'],
            data['company_number']
        )

    def get_username(self):
        return self.username

    def get_user_id(self):
        return self.user_id

    def get_access_key(self):
        return self.access_key

    def get_company_number(self):
        return self.company_number

    def set_username(self, username):
        self.username = username

    def set_user_id(self, user_id):
        self.user_id = user_id

    def set_access_key(self, access_key):
        self.access_key = access_key

    def set_company_number(self, company_number):
        self.company_number = company_number



    def toJSON(self):
        return {
            'username': self.username,
            'user_id': self.user_id,
            'access_key': self.access_key,
            'company_number': self.company_number
        }
# דוגמה לשימוש במחלקה:
# יצירת אובייקט מודל
user_view_object = UserViewObject('JohnDoe', 123456, 'abc123', '789')

# השגת פרטים על ידי פונקציות המאחזרות
print(user_view_object.get_username())  # 'JohnDoe'
print(user_view_object.get_user_id())  # 123456
print(user_view_object.get_access_key())  # 'abc123'
print(user_view_object.get_company_number())  # '789'

# עדכון פרטים על ידי פונקציות הקובעות
user_view_object.set_username('JaneDoe')
user_view_object.set_user_id(654321)
user_view_object.set_access_key('xyz789')
user_view_object.set_company_number('987')

# הדפסת הפרטים לאחר העדכון
print(user_view_object.to_dict())
