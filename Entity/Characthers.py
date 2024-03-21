from Entity.e import db


class characther(db.Model):
    id = db.Column(db.Integer, primary_key=True, autoincrement=True, nullable=False, unique=True)
    char = db.Column(db.String(50), nullable=False)

    def __init__(self, char):
        self.char = char

    def get_char(self):
        return self.char

    def set_char(self, char):
        self.char = char

    def get_id(self):
        return self.id
