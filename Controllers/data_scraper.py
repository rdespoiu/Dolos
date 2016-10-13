import threading
import time
from Controllers.get_user_data import GetUserData
from Utility.pprint import pprint

class DataScraper(object):

    def __init__(self, interval, models, db, api):
        self.interval = interval
        self.models = models
        self.db = db
        self.api = api

        thread = threading.Thread(target = self.run, args = ())
        thread.daemon = True
        thread.start()

    def run(self):
        while True:
            users = self.models['Users'].query.all()
            for user in users:
                try:
                    GetUserData(self.models, self.db, self.api, user.username).getUserTweets()
                    pprint('Successfully scraped new data for user: {}'.format(user.username))
                except Exception, e:
                    error = str(e)
                    pprint(error)
                time.sleep(self.interval)
