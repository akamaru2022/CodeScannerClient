import sys, getopt
import socket

class Repository:

    def __init__(self, deviceID, host, port):
        self.__deviceID = deviceID
        self.__host = host
        self.__port = int(port)

    def save(self, code):
        data = self.__deviceID + ':' + code
        s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        s.connect((self.__host, self.__port))
        s.send(data.encode())
        res = s.recv(1024)
        s.close
        return res.decode()

class Logger:
    def log(self, message):
        return

def main(argv):
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
