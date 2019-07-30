import requests
import twitter

class du3aaAPI():
    
    def __init__(self, length=280):
        self.consumer_key = 'igqHTcN90lrAJkmpMv2dCBBrx'
        self.consumer_secret = 'xM1HIUhCdIQJTh2qbmxXoByqay96HklXw2ymgTGUvg7KTTdrDA'
        self.access_token_key = '838160676199755776-YnmjKQxeht0YeXdyvV1vSZ7BJX1h7fY'
        self.access_token_secret = 'v7cGkFnV7G6ojQcYnksJfo2Kicxq5WxJ2QoWE3frfEiDs'
        self.length = length

    def Get(self):
        response = requests.get('https://du3aa.rest/api/')
        # print(response.status_code)

        data = response.json()
        data = data['du3aa']

        if(len(data) > self.length):
            # print(f'length is {len(data)} - bigger than {self.length}')
            self.Get()
        else:
            # print(data)
            # print(f'length is {len(data)}')
            self.Post(data)

    def Post(self, status):
        api = twitter.Api(
            consumer_key=self.consumer_key,
            consumer_secret=self.consumer_secret,
            access_token_key=self.access_token_key,
            access_token_secret=self.access_token_secret
        )
        # print(api.VerifyCredentials())
        post = api.PostUpdate(status=status)
        # print(post)


du3aa = du3aaAPI()
du3aa.Get()
# du3aa.Post()