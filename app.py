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
POST_ALL_FILEPATH = CURRENTPATH + '/logs/postAll/'
CLEAN_FILEPATH = CURRENTPATH + '/logs/clean/'
FILENAME = DATENOW + '.log'

if not os.path.exists(GET_RANDOM_FILPATH):
    os.makedirs(GET_RANDOM_FILPATH)
if not os.path.exists(POST_FILEPATH):
    os.makedirs(POST_FILEPATH)
if not os.path.exists(POST_ALL_FILEPATH):
    os.makedirs(POST_ALL_FILEPATH)
if not os.path.exists(CLEAN_FILEPATH):
    os.makedirs(CLEAN_FILEPATH)

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

postAllLoger = logging.getLogger('POST_ALL')
postAllLoger.setLevel(logging.INFO)
postAll_file_handler = logging.FileHandler(POST_ALL_FILEPATH + FILENAME)
postAll_file_handler.setFormatter(formatter)
postAllLoger.addHandler(postAll_file_handler)

cleanLogger = logging.getLogger("CLEAN")
cleanLogger.setLevel(logging.INFO)
clean_file_handler = logging.FileHandler(CLEAN_FILEPATH + FILENAME)
clean_file_handler.setFormatter(formatter)
cleanLogger.addHandler(clean_file_handler)

class du3aaAPI():

    def __init__(self, length=280):
        self.consumer_key = os.environ.get('CONSUMER_KEY')
        self.consumer_secret = os.environ.get('CONSUMER_SECRET')
        self.access_token_key = os.environ.get('ACCESS_TOKEN_KEY')
        self.access_token_secret = os.environ.get('ACCESS_TOKEN_SECRET')
        self.MonogoDB = pymongo.MongoClient(os.environ.get('MONGODB'))
        self.DB = self.MonogoDB[os.environ.get('DATABASE_NAME')]
        self.collection = self.DB[os.environ.get('D_COLLECTION')]
        self.tcollection = self.DB[os.environ.get('T_COLLECTION')]
        self.length = length
        self.count = 0
        self.deleted = 0

    def getRandom(self):
        try:
            for r in self.collection.aggregate([{ "$sample": { "size": 1 } }]):
                data = r['du3aa']

            if(len(data) > self.length):
                getRandomLogger.error('Data length is long. Trying again')
                self.getRandom()
            else:
                return data
        except Exception as e:
            getRandomLogger.error(f'Exception occured while requesting data. Trying again: {e}')

    def Iterate(self):
        try:
            self.count = 0

            for x in self.tcollection.find():
                self.PostMulti(x['oauth_token'], x['oauth_token_secret'])
            
            postAllLoger.info(f'{self.count} tweets posted')
        except Exception as e:
            postAllLoger.error(f'Exception occured while iterating: {e}')
            pass
    
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
            postLogger.info('Tweet posted')
        except Exception as e:
            postLogger.error(f'Exception occured while posting. Trying again: {e}')
            self.Post()

    def PostMulti(self, oauth_token, oauth_token_secret):
        try:
            access_token_key = oauth_token
            access_token_secret = oauth_token_secret

            status = self.getRandom()
            
            api = twitter.Api(
                consumer_key=self.consumer_key,
                consumer_secret=self.consumer_secret,
                access_token_key=access_token_key,
                access_token_secret=access_token_secret
            )
            post = api.PostUpdate(status=status)
            self.count += 1

        except twitter.error.TwitterError as e:
            postAllLoger.error(f'Exception occured while posting multi. Trying again: {e}')
            err = e.message[0]['message']
            if (err == 'Invalid or expired token.'):
                pass
            else:
                self.PostMulti(access_token_key, access_token_secret)

        except Exception as e:
            postAllLoger.exception(f'Exception occured while posting multi2. Trying again: {e}')
            self.PostMulti(access_token_key, access_token_secret)

    def Clean(self):
        try:
            self.count = 0
            self.deleted = 0

            for x in self.tcollection.find():
                self.cleaningProcess(x['oauth_token'], x['oauth_token_secret'], x['user_id'])
                self.count += 1

            cleanLogger.info(f'Total users {self.count}, deleted users {self.deleted}, remaining users {self.count - self.deleted}')
        except Exception as e:
            cleanLogger.error(f'Exception in Clean method. Trying again: {e}')
            self.Clean()

    def cleaningProcess(self, oauth_token, oauth_token_secret, userid):
        try:
            access_token_key = oauth_token
            access_token_secret = oauth_token_secret
            user_id = userid

            api = twitter.Api(
                consumer_key = self.consumer_key,
                consumer_secret = self.consumer_secret,
                access_token_key = access_token_key,
                access_token_secret = access_token_secret
            )
            api.VerifyCredentials()
            
        except twitter.error.TwitterError as e:
            cleanLogger.error(f'Exception occured in cleaning process. Trying again: {e}')
            err = e.message[0]['message']
            if (err == 'Invalid or expired token.'):
                data = { "user_id": user_id }
                self.collection.delete_one(data)
                self.deleted += 1
            else:
                self.cleaningProcess(access_token_key, access_token_secret, user_id)

        except Exception as e:
            cleanLogger.error(f'Exception occured in cleaning process. Trying again: {e}')
            self.cleaningProcess(access_token_key, access_token_secret, _user_id)
