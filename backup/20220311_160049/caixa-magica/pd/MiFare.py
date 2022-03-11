import time
from datetime import datetime
import logging
import socket
import json
import uuid
import serial

class MiFareRead():
    port = ''
    def __init__(self, port='/dev/ttyUSB0'):
        self.port = port

    def get_card_number(self):
        with serial.Serial(self.port, 19200) as ser:
            r = ser.read(9)
            s = str(r.hex())
            ser.close()
            return s[6:14]
        return False

# logging.basicConfig(filename='/home/pi/caixa-magica/core/logs/mifare.log', filemode='w', format='%(asctime)-15s - %(name)s - %(levelname)s - %(message)s', level=logging.DEBUG)

HOST = ''  # The server's hostname or IP address
PORT = 0        # The port used by the server
BUFSIZE = 0

with open('/home/pi/caixa-magica-vars/config.json') as json_data:
    config = json.load(json_data)
    HOST = config['core']['host']
    PORT = config['core']['port']
    BUFSIZE = config['core']['bufsize']

def send(cartao):
    try:
        with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
            data = {
                'type': 'cartao',
                'cartao': cartao
            }
            s.connect((HOST, PORT))
            js = json.dumps(data)
            s.sendall(js.encode('utf-8'))
            data = s.recv(BUFSIZE)
        print('Received', repr(data))
        
    except:
        print("Verifique se o server está up")
 
mifare = MiFareRead()
while True:
    try:
        cartao = mifare.get_card_number()
        print(cartao)
        if cartao and cartao != "":
            print("Cartao:", cartao)
            logging.info("Cartao Selecionado")
            send(cartao)
            time.sleep(3)
        else:
            print("Cartao nao detectado")
    except Exception as e:
        print("Cartao nao detectado", e)
    time.sleep(0.2)
