from flask import Flask
from flask_sqlalchemy import SQLAlchemy
import json

from Entity.e import getSession

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql://postgres:password@localhost:5432/login'
db = SQLAlchemy(app)

# Define the Company model
class Company(db.Model):
    __tablename__ = 'company'

    id = db.Column(db.Integer, primary_key=True)
    company_name = db.Column(db.String(50))
    code_image = db.Column(db.LargeBinary)
    code_audio = db.Column(db.LargeBinary)

    def __init__(self, company_name: object, code_image: object, code_audio: object):
        self.company_name = company_name
        self.code_audio =code_audio
        self.code_image =code_image
    def get_company_name(self):
        return self.company_name
    def get_code_audio(self):
        return self.code_audio
    def get_code_image(self):
        return self.code_image
    def set_code_image(self, code_image):
        self.code_image = code_image
    def set_code_audio(self, code_audio):
        self.code_audio = code_audio
    def set_company_name(self, company_name):
        self.company_name = company_name


# Function to change company code
def change_code(company_id, data):
    with app.app_context():
        try:
            company = Company.query.get(company_id)
            if company:
                for item in data:
                    if 'companyNumber' in item:
                        # Update company number
                        company.company_name = item['companyNumber']
                    elif 'algorithmType' in item:
                        # Update algorithm type
                        company.code = bytes(item['algorithmType'])
                db.session.commit()
                return {'message': 'Code updated successfully'}
            else:
                return {'message': 'Company not found'}
        except Exception as e:
            return {'message': f'Error: {str(e)}'}

from flask import jsonify
from sqlalchemy.orm import sessionmaker
from Entity.e import getSession
# Function to get the number of rows in the company table
def get_company_count():
    Session = getSession()
    session = Session()
    try:
        count = session.query(Company).count()
        session.close()
        return count
    except Exception as e:
        session.close()
        return {'message': f'Error: {str(e)}'}

# Function to add a new company
from sqlalchemy.exc import SQLAlchemyError

# Function to add a new company
def add_company(company_name):
    print("adding company")
    Session = getSession()
    session = Session()
    try:
        new_company = Company(company_name=company_name, code_audio=b'', code_image=b'')
        session.add(new_company)
        session.commit()
        session.close()
        return {'message': 'Company added successfully'}
    except SQLAlchemyError as e:
        session.rollback()
        session.close()
        return {'message': f'Error: {str(e)}'}



