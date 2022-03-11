import logging
from ctypes import *
import Constants
import os
import ctypes
from tkinter import messagebox
import traceback

class CommandsBiometric():        
    def __init__(self):
        pass
    
    #Carrega a lib na memória
    def init_cis(self):
        global lib
        global path
        print('init_cis')
        logging.warning('init_cis')
        logging.warning("Path: " + path)
        # Load DLL into memory.
        result = lib.CIS_SDK_Biometrico_Iniciar()    
        print('Código retorno: ', result)
        logging.warning("Código retorno: " + str(result))
        return result

    #Libera a porta
    def finish_cis(self):
        global lib
        global path
        print('finish_cis')
        logging.warning('finish_cis')
        logging.warning("Path: " + path)
        result = lib.CIS_SDK_Biometrico_Finalizar()    
        print('Código retorno: ', result)
        logging.warning("Código retorno: " + str(result))
        return result

    def salvar_fingerprint(self):
        global amostra

    #Cadastro biometria
    def enroll_fingerprint_cis(self):
        global lib
        global amostra
        amostra = bytes(b'\x00')*Constants.TAM_TMP_FINGERPRINT
        print('enroll_fingerprint_cis')
        logging.warning('enroll_fingerprint_cis')
        result = lib.CIS_SDK_Biometrico_LerDigital(amostra)
        print('Código retorno: ', result)        
        logging.warning("Código retorno: " + str(result))
        if result==Constants.COMANDO_EXECUTADO_COM_SUCESSO:
            return amostra
        else:
            amostra = bytes(b'\x00')*1
        return amostra


    #Le biometria
    def read_fingerprint_cis(self):
        global lib
        global amostra
        amostra = bytes(b'\x00')*Constants.TAM_TMP_FINGERPRINT
        print('read_fingerprint_cis')
        logging.warning('read_fingerprint_cis')
        result = lib.CIS_SDK_Biometrico_LerDigital(amostra)    
        print('Código retorno: ', result)        
        logging.warning("Código retorno: " + str(result))
        if result==Constants.COMANDO_EXECUTADO_COM_SUCESSO:
            print('Executado com sucesso')        
        return result
    
    #Compara biometrias
    def compare_fingerprints_cis(self, amostra_lida):
        global lib
        print('compare_fingerprints_cis')
        logging.warning('compare_fingerprints_cis')
        result = compare_template_fingerprint(amostra_lida)
        print('Código retorno: ', result)
        logging.warning("Código retorno: " + str(result))
        return result
    
    
    #Retorna versão das SDK
    def version_sdk_cis(self):
        global lib
        print('version_sdk_cis')
        logging.warning('version_sdk_cis')
        #TODO - Verificar        
        result = lib.CIS_SDK_Versao(template)    
        print('Código retorno: ', result)
#        logging.warning("Código retorno: " + str(result))
        return result    
    
    #Retorna ponteiro como string
    def return_sdk_cis(self):
        global lib
        print('return_sdk_cis')
        logging.warning('return_sdk_cis')
        #TODO - Verificar        
        result = lib.CIS_SDK_Retorno(template)    
        print('Código retorno: ', result)
        logging.warning("Código retorno: " + str(result))
        return result

    #Efetua a leitura da digital retornando ponteiro
    def read_fingerprint_return_pointer(self):
        global lib
        global amostra

        print('read_fingerprint_return_pointer')
        logging.warning('read_fingerprint_return_pointer')
        
        result = ctypes.c_long()
#        digital = ctypes.c_byte(Constants.TAM_TMP_FINGERPRINT)
#        i_ret = ctypes.pointer(result)
#        digital = lib.CIS_SDK_Biometrico_LerDigital_RetornoPonteiro(i_ret)
        print('Código retorno: ', result.value)
        logging.warning("Código retorno: " + str(result))
        return result  

    #Efetua a leitura da imagem do dedo em WSQ
    def read_fingerprint_return_wsq(self):
        global lib
        print('read_fingerprint_return_wsq')
        logging.warning('read_fingerprint_return_wsq')        
        result = lib.CIS_SDK_Biometrico_LerDigital_LerWSQ()    
        print('Código retorno: ', result)
        logging.warning("Código retorno: " + str(result))
        return result  
 
    #Efetua a leitura da imagem do dedo em WSQ
    def read_fingerprint_return_image(self):
        global lib
        print('read_fingerprint_return_image')
        logging.warning('read_fingerprint_return_image')        
        result = lib.CIS_SDK_Biometrico_LerDigitalComImagem()    
        print('Código retorno: ', result)
        logging.warning("Código retorno: " + str(result))
        return result 

    #Verifica se a digital já foi cadastrada
    def compare_template_fingerprint(self, amostra_lida):
        global lib
        path_digital = os.getcwd()
        path_digital = path_digital + Constants.PATH_FINGERPRINTS_LINUX
        
        list_files = os.listdir(path_digital)
        r = Constants.DIGITAL_NAO_ENCONTRADA
        #RECUPERA DIGITAIS CADASTRADAS        
        for file in list_files:
            file_name = file
            file = open(path_digital + Constants.DIVISOR_PATH_LINUX + file_name,"rb")
            print("COMPARANDO DIGITAL: ", file_name)
            tpl = file.read()
            file.close()
            r = lib.CIS_SDK_Biometrico_CompararDigital(amostra_lida,tpl)
            if(r != Constants.DIGITAL_ENCONTRADA):
                print("Digital não cadastrada")    
            else:
                print("Digital encontrada com sucesso")
                break
        return r
    
    #Verifica se a digital já foi cadastrada
    def check_template_fingerprint(self, amostra_lida):
        global lib
        path_digital = os.getcwd()
        path_digital = path_digital + Constants.PATH_FINGERPRINTS_LINUX
        
        list_files = os.listdir(path_digital)
        cpf = '0'
        #RECUPERA DIGITAIS CADASTRADAS        
        for file in list_files:
            file_name = file
            file = open(path_digital + Constants.DIVISOR_PATH_LINUX + file_name,"rb")
            print("COMPARANDO DIGITAL: ", file_name)
            tpl = file.read()
            file.close()
            r = lib.CIS_SDK_Biometrico_CompararDigital(amostra_lida,tpl)
            if(r != Constants.DIGITAL_ENCONTRADA):
                cpf = '0'
                print("Digital não cadastrada")    
            else:
                cpf = file_name[:-4]#Remove extensão do arquivo .tpl
                print("Digital encontrada com sucesso")
                break
        return cpf    
    
try:
    #Get Path do projeto
    amostra = bytes(b'\x00')*Constants.TAM_TMP_FINGERPRINT
    path = os.getcwd()
    #path = path + Constants.PATH_LIB_BIOMETRY_PDS_ARM
    path = path + Constants.PATH_LIB_BIOMETRY_LINUX
    #path = path + Constants.PATH_LIB_BIOMETRY_WINDOWS
    print(path)

    #lib = windll.LoadLibrary(path)#Windows
    lib = cdll.LoadLibrary(path)#Linux
except:
    print('>>> traceback <<<')
    traceback.print_exc()
    print('>>> end of traceback <<<')    
    messagebox.showerror("Falha", "Falha ao importar bibliotecas")
    logging.error("Falha ao importar bibliotecas.")
    print("Falha ao importar bibliotecas.")
    quit()
