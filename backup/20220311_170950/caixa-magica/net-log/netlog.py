#!/usr/bin/pyconcrete

'''
sudo mv netlog.service /lib/systemd/system/netlog.service
sudo systemctl start netlog
sudo systemctl enable netlog
'''
import socket
from time import sleep
from datetime import datetime
import logging
from logging.handlers import RotatingFileHandler

log_formatter = logging.Formatter('%(asctime)s %(levelname)s %(message)s')

logFile = 'netlog.log'

my_handler = RotatingFileHandler(logFile, mode='a', maxBytes=5*1024*1024, backupCount=2, encoding=None, delay=0)
my_handler.setFormatter(log_formatter)
my_handler.setLevel(logging.INFO)
app_log = logging.getLogger('root')
app_log.setLevel(logging.INFO)
app_log.addHandler(my_handler)

def has_internet(host="8.8.8.8", port=53, timeout=3):
  """
  Host: 8.8.8.8 (google-public-dns-a.google.com)
  OpenPort: 53/tcp
  Service: domain (DNS/TCP)
  """
  try:
    socket.setdefaulttimeout(timeout)
    socket.socket(socket.AF_INET, socket.SOCK_STREAM).connect((host, port))
    return True
  except socket.error as ex:
    #print(ex)
    return False

while True:
    if has_internet():
        sleep(30)
    else:
        first_time = datetime.now()
        app_log.info("Internet caiu")
        while True:
            sleep(5)
            if has_internet():
                now = datetime.now()
                delta = now - first_time
                app_log.info("Internet voltou. Tempo sem internet: " + str(delta))
                break