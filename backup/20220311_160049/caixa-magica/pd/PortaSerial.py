import serial
from SocketUDP import SocketUDP
from tkinter import messagebox
import logging
class PortaSerial():
        
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
            texto.append('/dev/ttyS0')#Porta padrão do Raspberry Pi
            #texto.append('COM5')#Porta para teste no Windows
            texto.append(':')
            texto.append('9600')#Baud rate padrão do GPS
            arq.writelines(texto)
            arq.close()
            arq = open('serial.cfg', 'r')
            default=arq.read()
            return default    


    def read_bus_company(self):
        try:
            arq_bus = open('bus_company.cfg', 'r')
            print ('Arquivo config bus encontrado!')
            config=arq_bus.read()
            return config
        except IOError:
            print ('Arquivo de config bus não encontrado! Criando configuração padrão.')
            arq = open('bus_company.cfg', 'w')
            texto = []
            texto.append('1')#Empresa padrão 1
            texto.append(';')
            texto.append('1')#Onibus padrão 1
            arq.writelines(texto)
            arq.close()
            arq = open('bus_company.cfg', 'r')
            default=arq.read()
            return default
     
    def extrair_latitude_longitude(self, line):
        try:
            logging.warning("Extraindo informação latitude e longitude: " + line.decode().replace('\r\n',''))
            print("Extraindo informação latitude e longitude: ", line)
            
            try:
                line_decoded = line.decode() 
                values = line_decoded.split(",")  
            except Exception:
                values = line.split(",")
            #Dados para teste    
            #values = ['$GPRMC','132321.000','A','2214.70','S','04528.57','W','0.00','','050719','','','A*73']  
                
            if values[2]=="A":
                lat = "" ##Latitude teste
                long = "" ##Longitute teste
                
                if values[4]=="S":
                    lat = "-"
                    
                if values[3]!='':
                    logging.warning('NS Indicador: '+ values[4])
                    logging.warning('Latitude recebida: '+ values[3])
                    print('NS Indicador: ', values[4])
                    print('Latitude recebida: ', values[3])
                    aux = values[3]
                    aux = aux.replace(".","")
                    aux_end = aux[0:2]
                    ##Formatando a saida
                    aux_end = aux_end + "." +aux[2:]
                    lat = lat + aux_end
                    print('Latitude formatada: ', lat)
                    logging.warning('Latitude formatada: ' + lat)
                else:
                    logging.warning('Sem latitude')
                    print('Sem latitude')        
                    
                if values[6]=='W':
                    long = "-"
                    
                if values[5]!='':
                    logging.warning('EW Indicador: '+ values[6])
                    logging.warning('Longitude recebida: '+ values[5])
                    print('EW Indicador: ', values[6])
                    print('Longitude recebida: ', values[5])    
                    aux = values[5]
                    aux = aux.replace(".","")
                    aux_end = aux[0:3]
                    ##Formatando a saida
                    aux_end = aux_end + "." + aux[3:]
                    long = long + aux_end
                    print('Longitude formatada: ', long)
                    logging.warning('Longitude formatada: ' + long)
                else:
                    logging.warning('Sem longitude')
                    print('Sem longitute')
            else:
                logging.warning('Dados inválidos, sem posição do GPS')
                print('Dados inválidos, sem posição do GPS')
                  
        except Exception:
            lat = "" ##Latitude 
            long = "" ##Longitute

        return (lat+";"+long)
     
    ################    FUNCAO PARA ESCREVER NA PORTA ####################
    #def escrever_porta():
    # 
    #   try:
    # 
    #       valor = (raw_input("Digite o valor a ser enviado: "))
    #       Obj_porta = serial.Serial(porta, baud_rate)
    #       Obj_porta.write(valor)
    #       Obj_porta.close()
    # 
    #   except serial.SerialException:
    #       print"ERRO: Verifique se ha algum dispositivo conectado na porta!"
    # 
    #   return valor
     
    ########################## FUNCAO PARA LER A PORTA #######################
    def ler_porta(self,values):
        dados_validos = False
        try:
            aux = values.split(":")
            porta = aux[0]
            baud_rate = aux[1]
        except Exception:
            logging.error("Falha ao obter a configuração da porta serial")
            #porta = '/dev/ttyS0'
            porta = 'COM5'
            baud_rate = 9600

        try:
            obj_porta = serial.Serial(porta, baud_rate)
            while obj_porta.inWaiting:                   
                line = obj_porta.readline()
                print("Valor lido da Serial: ",line)
                logging.warning("Dados recebidos: " + line.decode().replace('\r\n',''))
                #Compare MESSAGE ID do extract information
                try:
                    if 'GPRMC' in line.decode():
                        socket = SocketUDP()
                        #Read data Company and Bus
                        company_bus = self.read_bus_company()

                        lat_long = self.extrair_latitude_longitude(line)
                        if lat_long!=";":                            
                            #Convert to byte array to send
                            message_complete = (company_bus + ";"+ lat_long).encode('utf-8')
                            #Read config server UDP
                            server = socket.read_config_server_udp();
                            #Send packet to socket
                            socket.send_message(server, message_complete)
                            obj_porta.close()
                            dados_validos = True
                        else:
                            dados_validos = False
                        
                        break;
                except Exception:
                    dados_validos = False
                    obj_porta.close()
                    break;            
        except Exception as e:
            print("Deu pau", e)
            messagebox.showwarning("Falha", "Verifique se existe algum dispositivo conectado na porta serial!")
            logging.error("ERRO: Verifique se ha algum dispositivo conectado na porta serial!")

        return dados_validos
    
    
    def read_config_serial_rfid(self):
        try:
            arq = open('serial_rfid.cfg', 'r')
            print ('Arquivo config serial encontrado!')
            config=arq.read()
            return config
        except IOError:
            print ('Arquivo de serial_rfid serial não encontrado! Criando configuração padrão.')
            arq = open('serial_rfid.cfg', 'w')
            texto = []
            texto.append('/dev/ttyACM0')#Porta padrão do Raspberry Pi
            #texto.append('COM6')#Porta para teste no Windows
            texto.append(':')
            texto.append('115200')#Baud rate padrão do leitor RFID
            arq.writelines(texto)
            arq.close()
            arq = open('serial_rfid.cfg', 'r')
            default=arq.read()
            return default    
    
    
    def escrever_porta_rfid(self, config, comand):
        dados = [0]*1
        try:
            aux = config.split(":")
            porta = aux[0]
            baud_rate = aux[1]
        except Exception:
            logging.error("Falha ao obter a configuração da porta serial do leitor RFID")
            porta = '/dev/ttyACM0'
            #porta = 'COM6'
            baud_rate = 115200
            
        try:
            obj_porta = serial.Serial(porta, baud_rate)
            #logging.warning("Enviando comando: " + str(comand))
            obj_porta.write(comand)
            
            response = obj_porta.read()
            #logging.warning("Response: " + response.hex())
            print("Response: ", response)
            if response.hex()=='bd':
                data_size = obj_porta.read()
                size = int.from_bytes(data_size, "big")
                #logging.warning("Tamanho resposta RFID: " + str(size))
                #print("Response RFID size: ", size)
                dados = [0]*size
                
                for i in range(size):
                    dados[i] = obj_porta.read()
                    
                #logging.warning("Dados lidos RFID: " + str(dados))
            obj_porta.close()
        except Exception as e:
            print("deu pau 2", e)
            #messagebox.showwarning("Falha", "Verifique se existe algum dispositivo conectado na porta serial RFID!")
            #logging.error("ERRO: Verifique se ha algum dispositivo conectado na porta serial RFID!")
        
        return dados    
