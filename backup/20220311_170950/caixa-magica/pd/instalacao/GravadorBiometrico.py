from tkinter import *
import time
from datetime import datetime
from threading import Thread
import logging
from ctypes import *
import Constants
import os
from CommandsBiometric import CommandsBiometric
from CPFWindow import CPFWindow
from Usuarios import Usuarios
import traceback
import platform

#import RPi.GPIO as gpio

class Application:
    def __init__(self, master=None):
        pass

#Thread para atualizar a tempo do sistema de segundo em segundo
def atualizar_hora():
    while(running):
        if running:        
            now = datetime.now()
            display_time = now.strftime('%d/%m/%Y - %H:%M:%S')
            hora_texto.set(display_time)
            time.sleep(1.0)
        
        
#Thread para atualizar a tempo do sistema de segundo em segundo
def update_label():
    global  resultado_load
    global root
    amostra = bytes(b'\x00')*Constants.TAM_IMG_FINGERPRINT
    while(running):
        if running:
            if resultado_load==Constants.COMANDO_EXECUTADO_COM_SUCESSO:
                biometrics = CommandsBiometric()
                linha_info_identifier.set(Constants.MENSAGEM_PADRAO)
                amostra = biometrics.enroll_fingerprint_cis()
                result = Constants.COMANDO_NAO_EXECUTADO
                if len(amostra) > 1: 
                    digital_cadastrada = Constants.DIGITAL_NAO_ENCONTRADA
                    digital_cadastrada = biometrics.compare_template_fingerprint(amostra)
                    if digital_cadastrada != Constants.DIGITAL_ENCONTRADA:
                        window = CPFWindow()
                        window.focus_force()
                        #window.attributes('-fullscreen',True)
                        window.transient(root)
                        root.wait_window(window)
    #                    window.mainloop()
                        cpf = window.get_cpf()
                    
                        if len(cpf)>0:
                            result = gravar_biometria(amostra,cpf)
                            
                        if result==Constants.COMANDO_EXECUTADO_COM_SUCESSO:        
                            linha_info_identifier.set(Constants.TXT_DIGITAL_CADASTRADA_COM_SUCESSO)
                            time.sleep(3.0)
                        else:
                            linha_info_identifier.set(Constants.TXT_DIGITAL_JA_CADASTRADA)
                            time.sleep(3.0)
                    else:
                        linha_info_identifier.set(Constants.TXT_DIGITAL_JA_CADASTRADA)
                        time.sleep(3.0)
                        linha_info_identifier.set(Constants.MENSAGEM_PADRAO)
            else:
                linha_info_identifier.set(Constants.MENSAGEM_RELOAD)
                time.sleep(1.0)
                linha_info_identifier.set(Constants.MENSAGEM_VAZIA)
                time.sleep(1.0)

def teste_usuario():
    dir_dig = os.getcwd()
    dir_dig = dir_dig + Constants.PATH_FINGERPRINTS_LINUX   
    window = CPFWindow()
    window.focus_force()
    #window.attributes('-fullscreen',True)
    window.transient(root)
    root.wait_window(window)
#                    window.mainloop()
    cpf = window.get_cpf()

    if len(cpf)>0:
        if os.path.isdir(dir_dig): # vemos de este diretorio ja existe
            print ('Ja existe uma pasta com esse nome!')
        else:
            os.mkdir(dir_dig) # aqui criamos a pasta caso nao exista
            print ('Pasta criada com sucesso!')
            
        if os.path.isfile(dir_dig + Constants.DIVISOR_PATH_LINUX + cpf+Constants.EXTENSAO_TEMPLATE): # vemos se a digital já existe
            print('CPF já cadastrado')
            linha_info_identifier.set(Constants.TXT_CPF_JA_CADASTRADO)
            response = Constants.DIGITAL_JA_CADASTRADA
        else:
            #CADASTRA A DIGITAL
            print("CADASTRANDO DIGITAL...")
            tpl = open(dir_dig+Constants.DIVISOR_PATH_LINUX+cpf+Constants.EXTENSAO_TEMPLATE,"wb")
#            tpl.write('teste'.)
            tpl.close()
            #Salva usuário
            salvar_usuario(cpf)
            response = Constants.COMANDO_EXECUTADO_COM_SUCESSO
    
    select_usuario(cpf)
    
    if Constants.COMANDO_EXECUTADO_COM_SUCESSO:        
        linha_info_identifier.set(Constants.TXT_DIGITAL_CADASTRADA_COM_SUCESSO)
        time.sleep(3.0)
    else:
        linha_info_identifier.set(Constants.MENSAGEM_RELOAD)
        time.sleep(3.0)
        linha_info_identifier.set(Constants.MENSAGEM_VAZIA)
        time.sleep(3.0)


def gravar_biometria(fingerprint, cpf):
    try: 
        dir_dig = os.getcwd()
        dir_dig = dir_dig + Constants.PATH_FINGERPRINTS_LINUX
        if os.path.isdir(dir_dig): # vemos de este diretorio ja existe
            print ('Ja existe uma pasta com esse nome!')
        else:
            os.mkdir(dir_dig) # aqui criamos a pasta caso nao exista
            print ('Pasta criada com sucesso!')
            
        if os.path.isfile(dir_dig + Constants.DIVISOR_PATH_LINUX + cpf+".tpl"): # vemos se a digital já existe
            print('Digital já cadastrada')
            linha_info_identifier.set(Constants.TXT_CPF_JA_CADASTRADO)
            response = Constants.DIGITAL_JA_CADASTRADA
        else:
            #CADASTRA A DIGITAL
            print("CADASTRANDO DIGITAL...")
            tpl = open(dir_dig + Constants.DIVISOR_PATH_LINUX + cpf+Constants.EXTENSAO_TEMPLATE,"wb")
            tpl.write(fingerprint)
            tpl.close()
            #Salva usuário
            salvar_usuario(cpf)
            response = Constants.COMANDO_EXECUTADO_COM_SUCESSO
    except:
        response = Constants.FALHA_GRAVAR_BIOMETRIA
    
    return response

def salvar_usuario(cpf):
    try:
        file_digital = cpf + Constants.EXTENSAO_TEMPLATE
        print('Salvando usuário CPF: ', cpf)
        usuario = Usuarios()
        usuario.cpf = cpf
        usuario.numero_passagens = '10.00'
        usuario.valor_credito = '10.00'
        usuario.arq_digitais = ''#file_digital
        usuario.arq_facial = ''
        r = usuario.insert_user()
        print('Response: ', r)
        print('Usuário salvo com sucesso!')
    except:    
        print('Falha ao salvar usuário')


def select_usuario(cpf):
    print('Buscando CPF: ', cpf)
    usuario = Usuarios()
    r = usuario.select_user_by_cpf(cpf)
    print('Response: ',r)
    print('ID: ', usuario.id_usuario)
    print('CPF: ', usuario.cpf)
    print('Fingerprint: ', usuario.arq_digitais)
    print('Crédito: ', usuario.valor_credito)
    print('Passagens: ', usuario.numero_passagens)
    
    usuario.valor_credito = '10.00'
    r = usuario.update_user()
    print('Response: ',r)

    r = usuario.select_user_by_cpf(cpf)
    print('Response: ',r)
    print('ID: ', usuario.id_usuario)
    print('CPF: ', usuario.cpf)
    print('Fingerprint: ', usuario.arq_digitais)
    print('Crédito: ', usuario.valor_credito)
    print('Passagens: ', usuario.numero_passagens)



#Inicia o software    
def load_library():
    global resultado_load
    biometrics = CommandsBiometric()
    resultado_load = biometrics.init_cis()
    return resultado_load

#Encerra o software    
def fechar_programa():
    biometrics = CommandsBiometric()
    biometrics.finish_cis()
    print("Good bye.....")
    quit()


#Criação da root principal
root = Tk()
logging.basicConfig(filename='app.log', filemode='a', format='%(asctime)s - %(message)s')
running = 1
fonte = ("Verdana 30 bold")

#Título da root
root.title('Gravador Biométrico')
#frame master
root.frame_master = Frame()
root.frame_master["pady"] = 10
root.frame_master.configure(bg='black')
root.frame_master.pack(fill='both', expand=True)
update_dados = False
#Deixa a root em tela cheia
root.attributes('-fullscreen',True)
#root.resizable(False, False)

#Variaveis
dados_linha = StringVar()
hora_texto = StringVar()
linha_info_identifier = StringVar()

#frame titulo
root.frame_titulo = Frame(root.frame_master)
#root.frame_titulo.configure(bg='black')
root.frame_titulo.pack(side = 'top',fill='both', expand=True)

lbl_principal = Label(root.frame_titulo, text='GRAVADOR BIOMÉTRICO', fg='white', bg='black',font=fonte, width='500')
lbl_principal.pack(side="top")
#titulo_principal.place(x=0,y=0)

#frame center
root.frame_center = Frame(root.frame_master)
root.frame_center.pack(fill='both', expand=True)

w = Label(root.frame_center, textvariable=linha_info_identifier, font = fonte)
w.pack(fill=BOTH, expand=True)

linha_info_identifier.set(Constants.MENSAGEM_PADRAO)

#Frame options
root.frame_general_options = Frame(root.frame_master)
root.frame_general_options.configure(bg='black')
root.frame_general_options.pack(side="bottom", fill='x')
fonte_botoes = ('Arial', '17', 'bold')
tamanho_border_botoes = ('3')

###Fechar
btn_fechar = Button(root.frame_general_options)
btn_fechar['text'] = 'Fechar'
btn_fechar['font'] = fonte
btn_fechar["command"] = fechar_programa
btn_fechar["borderwidth"] = tamanho_border_botoes
btn_fechar.pack(side='bottom', fill='both', expand=True)

####Recarregar
#btn_reload = Button(root.frame_general_options)
#btn_reload['text'] = 'Recarregar Lib'
#btn_reload['font'] = fonte
#btn_reload["command"] = load_library
#btn_reload["borderwidth"] = tamanho_border_botoes
#btn_reload.pack(side='bottom', fill='both', expand=True)


#frame hora
root.frame_dados = Frame(root.frame_master)
root.frame_dados.pack(side = 'bottom', fill='both', expand=True)

#Label hora
lbl_hora = Label(root.frame_dados, textvariable=hora_texto, fg='white', bg='black', font=fonte, width='500', borderwidth=10)
lbl_hora.pack(side="bottom")


#Load DLL
resultado_load = load_library()

#Criação da Thread apontando para função que deve ser executada(atualização da hora)
update_hora = Thread(target=atualizar_hora)
update_hora.start()

#Update titulo
update_titulo = Thread(target=update_label)
update_titulo.start()

#Loop para root principal
Application(root)
root.mainloop()

#update.stop()
running = 0
