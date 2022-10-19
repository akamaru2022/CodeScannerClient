import sys, getopt
# from datetime import datetime
import logging
import logging.handlers
import os
import configparser
import RPi.GPIO as GPIO
import time

from repository import Repository

HINT = 'scanner.py -d <deviceID> -i <serverIP> -p <serverPort>'
SUCCESS = '200'
FAILED = '500'

blue = 12
orange = 18
sound = 37
piano = 1000

GPIO.setmode(GPIO.BOARD)
GPIO.setup(orange, GPIO.OUT)
GPIO.setup(blue, GPIO.OUT)
GPIO.setup(sound, GPIO.OUT)

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

    logger = logging.getLogger('scanner')

    try:
        currentFolder = os.path.dirname(os.path.abspath(__file__))
        propertiesFile = os.path.join(currentFolder, '.properties')
        config = configparser.RawConfigParser()
        config.read(propertiesFile)
        deviceID = config.get('Device', 'ID')
        ip = config.get('Service', 'IP')
        port = config.get('Service', 'Port')
    except Exception as e:
        logger.e(e)
        pass

    try:
        opts, args = getopt.getopt(argv,"hd:i:p:",["deviceID=","serverIP=","serverPort="])
    except getopt.GetoptError:
        print(HINT)
        sys.exit(1)

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

def saveSuccess():
    GPIO.output(orange, False)
    GPIO.output(blue, True)
    print('success!!!')

def saveFailed():
    GPIO.output(blue, False)
    GPIO.output(orange, True)
    print('failed!!!')
    play(piano, 1)

def play(pitch, sec):
    half_pitch = (1 / pitch) / 2
    t = int(pitch * sec)
    for i in range(t):
        GPIO.output(sound, GPIO.HIGH)
        time.sleep(half_pitch)
        GPIO.output(sound, GPIO.LOW)
        time.sleep(half_pitch)

def main(argv):

    initLogger()
    (deviceID, ip, port) = initService(argv)

    repository = Repository(deviceID, ip, port)

    while True:
        outdata = input('scan... ')
        response = repository.save(outdata)
        if(response == SUCCESS):
            saveSuccess()
        else:
            saveFailed()


if __name__ == "__main__":
    main(sys.argv[1:])