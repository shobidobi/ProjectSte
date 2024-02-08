from datetime import datetime

from Entity.e import db


class TryLogin(db.Model):
    user_name = db.Column(db.String(50), nullable=False)
    password = db.Column(db.String(80), nullable=False)
    date = db.Column(db.DateTime, nullable=False, default=datetime.utcnow)
    valid = db.Column(db.Boolean)
    def __init__(self, user_name, password):
        self.user_name = user_name
        self.password=password
        self.date =datetime.utcnow()
        self.valid = True

    def set_password(self, password):
        self.password =password
    def get_password(self):
        return self.password
    def set_user_name(self, user_name):
        self.user_name =user_name
    def get_user_name(self):
        return self.user_name
    def get_valid(self):
        return self.valid
    def get_date(self):
        return self.date