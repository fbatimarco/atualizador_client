from tkinter import *
import tkinter as tk
import time
from datetime import datetime
from threading import Thread
from PortaSerial import PortaSerial
from EditWindow import EditWindow
from CommandsMifare import CommandsMifare
import logging
import Banco
import Usuarios
import Beneficios
import Configuracoes
import RPi.GPIO as gpio
import Constants
from HttpConnection import HttpConnection
from CommandsBiometric import CommandsBiometric
from Usuarios import Usuarios
from Beneficios import Beneficios
from Beneficios import Periodos
from Configuracoes import Instalacao
from Configuracoes import MatrizHoraria
from tkinter import messagebox
from InstallWindow import InstallWindow


class Application:
    def __init__(self, master=None):
        pass
    
def atualizar_dados_interface(event):
    global update_dados
    try:
        v = read_dados()
        linha_info.set(v)
    except:
        pass
    
    update_dados = False
        
#Comando do botão Editar
def comando_editar_valores():
    logging.warning('Editando valores')
    print('Editando valores')
    global update_dados
    update_dados = True
    window = EditWindow()
    window.focus_force()
    window.attributes('-fullscreen',True)
    window.transient(root)
    window.bind("<Destroy>", atualizar_dados_interface)
    root.wait_window(window)
    window.mainloop()

#Thread para atualizar a tempo do sistema de segundo em segundo
def atualizar_hora():
    while(running):
        now = datetime.now()
        display_time = now.strftime('%d/%m/%Y - %H:%M:%S')
        hora_texto.set(display_time)
        time.sleep(1.0)
        
        
#Thread para atualizar a label principal
def atualizar_texto_principal():
    global processando_passagem
    while(running):    
        time.sleep(0.5)
        if running and processando_passagem==0:
            linha_info_cartao_rfid.set('')
        time.sleep(0.5)    
        if running and processando_passagem==0:            
            linha_info_cartao_rfid.set('Identifique-se')
        
#Thread para ler os dados do GPS        
def ler_dados_gps():
    global update_dados
    while(0):
        if (update_dados==False):
            logging.warning('Iniciando envio de dados do GPS')
            serial = PortaSerial()
            aux = serial.read_config_serial();
            dados_validos = serial.ler_porta(aux)
            if dados_validos:
                linha_info_gps.set('Dados do GPS enviado')
                time.sleep(2.0)
                linha_info_gps.set('GPS On-line')
            else:
                linha_info_gps.set('Dados do GPS inválido')
                time.sleep(2.0)
                if running:
                    linha_info_gps.set('GPS Off-line')
            
            time.sleep(30.0)
        else:
            if running:
                linha_info_gps.set('GPS Off-line')
                time.sleep(10.0)

#Thread para realizar a leitura de cartão RFID
def ler_cartao_rfid():
    global login_ok
    global cpf
    global card_number_logado
    global credito_restante
    global update_dados
    global processando_passagem
    while(running):
        if update_dados==False:                
            cartao = selecionar_cartao_rfid()
            if len(cartao)>0 and processando_passagem == 0:
                processando_passagem = 1
                logging.warning('Cartão detectado ' + cartao)
                logar_chaves_pre_definidas()
                #Verifica se o cartão é válido
                if login_ok:
                    logging.warning('Cartão logado' + cartao)
                    #Busca o usuário no banco local
                    usuario = select_usuario_cartao(cartao)
                    #ID 0 não é utilizado para nenhum usuário, caso o id seja 0, não foi encontrado
                    if usuario is not None and usuario.id > 0:
                        #Faz o processamento da passagem caso o usuário possua crédito.
                        passagem_ok = processa_passagem_usuario(usuario)
                        if passagem_ok:
                            #Exibe mensagem ao usuário na interface
                            linha_info_cartao_rfid.set('CPF ' + cpf + ' \n R$ '+ str("{:.2f}".format(credito_restante)))
                            print('Passagem processada com sucesso')
                            logging.warning('Passagem processada com sucesso, cartão: ' + cartao)    
                        else:
                            #Exibe mensagem ao usuário na interface
                            linha_info_cartao_rfid.set('Saldo insuficiente \n R$ '+ str("{:.2f}".format(credito_restante)))
                            print('Passagem não processada')
                            logging.warning('Passagem não processada, saldo insuficiente, cartão: ' + cartao)
                    else:
                        #Exibe mensagem ao usuário na interface
                        linha_info_cartao_rfid.set('Usuário não encontrado')
                        logging.warning('Usuário não encontrado para cartão:' + cartao)                        
                else :
                    #Exibe mensagem ao usuário na interface
                    linha_info_cartao_rfid.set('Cartão inválido')
                    logging.warning('Cartão inválido:' + cartao)
            #Caso consiga detectar um cartão aguarda 5 segundos com a mensagem na tela
            time.sleep(5.0)
            processando_passagem = 0
            #Lê cartão a cada 500ms
            time.sleep(0.5)
        
        
#Thread para realizar a leitura da biometria
def ler_biometria():
    global login_ok
    global cpf
    global credito_restante
    global update_dados
    global  rresultado_load_libesultado_load_lib
    global processando_passagem
    amostra = bytes(b'\x00')*Constants.TAM_TMP_FINGERPRINT
    while(running):
        if running==True and update_dados==False:
            if resultado_load_lib==Constants.COMANDO_EXECUTADO_COM_SUCESSO:
                biometrics = CommandsBiometric()
                amostra = biometrics.enroll_fingerprint_cis()
                if update_dados==False and processando_passagem == 0:
                    processando_passagem = 1
                    if len(amostra) > 1: 
                        cpf = biometrics.check_template_fingerprint(amostra)
                        if len(cpf)>1 and len(cpf)==Constants.TAM_MIN_CPF:
                            logging.warning("Digital encontrada com sucesso")
                            
                            passagem_ok = select_usuario(cpf)
                            if passagem_ok:
                                linha_info_cartao_rfid.set('CPF ' + cpf + ' \n R$ '+ str("{:.2f}".format(credito_restante)))
                                print('Passagem processada com sucesso')
                                logging.warning('Passagem processada com sucesso, CPF: ' + cpf)
                                #Pulso nos pinos 38 e 40
                                pulsar_pinos()
                            else:
                                linha_info_cartao_rfid.set('Saldo insuficiente \n R$ '+ str("{:.2f}".format(credito_restante)))
                                print('Passagem não processada')
                                logging.warning('Passagem não processada, saldo insuficiente, CPF: ' + cpf)                        
                        else :
                            logging.warning("Digital não encontrada")
                            linha_info_cartao_rfid.set('Digital não encontrada')                        
            
                        time.sleep(5.0)
                        processando_passagem = 0
        
#Seleciona usuário no banco de dados        
def select_usuario(cpf_user):
    global credito_restante
    global passagens_processadas
    print('Buscando CPF: ', cpf_user)
    usuario = Usuarios()
    r = usuario.select_user_by_cpf(cpf_user)
    print('Response: ',r)
    print('ID: ', usuario.id)
    print('CPF: ', usuario.cpf)
    print('Fingerprint: ', usuario.arq_digitais)
    print('Crédito: ', usuario.valor_credito)
    print('Passagens: ', usuario.numero_passagens)
    
    
    #Obtem o valor da passagem
    values = read_dados().split(' - ')
    aux = values[1].split(" ")
    v_passagem = float(aux[1].replace(',','.'))
    print('Valor passagem: ', v_passagem)
    credito_usuario = float(usuario.valor_credito)
    if credito_usuario >= v_passagem:
        credito_restante = float(credito_usuario - v_passagem)
        print('Credito restante: ', float("{0:.2f}".format(credito_restante)))
        logging.warning('Cartão com crédito suficiente')
        print('Cartao com crédito')
        usuario.valor_credito = str(credito_restante)
        passagem_ok = usuario.update_user()
        if passagem_ok:
            passagens_processadas += 1
            logging.warning('Cartão com crédito suficiente')
            print('Cartao com crédito')                    
        else:
            logging.warning('Falha na gravação do crédito restante')
            print('Falha na gravação do crédito restante')                              
    else:
        credito_restante = float(usuario.valor_credito)
        passagem_ok = False
        logging.warning('Cartão sem crédito suficiente')
        print('Cartao sem crédito')  

    return passagem_ok

#Seleciona usuário no banco de dados 
def select_usuario_cartao(cartao_user):
    print('Buscando cartão: ', cartao_user)
    usuario = Usuarios()

    try:
        r = usuario.select_user_by_cartao(cartao_user)
        print('Response: ',r)
        print('ID: ', usuario.id)
        print('CPF: ', usuario.cpf)
        print('Fingerprint: ', usuario.arq_digitais)
        print('Crédito: ', usuario.valor_credito)
        print('Passagens: ', usuario.numero_passagens)       
    except:
        pass
    
    return usuario

#Processa passagem para o usuário       
def processa_passagem_usuario(usuario):
    global credito_restante
    global passagens_processadas
    print('Processando passagem usuário: ', usuario.cpf)
    beneficio = Beneficios()
    desconto_beneficio = beneficio.select_beneficio_by_usuario_id(usuario.id)
    
    #Obtem o valor da passagem
    values = read_dados().split(' - ')
    aux = values[1].split(" ")
    v_passagem = float(aux[1].replace(',','.'))
    print('Valor passagem: ', v_passagem)
    credito_usuario = float(usuario.valor_credito)
    passagem_com_desconto = (v_passagem - desconto_beneficio)
    if credito_usuario >= passagem_com_desconto:
        credito_restante = float(credito_usuario - passagem_com_desconto)
        print('Credito restante: ', float("{0:.2f}".format(credito_restante)))
        logging.warning('Cartão com crédito suficiente')
        print('Cartao com crédito')
        usuario.valor_credito = str(credito_restante)
        passagem_ok = usuario.update_user()

        if passagem_ok:
            logging.warning('Crédito do usuário atualizado!')
            passagens_processadas += 1
            print('Crédito do usuário atualizado!')
        else:
            logging.warning('Falha na atualização do crédito!')
            print('Falha na atualização do crédito!')
    else:
        credito_restante = float(usuario.valor_credito)
        passagem_ok = False
        logging.warning('Crédito insuficiente!')
        print('Crédito insuficiente!')

    return passagem_ok
    
#Leitura de dados do arquivo com as informações da linha        
def read_dados():
    try:
        arq = open('config.cfg', 'r')
        texto=arq.read()
        return texto
    except IOError:
        logging.warning('Arquivo de configuração não encontrado.')
        print ('Arquivo não encontrado! Criando um arquivo padrão.')
        arq = open('config.cfg', 'w')
        texto = []
        texto.append('Linha 0000')
        texto.append(' - ')
        texto.append('R$ 5,00')
        arq.writelines(texto)
        arq.close()
        arq = open('config.cfg', 'r')
        t=arq.read()
        return t
#Comando do clique do botão direito para abertura de janela para edição de dados    
def popup(event):
    comando_editar_valores()   


#Comando do clique do botão direito para abertura de janela para fechar o turno    
def popup_fechar(event):
    mensagem_encerramento()
    

#Leitura de cartão RFID    
def selecionar_cartao_rfid():
    global card_number_logado
    serial = PortaSerial()
    commands = CommandsMifare()
    cmd = commands.command_select_card()
    print('Command select card', cmd)
    logging.warning('Command select card' + str(cmd))
    config = serial.read_config_serial_rfid();
    data_received = serial.escrever_porta_rfid(config, cmd)
    logging.warning("Cartão selecionado: " + str(data_received))
    print("Resposta completa da leitura do cartão:", str(data_received))    
    #Se for 0x00 - Leitura ok
    str_card_number = ''
    complete_response = ''
    print(len(data_received))
    if len(data_received)>1 and data_received[1].hex()=='00':
        #Descarta Tipo do cartão e BCC  
        size_data = len(data_received) - 2
        card_number = data_received[2:size_data]
        card_number_logado = data_received[2:size_data]

        #Converte o dado em número do cartão
        for i in range(len(card_number)):
            str_card_number += card_number[i].hex()
        
        print("Dados do cartão", str(card_number))
        logging.warning('Cartão: '+ str_card_number.upper())
        complete_response = 'Cartão: '+ str_card_number.upper()
         
    return complete_response     

#Login no cartão RFID com chaves pré-armazenas
def logar_chaves_pre_definidas():
    global card_number_logado
    global login_ok
    card_number = selecionar_cartao_rfid().upper()
    sector_data = 0x01
    if len(card_number)>0:
        login_ok = False
        serial = PortaSerial()
        commands = CommandsMifare()
        kt = 0x60
        list_keys = commands.get_keys_predefined()
        for i in range(len(list_keys)):
            card_number = selecionar_cartao_rfid().upper()
            if len(card_number)>0:
                print('Tentativa de login com chave: ', i)
                logging.warning("Tentativa de login no setor 1 com chave " + str(i))
                cmd = commands.command_login_sector(sector_data, kt, list_keys[i])        
                print('Command write ', cmd)
                config = serial.read_config_serial_rfid();
                data_received = serial.escrever_porta_rfid(config, cmd)
                login_ok = False
                if len(data_received)>1:                    
                    if data_received[1].hex()=='00':
                        logging.warning('\nCartão: ' +  card_number + ' - Login OK\n')
                        login_ok = True
                        break
                    if data_received[1].hex()=='03':
                        logging.warning('\nCartão: '+ card_number + ' - Falha no Login\n')
                        
                    if data_received[1].hex()=='F0':
                        resultado_comando.set('\nCartão: ' + card_number + ' - Erro de Checksum\n')
                        
                    print("Resposta do login", str(data_received))
                    logging.warning("Resposta do login" + str(data_received))
            
    if login_ok:
        print('Logado com sucesso!')
    else:
        print('Falha no login')
    
    return login_ok

#Leitura de dados do cartão - Informação para validação do cartão
def read_card_data_info():
    global card_number_logado
    global login_ok
    global cpf
    cartao_valido = False
    if login_ok:
        serial = PortaSerial()
        commands = CommandsMifare()
        cmd = commands.command_read_data_info()
        print('Command write ', cmd)
        config = serial.read_config_serial_rfid();
        data_received = serial.escrever_porta_rfid(config, cmd)
        if len(data_received)>1:
            print("Dados na resposta da leitura dos dados", str(data_received))
            logging.warning("Resposta da leitura" + str(data_received))
            if data_received[1].hex()=='00':
                logging.warning('\nSucesso na leitura de dados do cartão: ' +  str(card_number_logado)  + '\n')
                card = [0]*6
                if len(card_number_logado)==6:        
                    card[0] = card_number_logado[5]
                    card[1] = card_number_logado[4]
                    card[2] = card_number_logado[3]
                    card[3] = card_number_logado[2]
                    card[4] = card_number_logado[1]
                    card[5] = card_number_logado[0]
                
                if len(card_number_logado)==5:        
                    card[0] = card_number_logado[4]
                    card[1] = card_number_logado[3]
                    card[2] = card_number_logado[2]
                    card[3] = card_number_logado[1]
                    card[4] = card_number_logado[0]
                    card[5] = data_received[17]  
                    
                if len(card_number_logado)==4:        
                    card[0] = card_number_logado[3]
                    card[1] = card_number_logado[2]
                    card[2] = card_number_logado[1]
                    card[3] = card_number_logado[0]
                    card[4] = data_received[17]
                    card[5] = data_received[17]                    
                
                print('Card number logado: ', card_number_logado)

                if card[0]==data_received[16] and card[1]==data_received[15] and card[2]==data_received[14] and card[3]==data_received[2] and card[4]==data_received[17]:
                    #Limpa o CPF
                    cpf = ''
                    #Retira o CPF da resposta recebida
                    for i in range(11):
                        cpf +=  str(int.from_bytes(data_received[3+i], byteorder='big', signed=True))
                    
                    print('CPF lido', cpf)    
                    
                    cartao_valido = True
                    print('Cartao OK')
                else:
                    cartao_valido = False
                    print('Cartao NOK')
                
                
            if data_received[1].hex()=='04':
                logging.warning('Falha ao ler dados do cartão: '+ card_number_logado + '\n')
            if data_received[1].hex()=='F0':
                resultado_comando.set('\nCartão: ' + card_number_logado + ' - Erro de Checksum\n')
    return cartao_valido


#Leitura de dados do cartão - Informação para verificaçao do crédito
def read_card_credito_info():
    global card_number_logado
    global login_ok
    global credito_restante
    passagem_ok = False
    if login_ok:
        serial = PortaSerial()
        commands = CommandsMifare()
        cmd = commands.command_read_info_credit()
        print('Command write ', cmd)
        config = serial.read_config_serial_rfid();
        data_received = serial.escrever_porta_rfid(config, cmd)
        if len(data_received)>1:
            print("Dados na resposta da leitura dos dados", str(data_received))
            logging.warning("Resposta da leitura" + str(data_received))
            if data_received[1].hex()=='00':
                logging.warning('\nSucesso na leitura de dados do cartão: ' +  str(card_number_logado)  + '\n')
                #Obtem o valor da passagem
                values = read_dados().split(' - ')
                aux = values[1].split(" ")
                v_passagem = float(aux[1].replace(',','.'))
                print('Valor passagem: ', v_passagem)
                #Obtem os centavos gravados no cartão
                uni_centavos = int.from_bytes(data_received[13], byteorder='big', signed=True)
                
                dez_centavos = int.from_bytes(data_received[12], byteorder='big', signed=True)
                centavos = float(((dez_centavos*10)+uni_centavos)/100)
                #Obtem os reais gravados no cartão
                reais = int.from_bytes(data_received[11], byteorder='big', signed=True)
                r = int.from_bytes(data_received[10], byteorder='big', signed=True)
                reais = reais + (r*10)
                r = int.from_bytes(data_received[9], byteorder='big', signed=True)
                reais = reais + (r*100)
                r = int.from_bytes(data_received[8], byteorder='big', signed=True)
                reais = reais + (r*1000)
                print('Crédito: Reais: ', reais , 'Centavos', centavos)
                
                credito_completo = float(reais)
                credito_completo += float(centavos)
                
                print('Credito completo: ', credito_completo)
                
                if credito_completo >= v_passagem:
                    credito_restante = float(credito_completo - v_passagem)
                    print('Credito restante: ', float("{0:.2f}".format(credito_restante)))
                    logging.warning('Cartão com crédito suficiente')
                    print('Cartao com crédito')
                    passagem_ok = gravar_data_credito()
                    if passagem_ok:                        
                        logging.warning('Cartão com crédito suficiente')
                        print('Cartao com crédito')                    
                    else:
                        logging.warning('Falha na gravação dos dados do cartão')
                        print('Falha na gravação dos dados do cartão')                              
                else:
                    credito_restante = credito_completo
                    passagem_ok = False
                    logging.warning('Cartão sem crédito suficiente')
                    print('Cartao sem crédito')                
                
            if data_received[1].hex()=='04':
                logging.warning('Falha ao ler dados do cartão')
            if data_received[1].hex()=='F0':
                resultado_comando.set('Erro de Checksum')
                
    return passagem_ok

def gravar_data_credito():
    debito_ok = False
    global card_number_logado
    global credito_restante
    
    if login_ok == True:
        serial = PortaSerial()
        commands = CommandsMifare()
        cpf_u = [0]*11
        cpf_u[0] = int(cpf[0],16)
        cpf_u[1] = int(cpf[1],16)
        cpf_u[2] = int(cpf[2],16)
        cpf_u[3] = int(cpf[3],16)
        cpf_u[4] = int(cpf[4],16)
        cpf_u[5] = int(cpf[5],16)
        cpf_u[6] = int(cpf[6],16)
        cpf_u[7] = int(cpf[7],16)
        cpf_u[8] = int(cpf[8],16)
        cpf_u[9] = int(cpf[9],16)
        cpf_u[10] = int(cpf[10],16)
    
        card = [0]*6
        card[0] = '00'
        card[1] = '00'
        card[2] = '00'
        card[3] = '00'
        
        if len(card_number_logado)==6:        
            card[0] = card_number_logado[5]
            card[1] = card_number_logado[4]
            card[2] = card_number_logado[3]
            card[3] = card_number_logado[2]
            card[4] = card_number_logado[1]
            card[5] = card_number_logado[0]
        
        if len(card_number_logado)==5:        
            card[1] = card_number_logado[4]
            card[2] = card_number_logado[3]
            card[3] = card_number_logado[2]
            card[4] = card_number_logado[1]
            card[5] = card_number_logado[0]
               
            
        if len(card_number_logado)==4:        
            card[2] = card_number_logado[3]
            card[3] = card_number_logado[2]
            card[4] = card_number_logado[1]
            card[5] = card_number_logado[0]
   
   
        saldo = str(round(credito_restante,2)).split('.')
        
        r = ('0000'+saldo[0])[-4:]
        real = [0]*4
        real[0] = int(r[3])
        real[1] = int(r[2])
        real[2] = int(r[1])
        real[3] = int(r[0])
         
        cent  = saldo[1] 
        centavos = [0]*2
        
        #Quando valor redondo em centavos, completa com 0 a direita
        if len(str(cent))==1: 
            centavos[0] = 0x00
            centavos[1] = int(cent[0])            
        else:
            centavos[0] = int(cent[1])
            centavos[1] = int(cent[0])
        
        #Obtendo dados da linha de onibus
        values = read_dados().split(' - ')
        aux = values[0].split(" ")
        d_linha = ('0000'+aux[1])[-4:]
        print('Linha: ', d_linha)
        #Adiciona os dados da linha no vetor para gravação
        linha=[0]*4
        linha[0] = int(d_linha[0],16)
        linha[1] = int(d_linha[1],16)
        linha[2] = int(d_linha[2],16)
        linha[3] = int(d_linha[3],16)
        
        cmd = commands.command_write_info_credit(cpf_u, card, real, centavos, linha)
        print('Command write ', cmd)
        config = serial.read_config_serial_rfid();
        data_received = serial.escrever_porta_rfid(config, cmd)
        
        if data_received[1].hex()=='00':
            debito_ok = True
            #Pulso nos pinos 38 e 40
            pulsar_pinos()
            print('Gravação de créditos OK')
            
            #Monta vetor com data e hora para log
            today = datetime.now()
            #Formata os dados para gravação
            day = ('00'+str(today.day))[-2:]
            month = ('00'+str(today.month))[-2:]
            year = ('0000'+str(today.year))[-4:]
            hour = ('00'+str(today.hour))[-2:]
            minute = ('00'+str(today.minute))[-2:]
            second = ('00'+str(today.second))[-2:]
            data_hora = [0]*14
            #Dia
            data_hora[0]=int(day[0])
            data_hora[1]=int(day[1])
            #Mes
            data_hora[2]=int(month[0])
            data_hora[3]=int(month[1])
            #Ano
            data_hora[4]=int(year[0])
            data_hora[5]=int(year[1])
            data_hora[6]=int(year[2])
            data_hora[7]=int(year[3])
            #Hora
            data_hora[8]=int(hour[0])
            data_hora[9]=int(hour[1])
            #Minuto
            data_hora[10]=int(minute[0])
            data_hora[11]=int(minute[1])
            #Segundo
            data_hora[12]=int(second[0])
            data_hora[13]=int(second[1])
            
            cmd = commands.command_write_data_hora_log(data_hora)
            print('Command write ', cmd)
            config = serial.read_config_serial_rfid();
            data_received_log = serial.escrever_porta_rfid(config, cmd)
            if data_received_log[1].hex()=='00':
                logging.warning('Gravação de logs no cartão realizado')
                print('Gravação de logs OK')
            if data_received_log[1].hex()=='05':
                print('Falha na gravação dos logs, erro EEPROM')
            if data_received_log[1].hex()=='F0':
                print('Falha na gravação dos log, erro de Checksum')

        if data_received[1].hex()=='05':
            debito_ok = False
            print('Falha na gravação do credito, erro EEPROM')
        if data_received[1].hex()=='F0':
            debito_ok = False
            print('Falha na gravação do crédito, erro de Checksum')
            
        print("Resposta da gravação", str(data_received))
        logging.warning("Resposta da gravação" + str(data_received))
    else:
        logging.error("ERRO: Realize o login em um cartão para gravar os dados")
    
    return debito_ok

MESSAGE_WARNING_DURATION = 5000

def center(win):
    """
    centers a tkinter window
    :param win: the root or Toplevel window to center
    """
    win.update_idletasks()
    width = win.winfo_width()
    frm_width = win.winfo_rootx() - win.winfo_x()
    win_width = width + 2 * frm_width
    height = win.winfo_height()
    titlebar_height = win.winfo_rooty() - win.winfo_y()
    win_height = height + titlebar_height + frm_width
    x = win.winfo_screenwidth() // 2 - win_width // 2
    y = win.winfo_screenheight() // 2 - win_height // 2
    win.geometry('{}x{}+{}+{}'.format(width, height, x, y))
    win.deiconify()


def warning_user():
    top = Toplevel(bg='white')
    top.geometry("600x90") #Width x Height
    top.overrideredirect(True)
    center(top)
    message_user = Message(top, font=fonte, justify=CENTER)
    message_user['textvariable'] = linha_info_cartao_rfid
    message_user['bg'] = 'black'
    message_user['fg'] = 'white'
    message_user['width'] = 600
    message_user.pack(fill=BOTH)
    top.after(MESSAGE_WARNING_DURATION, top.destroy)


def pulsar_pinos():
    print('Acionando pinos')
    logging.warning('Acionando pinos 38 e 40')
    gpio.output(38,1)
    gpio.output(40,1)
    time.sleep(0.5)
    gpio.output(38,0)
    gpio.output(40,0)
    print('Desacionando pinos')
    logging.warning('Desligando pinos 38 e 40')


#Inicia o software    
def load_library():
    global resultado_load_lib
    biometrics = CommandsBiometric()
    resultado_load = biometrics.init_cis()
    return resultado_load


#Encerra o software    
def fechar_programa():
    global running
    running = 0
    biometrics = CommandsBiometric()
    biometrics.finish_cis() 
    print("Good bye.....")
    quit()

    

#Verifica inicializaçao diária
def check_inicializacao_diaria():
    global update_dados
    instalacao = Instalacao()   
    #Obtém o serial do Raspberry
    num_serie = str(get_serial())

    instalacao.select_instalacao_by_num_serie(num_serie)
    mat_horaria = MatrizHoraria()
    mat_horaria.select_matriz_horaria_by_veiculo(instalacao.veiculo)

    if mat_horaria.id == 0:
        http_connection = HttpConnection()
        json_inicializacao = http_connection.get_inicializacao_diaria(instalacao.acesso)
        
        mat_horaria.veiculo = json_inicializacao['veiculo']
        mat_horaria.chave_responsavel = json_inicializacao['chaveDoResponsavel']
        mat_horaria.feriado = json_inicializacao['feriado']
        mat_horaria.id_linha = json_inicializacao['linha']['idLinha']
        mat_horaria.nome_linha = json_inicializacao['linha']['nome']
        mat_horaria.dia_semana = json_inicializacao['horarioViagem']['diaSemana']
        mat_horaria.horario = json_inicializacao['horarioViagem']['horario']
        mat_horaria.motivo = json_inicializacao['viagem']['motivo']
        mat_horaria.tipo_viagem = json_inicializacao['viagem']['tipoViagem']
        
        #Inserção dos dados recebidos no banco de dados
        mat_horaria.insert_matriz_horaria()
        print("Matriz horária criada!")
    else:
        print("Matriz horária já existe!")


#Realiza o fechamento do turno
def fechamento_do_turno():
    instalacao = Instalacao()
    #Obtém o serial do Raspberry
    num_serie = str(get_serial())

    instalacao.select_instalacao_by_num_serie(num_serie)
    mat_horaria = MatrizHoraria()
    mat_horaria.select_matriz_horaria_by_veiculo(instalacao.veiculo)
    mat_horaria.delete_matriz_horaria()
    print("Remoção da matriz horária!")
    print("Turno fechado!")


#Verifica se ja foi realizada a instalação do equipamento
def verifica_instalacao():
    instalacao = Instalacao()
    #Obtém o serial do Raspberry
    num_serie = str(get_serial())
    instalacao.select_instalacao_by_num_serie(num_serie)
    if instalacao.id == 0:
        print("Sem instalação!")
        iniciar_instalacao()

    else:
        print("Já existe a configuração da instalação!")



#Inicia os procedimentos de instalação
def iniciar_instalacao():
    logging.warning('Instalando equipamento')
    print('Instalando equipamento')
    window = InstallWindow()
    window.focus_force()
    window.attributes('-fullscreen',True)
    window.transient(root)
    root.wait_window(window)

    http_connection = HttpConnection()
    instalacao = Instalacao()
    #Obtem o serial do Raspberry
    num_serie = str(get_serial())
    instalacao.num_serie = num_serie
    try:
        instalacao.veiculo = window.get_veiculo()
        instalacao.token = "hash"
        instalacao.instalacao = window.get_numero_instalacao()
        #Faz o request do restante da configuração
        jsonResponse = http_connection.put_requisicao_instalacao(instalacao)
        instalacao.operadora = jsonResponse['operadora']
        instalacao.acesso = jsonResponse['acesso']
        instalacao.caixa_id = jsonResponse['id']
        instalacao.bilhetadoraId = jsonResponse['operadora']['bilhetadoraId']
        print(instalacao.caixa_id)
        instalacao.insert_instalacao()
        print("Instalação concluída!")
    except:
#        tk.messagebox.showerror('Aviso','Instalação cancelada!')
        print("Cancelando instalação....good bye.....")
        quit()
        
#Exibe a mensagem da inicialização diária
def mensagem_inicializacao():
    MsgBox = tk.messagebox.askquestion ('Inicialização Diária','Deseja realizar a inicialização da matriz horária?',icon = 'question')
    if MsgBox == 'yes':
        try:
            #Realiza a inicialização da matriz horária
            check_inicializacao_diaria()
            tk.messagebox.showinfo('Aviso','Inicialização diária realizada com sucesso!')
        except:
            tk.messagebox.showerror('Aviso','Inicialização diária mal sucedida!')
            fechar_programa()
    else:
        tk.messagebox.showinfo('Aviso','Inicialização diária cancelada, a aplicação será finalizada!')
        fechar_programa()

#Exibe a mensagem de fechamento de turno
def mensagem_encerramento():
    global passagens_processadas
    MsgBox = tk.messagebox.askquestion ('Fechamento','Deseja realizar o fechamento do turno?',icon = 'question')
    if MsgBox == 'yes':
        try:
            #Realiza o fechamento do turno
            fechamento_do_turno()
            texto_finalizacao = "Fechamento do turno relizado com sucesso!\n Passagens processadas: " + str(passagens_processadas)
            tk.messagebox.showinfo('Fechamento do turno', texto_finalizacao)
            passagens_processadas = 0
        except:
            tk.messagebox.showerror('Aviso','Fechamento do turno mal sucedida!')

        fechar_programa()
    else:
        print('Continua....')



#Obtém o número serial do Raspberry Pi
def get_serial():
  # Extrai o serial do arquivo 'cpuinfo'
  cpuserial = "0000000000000000"
  try:
    f = open('/proc/cpuinfo','r')
    for line in f:
      if line[0:6]=='Serial':
        cpuserial = line[10:26]
    f.close()
  except:
    cpuserial = "ERROR00000000000"
 
  return cpuserial


#Criação da root principal
root = Tk()
logging.basicConfig(filename='app.log', filemode='a', format='%(asctime)s - %(message)s')
running = 1
update_values = 0
processando_passagem = 0
fonte = ("Verdana 20 bold")
fonte_info = ("Verdana 30 bold")
#Título da root
root.title('Caixa Mágica')
#frame master
root.frame_master = Frame()
root.frame_master["pady"] = 10
root.frame_master.configure(bg='black')
root.frame_master.pack(fill='both', expand=True)
update_dados = False
#Deixa a root em tela cheia
root.attributes('-fullscreen',True)
#root.resizable(False, False)

card_number_logado = ['0']*12
login_ok = False
cpf = ''
credito_restante = 0.00

#Load DLL
resultado_load_lib = load_library()

#Definindo os pinos
gpio.setmode(gpio.BOARD)
gpio.setwarnings(False)
gpio.setup(38,gpio.OUT)
gpio.setup(40,gpio.OUT)

#frame titulo
root.frame_titulo = Frame(root.frame_master)
#root.frame_titulo.configure(bg='black')
root.frame_titulo.pack(side = 'top',fill='both', expand=True)

lbl_principal = Label(root.frame_titulo, text='CAIXA MÁGICA', fg='white', bg='black',font=fonte, width='500')
lbl_principal.pack(side="top")
#titulo_principal.place(x=0,y=0)

#frame imagem
root.frame_imagem = Frame(root.frame_master)
#root.frame_imagem.configure(bg='gray')
root.frame_imagem.pack(fill='both', expand=True)

linha_info_cartao_rfid = StringVar()
valor_passagem = StringVar()
dados_linha = StringVar()
hora_texto = StringVar()
linha_info = StringVar()
linha_info_gps = StringVar()

#Variável que armazena o total de passagens processadas
passagens_processadas = 0

#imagem = PhotoImage(file="principal.png")
w = Label(root.frame_imagem, textvariable=linha_info_cartao_rfid, font = fonte_info)
w.pack(fill=BOTH, expand=True)
linha_info_cartao_rfid.set('Identifique-se')

root.frame_gps = Frame(root.frame_master)
root.frame_gps.configure(bg='black')
root.frame_gps.pack(side="bottom", fill='x')

lbl_mensagem_gps = Label(root.frame_gps, textvariable=linha_info_gps, fg='white', bg='black', font='Verdana 10 bold')
lbl_mensagem_gps.pack(side='right')

#Exibe o resultado da leitura do cartão
#lbl_mensagem_cartao = Label(root.frame_gps, textvariable=linha_info_cartao_rfid, fg='white', bg='black', font='Verdana 20 bold')
#lbl_mensagem_cartao.pack(side='left')

#frame dados
root.frame_dados = Frame(root.frame_master)
root.frame_dados.pack(side = 'bottom', fill='both', expand=True)

linha_info.set(read_dados())
lbl_config = Label(root.frame_dados,textvariable=linha_info, fg='white', bg='black', font=fonte, width='500')
lbl_config.pack(side='bottom')

lbl_hora = Label(root.frame_dados, textvariable=hora_texto, fg='white', bg='black', font=fonte, width='500', borderwidth=10)
lbl_hora.pack(side="bottom")

PopUpMenu = Menu(lbl_config, tearoff=0)

PopUpMenu = Menu(lbl_principal, tearoff=0)

# Adiciona evento do botão direito do mouse
lbl_principal.bind("<Button-3>", popup_fechar)

# Adiciona evento do botão direito do mouse
lbl_config.bind("<Button-3>", popup)

#Verifica se precisa realizar a instalação
verifica_instalacao()

#Pergunta se deve realizar a inicialização da matriz horária
mensagem_inicializacao()

#Criação da Thread apontando para função que deve ser executada(atualização da hora)
update_hora = Thread(target=atualizar_hora)
update_hora.start()

#Criação da Thread apontando para função que deve ser executada(ler dados gps)
update_gps = Thread(target=ler_dados_gps)
update_gps.start()

#Criação da Thread apontando para função que deve ser executada(ler cartão RFID)
update_gps = Thread(target=ler_cartao_rfid)
update_gps.start()

#Criação da Thread apontando para função que deve ser executada(update label principal)
update_label = Thread(target=atualizar_texto_principal)
update_label.start()

#Criação da Thread apontando para função que deve ser executada(ler fingerprint)
read_fingerprint = Thread(target=ler_biometria)
read_fingerprint.start()

#Loop para root principal
Application(root)
root.mainloop()

#Encerra biometria e threads
fechar_programa()
