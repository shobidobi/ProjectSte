from flask import Flask
from flask_sqlalchemy import SQLAlchemy
import json

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

    def __init__(self, company_name, code):
        self.company_name = company_name
        self.code = code
    def get_company_name(self):
        return self.company_name
    def get_code_audio(self):
        return self.code_audio
    def get_code_image(self):
        return self.code_image

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


