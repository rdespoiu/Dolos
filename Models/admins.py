from shared.models import db
from Utility.generatehash import generateHash, generateSalt

class Admins(db.Model):
    id = db.Column('admin_id', db.Integer, primary_key = True)
    username = db.Column('username', db.String(20), unique = True)
    password = db.Column('password', db.String(128))
    salt = db.Column('salt', db.String(32))

    def __init__(self, username, password):
        self.salt = generateSalt()
        self.username = username
        self.password = generateHash(self.salt, password)
