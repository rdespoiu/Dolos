import tweepy
from random import choice
from datetime import datetime
from config import *
from flask import Flask, request, flash, url_for, redirect, render_template
from flask_sqlalchemy import SQLAlchemy
from Controllers.tweet_manager import Tweeter
from Controllers.data_scraper import DataScraper
from Controllers.get_user_data import GetUserData
from Controllers.create_tweet import CreateTweet
from Utility.timestamp import timestamp
from Utility.generatehash import generateHash, generateSalt
from Utility.results import results
from shared.models import db
from Models.users import Users
from Models.tweets import Tweets
from Models.admins import Admins
from Models.generatedtweets import GeneratedTweets

# Dictionary of models
dbModels = {
            'Users': Users,
            'Tweets': Tweets,
            'Admins': Admins,
            'GeneratedTweets': GeneratedTweets
}

# Setup for Tweepy/Twitter API
auth = tweepy.OAuthHandler(CONSUMER_KEY, CONSUMER_SECRET)
auth.set_access_token(ACCESS_KEY, ACCESS_SECRET)
api = tweepy.API(auth)
api.wait_on_rate_limit = True
api.wait_on_rate_limit_notify = True

# Flask app setup
app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///dolos.sqlite3'
app.config['SESSION_TYPE'] = 'sqlite'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = True

db.init_app(app)
db.app = app
db.create_all()

# Authenticated user
loggedInUser = None


# Main user facing route
@app.route('/', methods=['GET', 'POST'])
def index():
    global loggedInUser

    if request.method == 'POST':
        user = Admins.query.filter_by(username = request.form['username']).first()
        if user:
            password = generateHash(user.salt, request.form['password'])
            if password == user.password:
                loggedInUser = request.form['username']
            else:
                flash('Invalid username or password', 'error')
        else:
            flash('Invalid username or password', 'error')

    if loggedInUser:
        return render_template('index.html',
                                user = loggedInUser,
                                twitterUsers = Users.query.all(),
                                userTweets = Tweets.query.order_by(Tweets.tweetid.desc()),
                                dolosTweets = GeneratedTweets.query.order_by(GeneratedTweets.date.desc()))
    else:
        return render_template('index.html', user = loggedInUser)

# Route used to manually post a tweet from the user interface
@app.route('/createtweet')
def create_tweet():
    global loggedInUser

    username = request.args.get('username')

    try:
        tweet = CreateTweet(dbModels, db, api, DEPTH, username).postTweet()
        return results(tweet)
    except Exception, e:
        return results('Failed to post tweet. An error occurred: {}'.format(str(e)))

# Route used to map new user to DB from the user interface
@app.route('/getuser')
def get_user_data():
    global loggedInUser

    if not loggedInUser:
        return results('Unauthorized access attempt. Please ensure you are authenticated.')


    username = request.args.get('username')
    if username:
        try:
            GetUserData(dbModels, db, api, username).getUser()
            return results('User: {} mapped to database successfully'.format(username))
        except Exception, e:
            return results('An error occurred: {}'.format(str(e)))
    else:
        return results('User ID or username required')

# Not currently being used, but it is intended as a way to manually scrape the Twitter API for user Tweets.
@app.route('/getusertweets')
def get_user_tweets():
    global loggedInUser

    if not loggedInUser:
        return results('Unauthorized access attempt. Please ensure you are authenticated.')

    username = request.args.get('username')
    if username:
        try:
            GetUserData(dbModels, db, api, username).getUserTweets()
            return results('Tweets for user: {} mapped to database successfully'.format(userID or username))
        except Exception, e:
            return results('An error occurred: {}'.format(str(e)))
    else:
        return results('User ID or username required')
