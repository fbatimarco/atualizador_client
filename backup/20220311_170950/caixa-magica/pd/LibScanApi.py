import logging
from ctypes import *
import Constants
import os
import ctypes
from tkinter import messagebox
import traceback

class LibScanApi():        
    def __init__(self):
        pass
    
    #Carrega a lib na memória
    def init_lib(self):
        global lib
        global path
        print('init_lib')
        logging.warning('init_lib')
        logging.warning("Path: " + path)
        # Load DLL into memory.
        handler = lib.ftrScanOpenDevice()    
        print('Código retorno: ', lib.ftrScanGetLastError())
        logging.warning("Código retorno: " + str(lib.ftrScanGetLastError()))
        return handler

    #Libera a porta
    def finish_lib(self, h):
        global lib
        global path
        print('finish_lib')
        logging.warning('finish_lib')
        logging.warning("Path: " + path)
        result = lib.ftrScanCloseDevice(h)    
        print('Código retorno: ', lib.ftrScanGetLastError())
        logging.warning("Código retorno: " + str(result))
        return result

    #Cadastro biometria
    def enroll_fingerprint(self, h):
        global lib
        global amostra
        amostra = bytes(b'\x00')*Constants.TAM_IMG_FINGERPRINT
        print('enroll_fingerprint')
        logging.warning('enroll_fingerprint')
        if lib.ftrScanGetImageSize(h,amostra) == False:
            print('Falha ao obter tamanho da imagem')
            lib.ftrScanCloseDevice(h)
        
        print('Aguardando digital.')
        #Checa detectção fingerprint
        while 1:
            if lib.ftrScanIsFingerPresent(h,None):
                print('Leitura realizada.')
                break;
            for item in range(100):
                i=0

        if lib.ftrScanGetImage2(h, 1, amostra):
            result = lib.ftrScanGetLastError()
            print('Código retorno: ', result) 
            return amostra            
        else :
            result = lib.ftrScanGetLastError()
            print('Código retorno: ', result)        
            logging.warning("Código retorno: " + str(result))
            amostra = bytes(b'\x00')*1
            return amostra
        

    #Le biometria
    def read_fingerprint(self):
        amostra = bytes(b'\x00')*Constants.TAM_IMG_FINGERPRINT
        print('read_fingerprint')
        logging.warning('read_fingerprint')
        if lin.ftrScanGetImageSize(h,amostra) == False:
            print('Falha ao obter tamanho da imagem')
            lib.ftrScanCloseDevice(h)
        
        print('Aguardando digital.')
        #Checa detectção fingerprint
        while 1:
            if lib.ftrScanIsFingerPresent(h,None):
                print('Leitura realizada.')
                break;
            for item in range(100):
                i=0

        if lib.ftrScanGetImage2(h, 1, amostra):
            result = lib.ftrScanGetLastError()
            print('Código retorno: ', result) 
            return amostra            
        else :
            result = lib.ftrScanGetLastError()
            print('Código retorno: ', result)        
            logging.warning("Código retorno: " + str(result))
            amostra = bytes(b'\x00')*1
            return amostra
    
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
    amostra = bytes(b'\x00')*Constants.TAM_IMG_FINGERPRINT
    path = os.getcwd()
    path = path + Constants.PATH_LIB_BIOMETRY_SCAN_API_LINUX
    print(path)
    lib = cdll.LoadLibrary(path)
except:
    print('>>> traceback <<<')
    traceback.print_exc()
    print('>>> end of traceback <<<')    
    messagebox.showerror("Falha", "Falha ao importar bibliotecas")
    logging.error("Falha ao importar bibliotecas.")
    print("Falha ao importar bibliotecas.")
    quit()

