import requests
import json
import datetime
import sys
import logging
import time
sys.path.insert(1, '/home/pi/caixa-magica/pd/')
from PortaSerial import PortaSerial
from threading import Thread

def ler_dados_gps():
    while True:
        logging.warning('Iniciando envio de dados do GPS')
        serial = PortaSerial()
        aux = serial.read_config_serial()
        print(aux)
        dados_validos = serial.ler_porta(aux)
        if dados_validos:
            print('Dados do GPS enviado')
            print(dados_validos)
            time.sleep(2.0)
            print('GPS On-line')
        else:
            print('Dados do GPS inválido')
            time.sleep(2.0)
            print('GPS Off-line')
        time.sleep(30.0)
ler_dados_gps()
