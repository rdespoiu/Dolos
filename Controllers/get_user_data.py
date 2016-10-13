import json
import tweepy

class GetUserData:
    def __init__(self, models, db, api, user):
        self.models = models
        self.db = db
        self.api = api
        self.user = user

    def getUser(self):
        userData = self.api.get_user(id = self.user)._json

        duplicateUser = self.models['Users'].query.filter_by(userid = userData['id']).first()

        if not duplicateUser:
            newUser = self.models['Users'](userData['id'], userData['screen_name'], userData['name'])
            self.db.session.add(newUser)
            self.db.session.commit()
            self.getUserTweets()

        return userData

    def getUserTweets(self):
        userTweets = [item._json for item in tweepy.Cursor(self.api.user_timeline, id = self.user).items()]

        if userTweets:
            for item in userTweets:
                duplicateTweet = self.models['Tweets'].query.filter_by(tweetid = item['id']).first()
                if not duplicateTweet:
                    tweet = self.models['Tweets'](item['id'], item['user']['screen_name'], item['user']['id'], item['text'])
                    self.db.session.add(tweet)
            self.db.session.commit()

        return userTweets
