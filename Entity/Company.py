from Entity.e import db


class Company(db.Model):
    id = db.Column(db.Integer, primary_key=True, autoincrement=True, nullable=False, unique=True)
    company_name = db.Column(db.String(50), nullable=False)
    def __init__(self, company_name):
        self.company_name = company_name
    def get_company_name(self):
        return self.company_name
    def set_company_name(self, company_name):
        self.company_name = company_name
    def get_id(self):
        return self.id