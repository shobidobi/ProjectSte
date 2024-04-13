from flask import Flask
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql://username:key@localhost:5432/login'
db = SQLAlchemy(app)

# הגדרת המודל Company
class Company(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    company_name = db.Column(db.String(50))
    code = db.Column(db.LargeBinary)
    def __init__(self, company_name, code):
        self.company_name = company_name
        self.code = code



