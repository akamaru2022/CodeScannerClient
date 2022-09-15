import sys, getopt
from datetime import datetime
import logging

from repository import Repository

def main(argv):
    HINT = 'scanner.py -d <deviceID> -i <serverIP> -p <serverPort>'

    logFilename = '{:%Y-%m-%d}.log'.format(datetime.now())
    logFormat = '%(asctime)s %(levelname)s: %(message)s'
    logging.basicConfig(filename=logFilename, format=logFormat, level=logging.INFO)
    deviceID = 'Lobby'
    ip = '127.0.0.1'
    port = '1234'

    try:
        opts, args = getopt.getopt(argv,"hd:i:p:",["deviceID=","serverIP=","serverPort="])
    except getopt.GetoptError:
        print(HINT)
        sys.exit(2)
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

    repository = Repository(deviceID, ip, port)

    while True:
        outdata = input('scan... ')
        response = repository.save(outdata)
        print(response)

if __name__ == "__main__":
    main(sys.argv[1:])
