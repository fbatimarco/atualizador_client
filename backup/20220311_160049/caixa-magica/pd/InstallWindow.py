from tkinter import *
from tkinter import messagebox
import logging
from Configuracoes import Instalacao
import Constants
from functools import partial

# global num_run 
# global btn_funcid 
# def click(btn):
#     global num_run
#     text = "%s" % btn
#     # if not text == "Del" and not text == "Close":
#     #     e.insert(END, text)
#     # if text == 'Del':
#     #     e.delete(0, END)
#     if text == 'Close':
#         boot.destroy()
#         num_run = 0
#         boot.unbind('<Button-1>', btn_funcid)


# def numpad():
#     global num_run, boot
#     boot = Tk()
#     boot['bg'] = 'green'
#     lf = LabelFrame(boot, text=" keypad ", bd=3)
#     lf.pack(padx=15, pady=10)
#     btn_list = [
#         '7',  '8',  '9',
#         '4',  '5',  '6',
#         '1',  '2',  '3',
#         '0',  'Del',  'Close']
#     r = 1
#     c = 0
#     n = 0
#     btn = list(range(len(btn_list)))
#     for label in btn_list:
#         cmd = partial(click, label)
#         btn[n] = Button(lf, text=label, width=10, height=5, command=cmd)
#         btn[n].grid(row=r, column=c)
#         n += 1
#         c += 1
#         if c == 3:
#             c = 0
#             r += 1


# def close(event):
#     global num_run, btn_funcid
#     if num_run == 1:
#         boot.destroy()
#         num_run = 0
#         root.unbind('<Button-1>', btn_funcid)


# def run(event):
#     global num_run, btn_funcid
#     if num_run == 0:
#         num_run = 1
#         numpad()
#         btn_funcid = root.bind('<Button-1>', close)

class InstallWindow(Toplevel):
    veiculo = ''
    # numero_instalacao = ''
    
    def salvar_novos_valores(self):
        global veiculo
        #global numero_instalacao
        
        veiculo = self.dados_onibus.get()
        #numero_instalacao = self.numero_instalacao.get()
        # if len(veiculo) <= 0:
        #     messagebox.showwarning('Aviso', 'Código do veículo inválido!')
        # else:
        self.destroy()
        
    def get_veiculo(self):
        global veiculo
        return veiculo

    def confirmacao(self):
        global veiculo
        veiculo = self.dados_onibus.get()

        if len(veiculo) == 0:
            messagebox.showwarning('Aviso', 'Código do veículo inválido!')
        else:
            self.destroy()

        msgbox = messagebox.askquestion('Confirmação', 'Você confirma essa instalação?')
        if msgbox == 'yes':
            return veiculo
        else:
            self.destroy()

    # def click(btn):
    #     global num_run
    #     text = "%s" % btn
    #     # if not text == "Del" and not text == "Close":
    #     #     e.insert(END, text)
    #     # if text == 'Del':
    #     #     e.delete(0, END)
    #     if text == 'Close':
    #         boot.destroy()
    #         num_run = 0
    #         root.unbind('<Button-1>', btn_funcid)

    # def get_numero_instalacao(self):
    #global numero_instalacao
    #     return numero_instalacao
        
    def __init__(self, master=None):
        Toplevel.__init__(self, master=master)
        fonte = ("Arial 30 bold")
        self.dados_onibus = StringVar()
        #self.numero_instalacao = StringVar()
        self.title('Instalação')
        self.frame_dados_onibus = Frame(self, borderwidth=10)
        self.frame_dados_onibus.pack(fill='x')
        
        self.lbl_onibus = Label(self.frame_dados_onibus, text="Instalação: ", font=fonte)
        self.lbl_onibus.pack(side='left')

        self.txt_veiculo = Entry(self.frame_dados_onibus, textvariable=self.dados_onibus)
        self.txt_veiculo["font"] = fonte
        self.txt_veiculo.focus_set()
        self.txt_veiculo.delete(0, END)
        self.txt_veiculo.pack(side='left', fill='x', expand=True)
        # global num_run
    
        # self.lf = LabelFrame(self, text=" teclado ", bd=3)
        # self.lf.pack(padx=15, pady=10)
        # btn_list = [
        #     '1',  '2',  '3',
        #     '4',  '5',  '6',
        #     '7',  '8',  '9',
        #     'X',  '0',  'OK']
        # r = 1
        # c = 0
        # n = 0
        # self.btn = list(range(len(btn_list)))
        # for label in btn_list:
        #     cmd = partial(click, label)
        #     self.btn[n] = Button(self.lf, text=label, width=10, height=5, command=cmd)
        #     self.btn[n].grid(row=r, column=c)
        #     n += 1
        #     c += 1
        #     if c == 3:
        #         c = 0
        #         r += 1


    
        # self.frame_dados_instalacao = Frame(self, borderwidth=10)
        
        # self.frame_dados_instalacao.pack(fill='x')
    
        # self.lbl_instalacao = Label(self.frame_dados_instalacao, text="Instalação: ", font=fonte)
        # self.lbl_instalacao.pack(side='left')

        # self.txt_instalacao = Entry(self.frame_dados_instalacao, textvariable=self.numero_instalacao)
        # self.txt_instalacao["font"] = fonte    
        # self.txt_instalacao.delete(0, END)
        # self.txt_instalacao.pack(side='left', fill='x', expand=True)

        fonte_botoes = ('Arial', '30', 'bold')

        #frame 123
        self.frame_1 = Frame(self)
        self.frame_1.configure(bg='white')
        self.frame_1.pack(fill='both', expand=True)

        ###111
        self.butt_1 = Button(self.frame_1)
        self.butt_1['text'] = '1'
        self.butt_1['font'] = fonte_botoes
        self.butt_1["command"] = self.key_1
        self.butt_1.configure(bg='white', activebackground='white')
        self.butt_1.pack(side='left', fill='both', expand=True)
        
        ###222
        self.butt_2 = Button(self.frame_1)
        self.butt_2['text'] = '2'
        self.butt_2['font'] = fonte_botoes
        self.butt_2["command"] = self.key_2
        self.butt_2.configure(bg='white', activebackground='white')
        self.butt_2.pack(side='left', fill='both', expand=True)
        
        ###333
        self.butt_3 = Button(self.frame_1)
        self.butt_3['text'] = '3'
        self.butt_3['font'] = fonte_botoes
        self.butt_3["command"] = self.key_3
        self.butt_3.configure(bg='white',
                                     activebackground='white')
        self.butt_3.pack(side='left', fill='both', expand=True)

        #frame 
        self.frame_4 = Frame(self)
        self.frame_4.configure(bg='white')
        self.frame_4.pack(fill='both', expand=True)

        ###444
        self.butt_4 = Button(self.frame_4)
        self.butt_4['text'] = '4'
        self.butt_4['font'] = fonte_botoes
        self.butt_4["command"] = self.key_4
        self.butt_4.configure(bg='white',
                                     activebackground='white')
        self.butt_4.pack(side='left', fill='both', expand=True)

        ###555
        self.butt_5 = Button(self.frame_4)
        self.butt_5['text'] = '5'
        self.butt_5['font'] = fonte_botoes
        self.butt_5["command"] = self.key_5
        self.butt_5.configure(bg='white',
                                     activebackground='white')
        self.butt_5.pack(side='left', fill='both', expand=True)

        ###666
        self.butt_6 = Button(self.frame_4)
        self.butt_6['text'] = '6'
        self.butt_6['font'] = fonte_botoes
        self.butt_6["command"] = self.key_6
        self.butt_6.configure(bg='white',
                                     activebackground='white')
        self.butt_6.pack(side='left', fill='both', expand=True)

        #frame 789
        self.frame_7 = Frame(self)
        self.frame_7.configure(bg='white')
        self.frame_7.pack(fill='both', expand=True)
        
        ###777
        self.butt_7 = Button(self.frame_7)
        self.butt_7['text'] = '7'
        self.butt_7['font'] = fonte_botoes
        self.butt_7["command"] = self.key_7
        self.butt_7.configure(bg='white',
                                     activebackground='white')
        self.butt_7.pack(side='left', fill='both', expand=True)

        ###888
        self.butt_8 = Button(self.frame_7)
        self.butt_8['text'] = '8'
        self.butt_8['font'] = fonte_botoes
        self.butt_8["command"] = self.key_8
        self.butt_8.configure(bg='white',
                                     activebackground='white')
        self.butt_8.pack(side='left', fill='both', expand=True)

        ###999
        self.butt_9 = Button(self.frame_7)
        self.butt_9['text'] = '9'
        self.butt_9['font'] = fonte_botoes
        self.butt_9["command"] = self.key_9
        self.butt_9.configure(bg='white',
                                     activebackground='white')
        self.butt_9.pack(side='left', fill='both', expand=True)
        
        #frame espaco
        self.frame_espaco = Frame(self)
        self.frame_espaco.configure(bg='white')
        self.frame_espaco.pack(fill='both', expand=True)
        

        ###_backspace
        self.butt_backspace = Button(self.frame_espaco)
        self.butt_backspace['text'] = '←'
        self.butt_backspace['font'] = fonte_botoes
        self.butt_backspace["command"] = self.def_backspace
        self.butt_backspace.configure(bg='white',
                                     activebackground='white')
        self.butt_backspace.pack(side='left', fill='both', expand=True)        


        ###000
        self.butt_0 = Button(self.frame_espaco)
        self.butt_0['text'] = '0'
        self.butt_0['font'] = fonte_botoes
        self.butt_0["command"] = self.key_0
        self.butt_0.configure(bg='white',
                                     activebackground='white')
        self.butt_0.pack(side='left', fill='both', expand=True)
        

        # ###cancelar
        # self.butt_cancelar = Button(self.frame_espaco)
        # self.butt_cancelar['text'] = '×'
        # self.butt_cancelar['font'] = fonte_botoes
        # self.butt_cancelar["command"] = self.def_cancelar
        # self.butt_cancelar.configure(bg='white',
        #                              activebackground='white')
        # self.butt_cancelar.pack(side='left', fill='both', expand=True)


        ###aceitar
        self.butt_confirmar = Button(self.frame_espaco)
        self.butt_confirmar['text'] = '✓'
        self.butt_confirmar['font'] = fonte_botoes
        self.butt_confirmar["command"] = self.salvar_novos_valores
        # self.butt_confirmar["command"] = self.confirmacao
        self.butt_confirmar.configure(bg='white',
                                     activebackground='white')
        self.butt_confirmar.pack(side='left', fill='both', expand=True)

        
    def key_1(self):
        self.insert_text('1')  
        
    def key_2(self):
        self.insert_text('2')
        
    def key_3(self):
        self.insert_text('3')

    def key_4(self):
        self.insert_text('4')

    def key_5(self):
        self.insert_text('5')

    def key_6(self):
        self.insert_text('6')

    def key_7(self):
        self.insert_text('7')

    def key_8(self):
        self.insert_text('8')

    def key_9(self):
        self.insert_text('9')

    def key_0(self):
        self.insert_text('0')

    #cancelar
    # def def_cancelar(self):
    #     self.destroy()

    #espaco
    def def_espaco(self):
        self.insert_text(' ')

    #apagar
    def def_backspace(self):
        if self.focus_get()==self.txt_veiculo:
            pos_fin = len(self.txt_veiculo.get()) -1
            self.txt_veiculo.delete(int(pos_fin))
        
        # if self.focus_get()==self.txt_instalacao:
        #     pos_fin = len(self.txt_instalacao.get()) -1
        #     self.txt_instalacao.delete(int(pos_fin))            


    def insert_text(self, value):
        if self.focus_get()==self.txt_veiculo:
            self.txt_veiculo.insert(END, value.upper())

        # if self.focus_get()==self.txt_instalacao:
        #     self.txt_instalacao.insert(END, value.upper())


