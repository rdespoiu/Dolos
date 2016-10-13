from shared.models import db

class Users(db.Model):
    userid = db.Column('userid', db.String(100), primary_key = True)
    username = db.Column('username', db.String(100), primary_key = True)
    displayname = db.Column('displayname', db.String(100))

    def __init__(self, userid, username, displayname):
        self.userid = userid
        self.username = username
        self.displayname = displayname
