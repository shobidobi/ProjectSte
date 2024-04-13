from datetime import datetime

from Entity.e import db


class Passwords(db.Model):

    user_id = db.Column(db.Integer,db.ForeignKey('users.id'),primary_key=True, nullable=False)
    password = db.Column(db.String(255),primary_key=True, nullable=False)
    date_c = db.Column(db.DateTime,primary_key=True, nullable=False, default=datetime.utcnow)

    def __init__(self, user_id, password):
        self.user_id = user_id
        self.password = password
    def set_password(self, password):
        self.password = password

    def get_password(self):
        return self.password
    def __set_date_c(self):
        self.date_c = datetime.utcnow()
    def get_date_c(self):
        return self.date_c
    def get_user_id(self):
        return self.user_id
    def set_user_id(self, user_id):
        self.user_id = user_id
