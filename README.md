# Dolos

Dolos is a Flask/SQLAlchemy driven Twitter bot that uses a Markov chain to emulate users.
Check it out at twitter.com/DolosBot!

To get started, follow these instructions:
```
cd YOUR_DIRECTORY                                   # Directory where you plan on cloning Dolos
git clone https://github.com/rdespoiu/Dolos.git
cd Dolos
pip install -r requirements.txt                     # Install required dependencies needed to run Dolos
```

Once you've cloned the repository and installed all required dependencies, you'll need to do a little configuration.

First, rename `config_SAMPLE.py` to `config.py`

Next, you'll need to register an application with Twitter in order to get some API keys.

Go to the Twitter [App Management](https://apps.twitter.com) page, log in and select `Create New App`
Create your application and navigate to the `Keys and Access Tokens` tab.

Take note of the `Consumer Key (API Key)` and `Consumer Secret (API Secret)` keys near the top of the page.

Under `Your Access Token`, select `Create My Access Token`.

When this is completed, you'll be able to see:
```
Consumer Key (API Key)
Consumer Secret (API Secret)
Access Token
Access Token Secret
```

Take these and set them as the values for their respective variables in `config.py`

```
# config.py


############
#   KEYS   #
############

CONSUMER_KEY = 'Your consumer key'
CONSUMER_SECRET = 'Your consumer secret'
ACCESS_KEY = 'Your access key'
ACCESS_SECRET = 'Your access secret'

# Depth for Dolos to crawl the Markov chain
DEPTH = 5

# Time interval between tweets (in seconds)
INTERVAL = 300

# Time interval between tweet scrapes for existing users (in seconds)
SCRAPE_INTERVAL = 1800
```

`INTERVAL`: Length of time between tweets by your application. It is set at 300 seconds (5 minutes) by default but feel free to fiddle with it.

`SCRAPE_INTERVAL`: Length of time between scrapes of users' tweets in your application's database. Be aware that Twitter's API will block requests if too many have been made in a 15 minute period. The length of time that subsequent calls are blocked increases exponentially with each failed request. To protect your application from the time-out increases,
```
api.wait_on_rate_limit = True
api.wait_on_rate_limit_notify = True
```
have been set in app.py. Failed requests will no longer count against the application and the application will print to your console the amount of time left until you can make another request.


You're now all set to get started!
```
cd ..           # Move up one directory from where the application's files are located
python Dolos    # Python 2.7 is expected. The application will throw an exception if Python 3 is used.
```

Your output should be something along the lines of `* Running on http://127.0.0.1:5000/ (Press CTRL+C to quit)`

In a browser, navigate to `http://127.0.0.1:5000` (or whatever your output specified)

You will see that you need to log in to use the application. You don't, however, have an account just yet. We wanted to start the application so that a sqlite3 database could be created.

To add an account:

```
python Dolos/DolosAdmin username password   # Replace username and password with your desired choices (A salt is created for each user and the password is then hashed using that salt)
```

Now you should be able to log in to the Dolos administrative panel. Navigate to the `Twitter Users` page. From here, you can type in a Twitter user's handle and click `Add User`. Dolos will then add that user to the database along with their tweets.

Continue to do this with any other users you'd like to emulate (staying aware that you may need to wait until Twitter allows you to make another call) and you should begin to see the application posting tweets on the account you created the app for!

To manually post a tweet for a specific user, click `Post Tweet` on the `Twitter Users` page.


For any questions or concerns, please contact me at roberto.despoiu@gmail.com
