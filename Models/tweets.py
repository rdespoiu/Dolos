from shared.models import db

class Tweets(db.Model):
    tweetid = db.Column('tweet_id', db.String(100), primary_key = True)
    username = db.Column('username', db.String(100), db.ForeignKey('users.username'))
    userid = db.Column('userid', db.String(100), db.ForeignKey('users.userid'))
    text = db.Column('text', db.String(140))

    def __init__(self, tweetid, username, userid, text):
        self.tweetid = tweetid
        self.username = username
        self.userid = userid
        self.text = text
