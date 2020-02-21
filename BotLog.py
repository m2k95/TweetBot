from datetime import datetime
import logging
import os

# Logging format
FORMAT = "[%(asctime)-15s] [%(levelname)s] %(message)s"

# Logging filename and path
DATENOW = datetime.now().strftime('%Y-%m-%d')
CURRENTPATH = os.path.dirname(os.path.realpath(__file__))
FILEPATH = CURRENTPATH + '/logs/'
FILENAME = DATENOW + '.log'

if not os.path.exists(FILEPATH):
    os.makedirs(FILEPATH)

# Configure logging
logging.basicConfig(filename=FILEPATH + FILENAME, filemode='a', format=FORMAT, level=logging.DEBUG)