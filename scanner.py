import sys, getopt
# from datetime import datetime
import logging
import logging.handlers
import os

from repository import Repository

HINT = 'scanner.py -d <deviceID> -i <serverIP> -p <serverPort>'

def initLogger():
    logFolder = os.path.join(os.path.abspath('log'))
    if not os.path.exists(logFolder):
        os.makedirs(logFolder)
    # logFilename = '{:%Y-%m-%d}.log'.format(datetime.now())
    logFilename = 'scanner.log'
    logpath = os.path.join(logFolder, logFilename)
    logFormat = '%(asctime)s %(levelname)s: %(message)s'
    logger = logging.getLogger('scanner')
    logger.setLevel(logging.INFO)
    logHandler = logging.handlers.RotatingFileHandler(
        filename=logpath,
        maxBytes=1024 * 1024 * 1,
        backupCount=10,
        encoding='utf-8'
        )
    # ONE_WEEK_DAYS = 7
    # loggerHandler = logging.handlers.TimedRotatingFileHandler(
    #     when='D',
    #     interval=1,
    #     backupCount=ONE_WEEK_DAYS,
    #     encoding='utf-8'
    # )
    logHandler.setFormatter(logging.Formatter(logFormat))
    logger.addHandler(logHandler)

def initService(argv):
    try:
        opts, args = getopt.getopt(argv,"hd:i:p:",["deviceID=","serverIP=","serverPort="])
    except getopt.GetoptError:
        print(HINT)
        sys.exit(2)
    deviceID = 'Lobby'
    ip = '127.0.0.1'
    port = '1234'
    for opt, arg in opts:
        if opt == '-h':
            print(HINT)
            sys.exit()
        elif opt in ("-d", "--deviceID"):
            deviceID = arg
        elif opt in ("-i", "--serverIP"):
            ip = arg
        elif opt in ("-p", "--serverPort"):
            port = arg
    return (deviceID, ip, port)

def main(argv):

    initLogger()
    (deviceID, ip, port) = initService(argv)

    repository = Repository(deviceID, ip, port)

    while True:
        outdata = input('scan... ')
        response = repository.save(outdata)
        print(response)

if __name__ == "__main__":
    main(sys.argv[1:])
