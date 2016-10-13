from shared.models import db
from datetime import datetime

class GeneratedTweets(db.Model):
    id = db.Column('id', db.Integer, primary_key = True)
    user = db.Column('user', db.String(100), db.ForeignKey('users.username'))
    tweet = db.Column('tweet', db.String(200))
    date = db.Column('tweet_date', db.DateTime)

    def __init__(self, user, tweet):
        self.user = user
        self.tweet = tweet
        self.date = datetime.today()
