from tkinter import *
from tkinter import messagebox
import Constants

class CPFWindow(Toplevel):
    cpf_informado = ''
    
    def salvar_fingerprint(self):
        global cpf_informado
        cpf_informado = self.dados_cpf.get()
        
        if len(cpf_informado) != Constants.TAM_MIN_CPF:
            messagebox.showwarning('Aviso', 'CPF deve possuir 11 dígitos')
        else:
            self.destroy()
    
    def get_cpf(self):
        global cpf_informado
        return cpf_informado
    
    def __init__(self, master=None):

        Toplevel.__init__(self, master=master)
        fonte = ("Arial 30 bold")
        self.title('CPF')
        self.dados_cpf = StringVar()
        self.frame_cpf = Frame(self, borderwidth=10)
        self.frame_cpf.pack(fill='x')        
        
        self.lbl_cpf = Label(self.frame_cpf, text="CPF: ", font=fonte)
        self.lbl_cpf.pack(side='left')

        self.txt_cpf = Entry(self.frame_cpf, textvariable=self.dados_cpf)
        self.txt_cpf["font"] = fonte
        self.txt_cpf.delete(0, END)
        self.txt_cpf.pack(side='left', fill='x', expand=True)
        self.txt_cpf.focus()
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
        

        ###cancelar
        self.butt_cancelar = Button(self.frame_espaco)
        self.butt_cancelar['text'] = '×'
        self.butt_cancelar['font'] = fonte_botoes
        self.butt_cancelar["command"] = self.def_cancelar
        self.butt_cancelar.configure(bg='white',
                                     activebackground='white')
        self.butt_cancelar.pack(side='left', fill='both', expand=True)

        ###aceitar
        self.butt_confirmar = Button(self.frame_espaco)
        self.butt_confirmar['text'] = '✓'
        self.butt_confirmar['font'] = fonte_botoes
        self.butt_confirmar["command"] = self.salvar_fingerprint
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
    def def_cancelar(self):
        self.salvar_fingerprint()
        #self.destroy()

    #apagar
    def def_backspace(self):
        if self.focus_get()==self.txt_cpf:
            pos_fin = len(self.txt_cpf.get()) -1
            self.txt_cpf.delete(int(pos_fin))      


    def insert_text(self, value):
        if self.focus_get()==self.txt_cpf:
            self.txt_cpf.insert(END, value.upper())


    def exit_program(self):
        print("Good bye.....")
        self.quit()

       