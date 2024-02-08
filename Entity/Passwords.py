from datetime import datetime

from Entity.e import db


class Password(db.Model):
    password = db.Column(db.String(80), nullable=False)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'))
    date_c = db.Column(db.DateTime, nullable=False, default=datetime.utcnow)
    def set_password(self, password):
        self.password =password

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

