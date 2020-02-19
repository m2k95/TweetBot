from time import time
from datetime import datetime
import os
import os.path

def TweetBotLog(status):
    Dirctory = 'logs'
    if not os.path.exists(Dirctory):
        os.makedirs(Dirctory)

    DATENOW = datetime.now().strftime('%Y-%m-%d')

    filename = DATENOW + '.log'

    FullFileName = Dirctory + '/' + filename
    file_exists = os.path.isfile(FullFileName)

    with open(FullFileName, 'a') as LogFile:

        timestamp = time()
        dt_object = datetime.fromtimestamp(timestamp)

        if not file_exists:
            LogFile.write('# TweetBot Logs\n')
            LogFile.write('# ' + DATENOW + '\n')
            LogFile.write('# @du3aaAPI\n')

        LogFile.write(f'\n[{dt_object.strftime("%I:%M:%S %p")}] {status}')
