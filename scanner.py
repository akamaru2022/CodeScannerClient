import sys, getopt
import socket
from datetime import datetime
import logging

class Repository:
    TIMEOUT=3

    def __init__(self, deviceID, host, port):
        self.__deviceID = deviceID
        self.__host = host
        self.__port = int(port)

    def save(self, code):
        data = self.__deviceID + ':' + code
        logging.info(data)
        s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        s.settimeout(self.TIMEOUT)
        try:
            s.connect((self.__host, self.__port))
            s.send(data.encode())
            res = s.recv(1024)
            return res.decode()
        except ConnectionRefusedError as cre:
            logging.exception('Connection Refused Error-> %s:%d', self.__host, self.__port)
            return
        except socket.timeout:
            logging.exception('Connection Timeout-> %s:%d', self.__host, self.__port)
            return
        except Exception as e:
            logging.exception(e)
            return
        finally:
            s.close

def main(argv):
    logFilename = '{:%Y-%m-%d}.log'.format(datetime.now())
    logFormat = '%(asctime)s %(levelname)s: %(message)s'
    logging.basicConfig(filename=logFilename, format=logFormat, level=logging.INFO)
    deviceID = 'Lobby'
    ip = '127.0.0.1'
    port = '1234'

    try:
        opts, args = getopt.getopt(argv,"hd:i:p:",["deviceID=","serverIP=","serverPort="])
    except getopt.GetoptError:
        print('test.py -i <inputfile> -o <outputfile>')
        sys.exit(2)
    for opt, arg in opts:
        if opt == '-h':
            print('test.py -i <inputfile> -o <outputfile>')
            sys.exit()
        elif opt in ("-d", "--deviceID"):
            deviceID = arg
        elif opt in ("-i", "--serverIP"):
            ip = arg
        elif opt in ("-p", "--serverPort"):
            port = arg

    repository = Repository(deviceID, ip, port)

    while True:
        outdata = input('type... ')
        response = repository.save(outdata)
        print(response)


if __name__ == "__main__":
    main(sys.argv[1:])
