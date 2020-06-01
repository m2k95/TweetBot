import requests
import twitter
import os
import BotLog
import logging
import pymongo

class du3aaAPI():

    def __init__(self, length=280):
        self.consumer_key = os.environ.get('CONSUMER_KEY')
        self.consumer_secret = os.environ.get('CONSUMER_SECRET')
        self.access_token_key = os.environ.get('ACCESS_TOKEN_KEY')
        self.access_token_secret = os.environ.get('ACCESS_TOKEN_SECRET')
        self.MonogoDB = pymongo.MongoClient(os.environ.get('MONGODB'))
        self.DB = self.MonogoDB[os.environ.get('DATABASE_NAME')]
        self.collection = self.DB[os.environ.get('D_COLLECTION')]
        self.length = length

    def Get(self):
        try:
            for r in self.collection.aggregate([{ "$sample": { "size": 1 } }]):
                data = r['du3aa']

            if(len(data) > self.length):
                logging.error('Data length is long. Trying again')
                self.Get()
            else:
                self.Post(data)
        except Exception as e:
            logging.error(f'Exception occured while requesting data. Trying again: {e}')
            self.Get()

    def Post(self, status):
        try:
            api = twitter.Api(
                consumer_key=self.consumer_key,
                consumer_secret=self.consumer_secret,
                access_token_key=self.access_token_key,
                access_token_secret=self.access_token_secret
            )
            post = api.PostUpdate(status=status)
            logging.info('Tweet posted')
        except Exception as e:
            logging.error(f'Exception occured while posting. Trying again: {e}')
            self.Get()

if __name__ == "__main__":
	du3aa = du3aaAPI()
	du3aa.Get()
