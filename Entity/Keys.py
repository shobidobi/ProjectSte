from Entity.e import db
from Entity.e import getSession

class Keys(db.Model):
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'), primary_key=True, nullable=False)
    key = db.Column(db.ARRAY(db.Integer), nullable=False)
    key = db.Column(db.ARRAY(db.BigInteger), nullable=False)

    def __init__(self, user_id, key):
        self.user_id = user_id
        self.key = key

    def set_key(self, key):
        self.key = key

    def get_key(self):
        return self.key

    def get_user_id(self):
        return self.user_id

    def set_user_id(self, user_id):
        self.user_id = user_id

def update_or_create_key(user_id, key):
    Session = getSession()
    session = Session()

    existing_key = session.query(Keys).filter_by(user_id=user_id).first()

    # אם המפתח כבר קיים, נעדכן אותו
    if existing_key:
        existing_key.key = key
    # אם המפתח לא קיים, ניצור שורה חדשה
    else:
        new_key = Keys(user_id=user_id, key=key)
        session.add(new_key)

    session.commit()

def get_key_by_user_id(user_id):
    Session = getSession()
    session = Session()

    key_object = session.query(Keys).filter_by(user_id=user_id).first()
    if key_object:
        return key_object.key
    else:
        return None
