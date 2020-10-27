from datetime import datetime
import requests
import twitter
import os
import logging
import pymongo

formatter = logging.Formatter("[%(asctime)-15s] [%(levelname)s] %(message)s")

# Logging filename and path
DATENOW = datetime.now().strftime('%Y-%m-%d')
CURRENTPATH = os.path.dirname(os.path.realpath(__file__))
GET_RANDOM_FILPATH = CURRENTPATH + '/logs/getRandom/'
POST_FILEPATH = CURRENTPATH + '/logs/post/'
FILENAME = DATENOW + '.log'

if not os.path.exists(GET_RANDOM_FILPATH):
    os.makedirs(GET_RANDOM_FILPATH)
if not os.path.exists(POST_FILEPATH):
    os.makedirs(POST_FILEPATH)

getRandomLogger = logging.getLogger('GET_RANDOM')
getRandomLogger.setLevel(logging.INFO)
random_file_handler = logging.FileHandler(GET_RANDOM_FILPATH + FILENAME)
random_file_handler.setFormatter(formatter)
getRandomLogger.addHandler(random_file_handler)

postLogger = logging.getLogger('POST')
postLogger.setLevel(logging.INFO)
post_file_handler = logging.FileHandler(POST_FILEPATH + FILENAME)
post_file_handler.setFormatter(formatter)
postLogger.addHandler(post_file_handler)

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

    def getRandom(self):
        try:
            for r in self.collection.aggregate([{ "$sample": { "size": 1 } }]):
                data = r['du3aa']

            if(len(data) > self.length):
                getRandomLogger.error('Data length is long. Trying again')
                self.getRandom()
            if(len(data) == 0):
                getRandomLogger.error('Data length equals 0. Trying again')
                self.getRandom()
            if(data is None):
                getRandomLogger.error('Data type is NoneType. Trying again')
                self.getRandom()
            else:
                return data
                
        except Exception as e:
            getRandomLogger.error(f'Exception occured while requesting data. Trying again: {e}')

    def Post(self):
        try:
            api = twitter.Api(
                consumer_key=self.consumer_key,
                consumer_secret=self.consumer_secret,
                access_token_key=self.access_token_key,
                access_token_secret=self.access_token_secret
            )
            status = self.getRandom()

            post = api.PostUpdate(status=status)
            if (post.created_at):
                postLogger.info('Tweet posted')
            else:
                postLogger.error('Tweet NOT posted')

        except Exception as e:
            postLogger.error(f'Exception occured while posting. Trying again: {e}')
            self.Post()

if __name__ == "__main__":
    app = du3aaAPI()
    app.Post()
