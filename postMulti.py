import requests
import twitter
import pymongo
import random
import os

class du3aaAPI():

    def __init__(self, length=280):
        self.consumer_key = os.environ.get('CONSUMER_KEY')
        self.consumer_secret = os.environ.get('CONSUMER_SECRET')
        self.MonogoDB = pymongo.MongoClient(os.environ.get('MONGODB'))
        self.DB = self.MonogoDB[os.environ.get('DATABASE_NAME')]
        self.collection = self.DB[os.environ.get('D_COLLECTION')]
        self.tcollection = self.DB[os.environ.get('T_COLLECTION')]
        self.length = length
        self.count = 0

    def Get(self):
        try:
            for r in self.collection.aggregate([{ "$sample": { "size": 1 } }]):
                data = r['du3aa']
            return data

        except Exception as e:
            pass

    def Iterate(self):
        try:
            status = self.Get()
            if(len(data) > self.length):
                status = self.Get()

            for x in self.tcollection.find():
                self.Post(status, x['oauth_token'], x['oauth_token_secret'])
        except Exception as e:
            pass


    def Post(self, status, oauth_token, oauth_token_secret):
        try:
            api = twitter.Api(
                consumer_key=self.consumer_key,
                consumer_secret=self.consumer_secret,
                access_token_key=oauth_token,
                access_token_secret=oauth_token_secret
            )
            post = api.PostUpdate(status=status)

        except twitter.error.TwitterError as e:
            pass

        except Exception as e:
            pass

if __name__ == "__main__":
    du3aa = du3aaAPI()
    du3aa.Iterate()
