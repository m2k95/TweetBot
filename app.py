import requests
import twitter
import os
from BotLog import TweetBotLog

class du3aaAPI():

    def __init__(self, length=280):
        self.consumer_key = os.environ.get('CONSUMER_KEY')
        self.consumer_secret = os.environ.get('CONSUMER_SECRET')
        self.access_token_key = os.environ.get('ACCESS_TOKEN_KEY')
        self.access_token_secret = os.environ.get('ACCESS_TOKEN_SECRET')
        self.length = length

    def Get(self):
        try:
            response = requests.get('https://du3aa.rest/api/')
            # print(response.status_code)

            data = response.json()
            data = data['du3aa']

            if(len(data) > self.length):
                # print(f'length is {len(data)} - bigger than {self.length}')
                TweetBotLog('Data length is long. Trying again')
                self.Get()
            else:
                # print(data)
                # print(f'length is {len(data)}')
                self.Post(data)
        except Exception:
            TweetBotLog('Exception occured while requesting data. Trying again')
            self.Get()

    def Post(self, status):
        try:
            api = twitter.Api(
                consumer_key=self.consumer_key,
                consumer_secret=self.consumer_secret,
                access_token_key=self.access_token_key,
                access_token_secret=self.access_token_secret
            )
            # print(api.VerifyCredentials())
            post = api.PostUpdate(status=status)
            TweetBotLog('Tweet posted')
            # print(post)
        except Exception:
            TweetBotLog('Exception occured while posting. Trying again')
            self.Get()

if __name__ == "__main__":
	du3aa = du3aaAPI()
	du3aa.Get()
