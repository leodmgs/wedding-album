import datetime
from app.main.database import DB


class User(object):

    def __init__(self, name, email, password, access_level=0):
        self.name = name
        self.email = email
        self.password = password
        self.access_level = access_level
        self.created_at = datetime.datetime.utcnow()

    def insert(self):
        result = DB.insert("users", data=self.json())
        if result.inserted_id:
            return True
        return False

    def json(self):
        return {
            'name': self.name,
            'email': self.email,
            'password': self.password,
            'access_level': self.access_level,
            'created_at': self.created_at
        }
