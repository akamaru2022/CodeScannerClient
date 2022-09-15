import socket
from datetime import datetime
import time
import json
import logging

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