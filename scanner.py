import sys, getopt
import socket
import time
from datetime import datetime
import logging
import json

class Repository:
    RETRY = 3
    TIMEOUT = 1

    def __init__(self, deviceID, host, port):
        self.deviceID = deviceID
        self.iport = (host, int(port))
        self.connect()

    def connect(self):
        self.s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        try :
            self.s.settimeout(self.TIMEOUT)
            self.s.connect(self.iport)
        except :
            pass

    def save(self, code):
        scanTime = '{:%Y-%m-%d %H-%M-%S}'.format(datetime.now())
        data = {
            'DeviceID': self.deviceID,
            'ScanTime': scanTime,
            'Code': code
            }
        dataStr = json.dumps(data)

        i = 0
        while (i < self.RETRY):
            i = i+1
            try:
                send = self.s.send(dataStr.encode())
                if(send > 0):
                    logging.info(dataStr)
                res = self.s.recv(1024)
                return res.decode()
            except ConnectionResetError as cre:
                logging.exception('Connection Reset Error-> %s, try reconnection', self.iport)
            except ConnectionRefusedError as cre:
                logging.exception('Connection Refused Error-> %s', self.iport)
            except socket.timeout:
                logging.exception('Connection Timeout-> %s', self.iport)
            except socket.error :
                logging.exception('Socket Error-> %s', self.iport)
                time.sleep(1)
                self.connect()
            except Exception as e:
                logging.exception(e)

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
