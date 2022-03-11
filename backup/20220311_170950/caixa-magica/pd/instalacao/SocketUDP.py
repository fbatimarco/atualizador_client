import socket
import logging

class SocketUDP():
        
    def __init__(self):
        pass
    
    def send_message(self, server, message):
        aux = server.split(":")
        # Create a UDP socket
        sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        server_address = (aux[0], int(aux[1]))
        try:
            # Send data
            print('sending {!r}'.format(message))
            logging.info('Enviando informações: ', message.decode())
            sent = sock.sendto(message, server_address)
        except Exception:
            print('Falha ao enviar dados ao servidor')
            
        finally:
            print('closing socket')
            sock.close()
            
            
    def read_config_server_udp(self):
        try:
            arq = open('server.cfg', 'r')
            print ('Arquivo config server encontrado!')
            config=arq.read()
            return config
        except IOError:
            print ('Arquivo config server não encontrado! Criando configuração padrão.')
            arq = open('server.cfg', 'w')
            texto = []
            texto.append('fs.b2ml.com.br')#Endereço servidor UDP
            texto.append(':')
            texto.append('9000')#Porta Servidor
            arq.writelines(texto)
            arq.close()
            arq = open('server.cfg', 'r')
            default=arq.read()
            return default            