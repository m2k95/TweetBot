from datetime import datetime
from pathlib import Path
import requests
import twitter
import os
import logging
import sys

formatter = logging.Formatter("[%(asctime)-15s] [%(levelname)s] %(message)s")

# Logging filename and path
DATENOW = datetime.now().strftime('%Y-%m-%d')
YEAR = datetime.now().strftime('%Y')
MONTH = datetime.now().strftime('%m')
CURRENTPATH = os.path.dirname(os.path.realpath(__file__))
LOGGER_PATH = CURRENTPATH + '/logs/' + YEAR + '/' + MONTH + '/'
FILENAME = DATENOW + '.log'

Path(LOGGER_PATH).mkdir(parents=True, exist_ok=True)

MainLogger = logging.getLogger('GET_RANDOM')
MainLogger.setLevel(logging.INFO)
logger_file_handler = logging.FileHandler(LOGGER_PATH + FILENAME)
logger_file_handler.setFormatter(formatter)
MainLogger.addHandler(logger_file_handler)

class du3aaAPI():

  def __init__(self, length=280):
    self.consumer_key = os.environ.get('CONSUMER_KEY')
    self.consumer_secret = os.environ.get('CONSUMER_SECRET')
    self.access_token_key = os.environ.get('ACCESS_TOKEN_KEY')
    self.access_token_secret = os.environ.get('ACCESS_TOKEN_SECRET')
    self.length = length

  def getRandom(self):
    try:
      response = requests.get('https://api.du3aa.rest')
      data = response.json()['prayer']

      if(len(data) > self.length):
        MainLogger.error('Data length is long. Trying again')
        self.getRandom()
      if(len(data) == 0):
        MainLogger.error('Data length equals 0. Trying again')
        self.getRandom()
      if(data is None):
        MainLogger.error('Data type is NoneType. Trying again')
        self.getRandom()
      else:
        return data
        
    except Exception as e:
      MainLogger.error(f'Exception occured while requesting data. Trying again: {e}')

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
        MainLogger.info('Tweet posted')
      else:
        MainLogger.error('Tweet NOT posted')

    except Exception as e:
      MainLogger.error(f'Exception occured while posting. Trying again: {e}')
      self.Post()

  def getRandomTest(self):
    status = self.getRandom()
    print(status)

if __name__ == "__main__":
  def usage():
    print('Usage: python app.py [post|test]')

  if len(sys.argv) == 2:
    app = du3aaAPI()
    if sys.argv[1] == 'post':
      app.Post()
    elif sys.argv[1] == 'test':
      app.getRandomTest()
    else:
      usage()
  else:
    usage()
