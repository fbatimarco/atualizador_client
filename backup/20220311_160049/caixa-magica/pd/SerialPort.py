import serial
from tkinter import messagebox
import logging
class SerialPort():
        
    def __init__(self):
        pass
    
    
    def read_config_serial(self):
        try:
            arq = open('serial.cfg', 'r')
            print ('Arquivo config serial encontrado!')
            config=arq.read()
            return config
        except IOError:
            print ('Arquivo de config serial não encontrado! Criando configuração padrão.')
            arq = open('serial.cfg', 'w')
            texto = []
            texto.append('/dev/ttyACM0')#Porta padrão do Raspberry Pi
            #texto.append('COM6')#Porta para teste no Windows
            texto.append(':')
            texto.append('115200')#Baud rate padrão do GPS
            arq.writelines(texto)
            arq.close()
            arq = open('serial.cfg', 'r')
            default=arq.read()
            return default    
     
    ################    FUNCAO PARA ESCREVER NA PORTA ####################
    def escrever_porta(self, config, comand):
        dados = [0]*1
        try:
            aux = config.split(":")
            porta = aux[0]
            baud_rate = aux[1]
        except Exception:
            # logging.error("Falha ao obter a configuração da porta serial")
            porta = '/dev/ttyACM0'
            #porta = 'COM6'
            baud_rate = 115200
            
        try:
            obj_porta = serial.Serial(porta, baud_rate)
            # logging.warning("Enviando comando: " + str(comand))
            obj_porta.write(comand)
            
            response = obj_porta.read()
            # logging.warning("Response: " + response.hex())
            print("Response: ", response)
            if response.hex()=='bd':
                data_size = obj_porta.read()
                size = int.from_bytes(data_size, "big")
                # logging.warning("Tamanho resposta: " + str(size))
                print("Response: ", size)
                dados = [0]*size
                
                for i in range(size):
                    dados[i] = obj_porta.read()
                    
                # logging.warning("Dados: " + str(dados))
            obj_porta.close()
            #self.ler_porta(config)
        except serial.SerialException:
            messagebox.showwarning("Falha", "Verifique se existe algum dispositivo conectado na porta serial!")
            # logging.error("ERRO: Verifique se ha algum dispositivo conectado na porta serial!")
        
        return dados
     
    ########################## FUNCAO PARA LER A PORTA #######################
    def ler_porta(self,config):
        # logging.info("Lendo dados da porta serial")
        dados = [0]*1
        try:
            aux = config.split(":")
            porta = aux[0]
            baud_rate = aux[1]
        except Exception:
            # logging.error("Falha ao obter a configuração da porta serial")
            #porta = '/dev/ttyS0'
            porta = 'COM6'
            baud_rate = 115200

        try:
            obj_porta = serial.Serial(porta, baud_rate)
            response = obj_porta.read()
            # logging.warning("Response: " + response.hex())
            print("Response: ", response)
            if response.hex()=='bd':
                data_size = obj_porta.read()
                size = int.from_bytes(data_size, "big")
                # logging.warning("Tamanho resposta: " + str(size))
                print("Response: ", size)
                dados = [0]*size
                
                for i in range(size):
                    dados[i] = obj_porta.read()
                    
                # logging.warning("Dados: " + str(dados)) 
            else:
                print("Erro")
            
            obj_porta.close()
        
        except serial.SerialException:
            messagebox.showwarning("Falha", "Verifique se existe algum dispositivo conectado na porta serial!")
            # logging.error("ERRO: Verifique se ha algum dispositivo conectado na porta serial!")
        
        return dados
    
