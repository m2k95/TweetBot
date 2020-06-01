import requests
import twitter
import pymongo
import os

class CheckSignedUsers():

    def __init__(self):
        self.consumer_key = os.environ.get('CONSUMER_KEY')
        self.consumer_secret = os.environ.get('CONSUMER_SECRET')
        self.MonogoDB = pymongo.MongoClient(os.environ.get('MONGODB'))
        self.DB = self.MonogoDB[os.environ.get('DATABASE_NAME')]
        self.collection = self.DB[os.environ.get('T_COLLECTION')]
        self.count = 0
        self.deleted = 0

    def Get(self):
        for x in self.collection.find():
            self.Clean(x['oauth_token'], x['oauth_token_secret'], x['user_id'])
            self.count += 1

        print (f'Total users {self.count}, deleted users {self.deleted}, remaining users {self.count - self.deleted}')

    def Clean(self, oauth_token, oauth_token_secret, user_id):
        try:
            api = twitter.Api(
                consumer_key = self.consumer_key,
                consumer_secret = self.consumer_secret,
                access_token_key = oauth_token,
                access_token_secret = oauth_token_secret
            )
            api.VerifyCredentials()
            
        except twitter.error.TwitterError as e:
            err = e.message[0]['message']
            if (err == 'Invalid or expired token.'):
                data = { "user_id": user_id }
                self.collection.delete_one(data)
                self.deleted += 1

        except Exception as e:
            print(e)

if __name__ == "__main__":
	check = CheckSignedUsers()
	check.Get()
