from Entity.e import db
class Users(db.Model):
    id = db.Column(db.Integer, primary_key=True, autoincrement=True, nullable=False, unique=True)
    user_name = db.Column(db.String(50), nullable=False)
    email = db.Column(db.String(120), nullable=False, unique=True)
    id_company = db.Column(db.Integer, db.ForeignKey('company.id'))
    is_change_company_code=db.Column(db.Boolean, default=False)
    def __init__(self, user_name, email, id_company):
        self.user_name = user_name
        self.email = email
        self.id_company = id_company

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

    def set_is_change_company_code(self, new_is_change_company_code):
        self.is_change_company_code=new_is_change_company_code

    def get_is_change_company_code(self):
        return self.is_change_company_code
