from Entity.e import db
from e import getSession
class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    user_name = db.Column(db.String(50), nullable=False)
    email = db.Column(db.String(120), nullable=False, unique=True)
    id_company = db.Column(db.Integer, db.ForeignKey('company.id'))
    def set_email(self, new_email):
        self.email = new_email

    def get_email(self):
        return self.email

    def set_username(self, new_username):
         self.user_name = new_username

    def get_username(self):
        return self.user_name

    def set_id_company(self, new_id):
        self.id_company = new_id

    def get_id_company(self):
        
        return self.id_company
    def get_id(self):
        return self.id
