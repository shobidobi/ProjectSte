
from Entity.e import db


class Keys(db.Model):

    user_id = db.Column(db.Integer,db.ForeignKey('users.id'),primary_key=True, nullable=False)
    key = db.Column(db.Integer, nullable=False)

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
        existing_key = Keys.query.filter_by(user_id=user_id).first()

        # אם המפתח כבר קיים, נעדכן אותו
        if existing_key:
            existing_key.key = key
        # אם המפתח לא קיים, ניצור שורה חדשה
        else:
            new_key = Keys(user_id=user_id, key=key)
            db.session.add(new_key)

        db.session.commit()

