# models.py
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from datetime import datetime

db = SQLAlchemy()

def getengine():
    url=f'postgresql://postgres:password@localhost:5432/login'
    engine = create_engine(url,pool_size=50,echo=False)
    return engine
engine=getengine()
def getSession():
    Session = sessionmaker(bind=engine)
    return Session












###########################################################

# app = Flask(__name__)
# app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql://postgres:password@localhost/login'
# db.init_app(app)
#
# if __name__ == "__main__":
#     with app.app_context():
#         db.create_all()
#     app.run(debug=True)
