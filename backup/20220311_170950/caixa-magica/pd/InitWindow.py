from tkinter import *
from tkinter import messagebox
from tkinter import ttk
import time
from datetime import datetime
from threading import Thread
import logging
from tkinter import messagebox
from Configuracoes import Instalacao
from Configuracoes import MatrizHoraria
from base64 import b64decode
import Constants
from HttpConnection import HttpConnection
from CommandsBiometric import CommandsBiometric
import os
import Constants

class InitWindow(Toplevel):
    load_lib = ''
    texto_info = StringVar()
    
    def set_load_lib(self, value):
        global load_lib
        load_lib = value
    
    def __init__(self, master=None):
        global texto_info
        Toplevel.__init__(self, master=master)
        self.fonte = ("Verdana 14 bold")
        #Título da root
        self.title('CAIXA MÁGICA')
        #frame master
        self.frame_master = Frame(self)
        self.frame_master["pady"] = 10
        #self.frame_master.configure(bg='black')
        self.frame_master.pack(fill='both', expand=True)
        update_dados = False
        #Deixa a root em tela cheia
        self.attributes('-fullscreen',True)
        #self.resizable(False, False)
        #frame titulo
        self.frame_titulo = Frame(self.frame_master)
        #self.frame_titulo.configure(bg='black')
        self.frame_titulo.pack(side = 'top', fill='both', expand=True)

        lbl_principal = Label(self.frame_titulo, text='CAIXA MÁGICA', font=self.fonte)
        lbl_principal.pack(side="top")

        ##frame key number
        self.frame_opcoes = Frame(self.frame_master)
        self.frame_opcoes.pack(fill='both', expand=True)

        lbl_opcoes_dados = Label(self.frame_opcoes,font='Verdana 20 bold',text='ABERTURA DE TURNO')
        lbl_opcoes_dados.pack(side='top')

        #frame Botoes
        self.frame_botoes = Frame(self.frame_master)
        self.frame_botoes.pack(fill='both', expand=True)

        fonte_info = ("Verdana 30 bold")

        fonte_botoes = ('Arial', '17', 'bold')
        tamanho_border_botoes = ('3')

        self.frame_botoes_change_key = Frame(self.frame_master)
        self.frame_botoes_change_key.pack(side='top', fill='both', expand=True)

        ##frame general options
        self.frame_general_options = Frame(self.frame_master)
        self.frame_general_options.pack(fill='both', expand=True)

        lbl_opcoes_dados = Label(self.frame_general_options,font=fonte_info,text='\n\nAGUARDANDO \nIDENTIFICAÇÃO \nDO \nRESPONSÁVEL\n\n')
        lbl_opcoes_dados.pack(side='top')

        ###Fechar
        #btn_fechar = Button(self.frame_general_options)
        #btn_fechar['text'] = 'Fechar'
        #btn_fechar['font'] = fonte_botoes
        #btn_fechar["command"] = fechar_programa
        #btn_fechar["borderwidth"] = tamanho_border_botoes
        ##btn_fechar.configure(bg='white', fg='black', activebackground='white')
        #btn_fechar.pack(side='top', fill='both', expand=True)


#        btn_confirmar = Button(self.frame_general_options)
#        btn_confirmar['text'] = 'Continuar'
#        btn_confirmar['font'] = fonte_botoes
#        #btn_confirmar["command"] = self.open_window
#        btn_confirmar["borderwidth"] = tamanho_border_botoes
#        #btn_fechar.configure(bg='white', fg='black', activebackground='white')
#        btn_confirmar.pack(side='top', fill='both', expand=True)

        hora_texto = StringVar()
        #texto_info = StringVar()

        #frame dados
        self.frame_dados = Frame(self.frame_master)
        self.frame_dados.pack(side = 'bottom', fill='both', expand=True)

        lbl_config = Label(self.frame_dados, textvariable=texto_info, font=("Verdana 10 bold"))
        lbl_config.pack(side='bottom')

        login_ok = False

    def init_matriz_horaria(self):
        global load_lib
        global texto_info
        instalacao = Instalacao()   
        #Obtém o serial do Raspberry
        num_serie = str(self.get_serial())

        instalacao.select_instalacao_by_num_serie(num_serie)
        mat_horaria = MatrizHoraria()
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
        
        #TODO CHECK BIOMETRIA
        if load_lib==Constants.COMANDO_EXECUTADO_COM_SUCESSO:
            print('Chave responsavel: ', mat_horaria.chave_responsavel)
            fingerprint = b64decode(mat_horaria.chave_responsavel)
            self.gravar_biometria_responsavel(fingerprint)
            biometrics = CommandsBiometric()
            amostra = biometrics.enroll_fingerprint_cis()
            if len(amostra) > 1 : 
                biometria_ok = biometrics.check_template_fingerprint(amostra)
                if len(biometria_ok)> 1 :
                    dados_inicializacao = 'teste'
#                    dados_inicializacao = '''Dados da matriz horária:
#                        \nLinha: ''' + str(mat_horaria.nome_linha) +
#                        '''\nDia: ''' +  mat_horaria.dia_semana +
#                        '''\nHorário: ''' +  mat_horaria.horario + 
#                        '''\nMotivo: ''' +  mat_horaria.motivo +
#                        '''\nTipo: ''' +  mat_horaria.tipo_viagem
                    
                    texto_info.set(dados_inicializacao)                    
                    try:
                        mat_horaria.insert_matriz_horaria()
                        print("Matriz horária criada!")
                        dados_inicializacao = 'Inicialização diária realizada com sucesso!'
                        time.sleep(5.0)
                        texto_info.set(dados_inicializacao)
                        self.destroy()
                    except:
                        texto_info.set('Inicialização diária mal sucedida\nTente novamente!')
                        time.sleep(3.0)
                        dados_inicializacao = '\n\nAGUARDANDO \nIDENTIFICAÇÃO \nDO \nRESPONSÁVEL\n\n'
                        texto_info.set(dados_inicializacao)
                else:
                    dados_inicializacao = 'Biometria do responsável não reconhecida!\n Tente novamente!'
                    texto_info.set(dados_inicializacao)
                    time.sleep(3.0)
                    dados_inicializacao = '\n\nAGUARDANDO \nIDENTIFICAÇÃO \nDO \nRESPONSÁVEL\n\n'
                    texto_info.set(dados_inicializacao)
                    
    #Obtem o número serial do Raspberry Pi
    def get_serial(self):
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
    
    
    def gravar_biometria_responsavel(self, fingerprint):
        try: 
            dir_dig = os.getcwd()
            dir_dig = dir_dig + Constants.PATH_FINGERPRINTS_LINUX
            if os.path.isdir(dir_dig): # vemos de este diretorio ja existe
                print ('Ja existe uma pasta com esse nome!')
            else:
                os.mkdir(dir_dig) # aqui criamos a pasta caso nao exista
                print ('Pasta criada com sucesso!')
            
            #CADASTRA A DIGITAL
            print("SALVANDO DIGITAL DO RESPONSAVEL...")
            tpl = open(dir_dig + Constants.DIVISOR_PATH_LINUX + 'responsavel' + Constants.EXTENSAO_TEMPLATE,"wb")
            tpl.write(fingerprint)
            tpl.close()
            response = Constants.COMANDO_EXECUTADO_COM_SUCESSO
        except:
            response = Constants.FALHA_GRAVAR_BIOMETRIA
    
        return response
