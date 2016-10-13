import json
import tweepy
from random import choice, randint
from MarkovChain.dolos import Dolos

class CreateTweet:
    genericTweets = {
        #'instructions': 'Want a reply from @DolosBot? Send me a tweet with a celebrity\'s handle! Example: @DolosBot realDonaldTrump',
        'information':  'Interested in seeing how @DolosBot works? Check out the source code at https://github.com/rdespoiu/Dolos'
    }
    def __init__(self, models, db, api, depth, user = None):
        self.models = models
        self.db = db
        self.api = api
        self.depth = depth
        self.user = user

    def generateTweet(self, tweets, user):
        markovGen = Dolos(tweets, self.depth, user)
        return markovGen.generateTweet()

    def postTweet(self):
        dbTweet = None
        tweet = None

        if self.user:
            tweets = [tweet.text for tweet in self.models['Tweets'].query.filter(self.models['Tweets'].username == self.user)]
            tweet = self.generateTweet(tweets, self.user)
            dbTweet = self.models['GeneratedTweets'](user = self.user, tweet = tweet)

            self.db.session.add(dbTweet)
            self.db.session.commit()
            self.api.update_status(tweet)
            return tweet

        else:
            # Chooses a random integer between 1 and 20. If it is <= 4 a generic Tweet is selected.
            # This translates to a 20% chance of a generic Tweet being selected
            if randint(1, 20) <= 4:
                tweet = self.genericTweets[choice(self.genericTweets.keys())]
            else:
                userToTweet = choice(self.models['Users'].query.all()).username
                tweets = [tweet.text for tweet in self.models['Tweets'].query.filter(self.models['Tweets'].username == userToTweet)]
                tweet = self.generateTweet(tweets, userToTweet)
                dbTweet = self.models['GeneratedTweets'](user = userToTweet, tweet = tweet)

            if dbTweet:
                self.db.session.add(dbTweet)
                self.db.session.commit()

            self.api.update_status(tweet)
            return tweet
