import threading
import time
from Controllers.create_tweet import CreateTweet
from Utility.pprint import pprint

class Tweeter(object):

    def __init__(self, interval, models, db, api, depth):
        self.interval = interval
        self.models = models
        self.db = db
        self.api = api
        self.depth = depth

        thread = threading.Thread(target = self.run, args = ())
        thread.daemon = True
        thread.start()

    def run(self):
        while True:
            try:
                CreateTweet(self.models, self.db, self.api, self.depth).postTweet()
                pprint('Posted new tweet successfully')
            except Exception, e:
                error = str(e)
                pprint(error)

            time.sleep(self.interval)
