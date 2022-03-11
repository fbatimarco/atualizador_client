from tkinter import *
from tkinter import messagebox
import logging

class EditWindow(Toplevel):

    def salvar_novos_valores(self):
        
        try:        
            print ('Salvando novos dados!')
            arq = open('config.cfg', 'w')
            
            texto = []
            texto.append("Linha ")
            texto.append(self.dados_linha.get())
            texto.append(' - ')
            texto.append("R$ ")
            texto.append(self.valor_passagem.get())
            arq.writelines(texto)
            arq.close()
            logging.warning('Dados atualizados:')
            logging.warning(texto)
            #messagebox.showinfo("Aviso","Dados atualizados com sucesso!")
            
        except IOError:
            messagebox.showerror("Falha", "Falha ao atualizar os dados!")
            
            
        self.destroy()
    
    
    def __init__(self, master=None):
        Toplevel.__init__(self, master=master)
        fonte = ("Arial 30 bold")
        self.dados_linha = StringVar()
        self.valor_passagem = StringVar()
        self.title('Edição')
        self.frame_dados_linha = Frame(self, borderwidth=10)
        
        self.frame_dados_linha.pack(fill='x')

        #self.protocol("WM_DELETE_WINDOW", fecha_jan)
#        titulo = Label(self.frame_dados, text="Informe os dados")
#        titulo["font"] = ("Calibri", "20", "bold")
#        titulo.grid(row=0)
        
        values = self.read_dados()

        x = values.split(" - ")
        
        self.lbl_linha = Label(self.frame_dados_linha, text="Linha: ", font=fonte)
        self.lbl_linha.pack(side='left')

        self.txt_linha = Entry(self.frame_dados_linha, textvariable=self.dados_linha)
        self.txt_linha["font"] = fonte
        self.txt_linha.delete(0, END)
        v = x[0].split(" ")
        self.txt_linha.insert(0, v[1])
        self.txt_linha.pack(side='left', fill='x', expand=True)
    
        self.frame_dados_preco = Frame(self, borderwidth=10)
        
        self.frame_dados_preco.pack(fill='x')
    
        self.lbl_valor = Label(self.frame_dados_preco, text="Valor: ", font=fonte)
        self.lbl_valor.pack(side='left')

        self.txt_valor = Entry(self.frame_dados_preco, textvariable=self.valor_passagem)
        self.txt_valor["font"] = fonte    
        self.txt_valor.delete(0, END)
        v = x[1].split(" ")
        self.txt_valor.insert(0, v[1])
        self.txt_valor.pack(side='left', fill='x', expand=True)
        
        
#        botao_salvar = Button(self, text='Salvar', font = fonte, command = self.salvar_novos_valores)
#        botao_salvar.pack()

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
        
#        #frame qwe
#        self.frame_q = Frame(self)
#        self.frame_q.configure(bg='white')
#        self.frame_q.pack(fill='both', expand=True)
#
#        ###QQQ
#        self.butt_q = Button(self.frame_q)
#        self.butt_q['text'] = 'q'
#        self.butt_q['font'] = fonte_botoes
#        self.butt_q["command"] = self.key_q
#        self.butt_q.configure(bg='white',
#                                     activebackground='white')
#        self.butt_q.pack(side='left', fill='both', expand=True)
#
#        ###WWW
#        self.butt_w = Button(self.frame_q)
#        self.butt_w['text'] = 'w'
#        self.butt_w['font'] = fonte_botoes
#        self.butt_w["command"] = self.key_w
#        self.butt_w.configure(bg='white',
#                                     activebackground='white')
#        self.butt_w.pack(side='left', fill='both', expand=True)
#
#        ###EEE
#        self.butt_e = Button(self.frame_q)
#        self.butt_e['text'] = 'e'
#        self.butt_e['font'] = fonte_botoes
#        self.butt_e["command"] = self.key_e
#        self.butt_e.configure(bg='white',
#                                     activebackground='white')
#        self.butt_e.pack(side='left', fill='both', expand=True)
#
#        ###RRR
#        self.butt_r = Button(self.frame_q)
#        self.butt_r['text'] = 'r'
#        self.butt_r['font'] = fonte_botoes
#        self.butt_r["command"] = self.key_r
#        self.butt_r.configure(bg='white',
#                                     activebackground='white')
#        self.butt_r.pack(side='left', fill='both', expand=True)
#
#        ###TTT
#        self.butt_t = Button(self.frame_q)
#        self.butt_t['text'] = 't'
#        self.butt_t['font'] = fonte_botoes
#        self.butt_t["command"] = self.key_t
#        self.butt_t.configure(bg='white',
#                                     activebackground='white')
#        self.butt_t.pack(side='left', fill='both', expand=True)
#
#        ###YYY
#        self.butt_y = Button(self.frame_q)
#        self.butt_y['text'] = 'y'
#        self.butt_y['font'] = fonte_botoes
#        self.butt_y["command"] = self.key_y
#        self.butt_y.configure(bg='white',
#                                     activebackground='white')
#        self.butt_y.pack(side='left', fill='both', expand=True)
#
#        ###UUU
#        self.butt_u = Button(self.frame_q)
#        self.butt_u['text'] = 'u'
#        self.butt_u['font'] = fonte_botoes
#        self.butt_u["command"] = self.key_u
#        self.butt_u.configure(bg='white',
#                                     activebackground='white')
#        self.butt_u.pack(side='left', fill='both', expand=True)
#
#        ###III
#        self.butt_i = Button(self.frame_q)
#        self.butt_i['text'] = 'i'
#        self.butt_i['font'] = fonte_botoes
#        self.butt_i["command"] = self.key_i
#        self.butt_i.configure(bg='white',
#                                     activebackground='white')
#        self.butt_i.pack(side='left', fill='both', expand=True)
#
#        ###OOO
#        self.butt_o = Button(self.frame_q)
#        self.butt_o['text'] = 'o'
#        self.butt_o['font'] = fonte_botoes
#        self.butt_o["command"] = self.key_o
#        self.butt_o.configure(bg='white',
#                                     activebackground='white')
#        self.butt_o.pack(side='left', fill='both', expand=True)
#
#        ###PPP
#        self.butt_p = Button(self.frame_q)
#        self.butt_p['text'] = 'p'
#        self.butt_p['font'] = fonte_botoes
#        self.butt_p["command"] = self.key_p
#        self.butt_p.configure(bg='white',
#                                     activebackground='white')
#        self.butt_p.pack(side='left', fill='both', expand=True)
#
#        #frame asd
#        self.frame_a = Frame(self)
#        self.frame_a.configure(bg='white')
#        self.frame_a.pack(fill='both', expand=True)
#
#        ###AAA
#        self.butt_a = Button(self.frame_a)
#        self.butt_a['text'] = 'a'
#        self.butt_a['font'] = fonte_botoes
#        self.butt_a["command"] = self.key_a
#        self.butt_a.configure(bg='white',
#                                     activebackground='white')
#        self.butt_a.pack(side='left', fill='both', expand=True)
#
#        ###SSS
#        self.butt_s = Button(self.frame_a)
#        self.butt_s['text'] = 's'
#        self.butt_s['font'] = fonte_botoes
#        self.butt_s["command"] = self.key_s
#        self.butt_s.configure(bg='white',
#                                     activebackground='white')
#        self.butt_s.pack(side='left', fill='both', expand=True)
#
#        ###DDD
#        self.butt_d = Button(self.frame_a)
#        self.butt_d['text'] = 'd'
#        self.butt_d['font'] = fonte_botoes
#        self.butt_d["command"] = self.key_d
#        self.butt_d.configure(bg='white',
#                                     activebackground='white')
#        self.butt_d.pack(side='left', fill='both', expand=True)
#
#        ###FFF
#        self.butt_f = Button(self.frame_a)
#        self.butt_f['text'] = 'f'
#        self.butt_f['font'] = fonte_botoes
#        self.butt_f["command"] = self.key_f
#        self.butt_f.configure(bg='white',
#                                     activebackground='white')
#        self.butt_f.pack(side='left', fill='both', expand=True)
#
#        ###GGG
#        self.butt_g = Button(self.frame_a)
#        self.butt_g['text'] = 'g'
#        self.butt_g['font'] = fonte_botoes
#        self.butt_g["command"] = self.key_g
#        self.butt_g.configure(bg='white',
#                                     activebackground='white')
#        self.butt_g.pack(side='left', fill='both', expand=True)
#
#        ###HHH
#        self.butt_h = Button(self.frame_a)
#        self.butt_h['text'] = 'h'
#        self.butt_h['font'] = fonte_botoes
#        self.butt_h["command"] = self.key_h
#        self.butt_h.configure(bg='white',
#                                     activebackground='white')
#        self.butt_h.pack(side='left', fill='both', expand=True)
#
#        ###JJJ
#        self.butt_j = Button(self.frame_a)
#        self.butt_j['text'] = 'j'
#        self.butt_j['font'] = fonte_botoes
#        self.butt_j["command"] = self.key_j
#        self.butt_j.configure(bg='white',
#                                     activebackground='white')
#        self.butt_j.pack(side='left', fill='both', expand=True)
#
#        ###KKK
#        self.butt_k = Button(self.frame_a)
#        self.butt_k['text'] = 'k'
#        self.butt_k['font'] = fonte_botoes
#        self.butt_k["command"] = self.key_k
#        self.butt_k.configure(bg='white',
#                                     activebackground='white')
#        self.butt_k.pack(side='left', fill='both', expand=True)
#
#        ###LLL
#        self.butt_l = Button(self.frame_a)
#        self.butt_l['text'] = 'l'
#        self.butt_l['font'] = fonte_botoes
#        self.butt_l["command"] = self.key_l
#        self.butt_l.configure(bg='white',
#                                     activebackground='white')
#        self.butt_l.pack(side='left', fill='both', expand=True)
#
#        ###ÇÇÇ
#        self.butt_ç = Button(self.frame_a)
#        self.butt_ç['text'] = 'ç'
#        self.butt_ç['font'] = fonte_botoes
#        self.butt_ç["command"] = self.key_cedilha
#        self.butt_ç.configure(bg='white',
#                                     activebackground='white')
#        self.butt_ç.pack(side='left', fill='both', expand=True)
#
#        #frame zxc
#        self.frame_z = Frame(self)
#        self.frame_z.configure(bg='white')
#        self.frame_z.pack(fill='both', expand=True)
#
#        ###ZZZ
#        self.butt_z = Button(self.frame_z)
#        self.butt_z['text'] = 'z'
#        self.butt_z['font'] = fonte_botoes
#        self.butt_z["command"] = self.key_z
#        self.butt_z.configure(bg='white',
#                                     activebackground='white')
#        self.butt_z.pack(side='left', fill='both', expand=True)
#
#        ###XXX
#        self.butt_x = Button(self.frame_z)
#        self.butt_x['text'] = 'x'
#        self.butt_x['font'] = fonte_botoes
#        self.butt_x["command"] = self.key_x
#        self.butt_x.configure(bg='white',
#                                     activebackground='white')
#        self.butt_x.pack(side='left', fill='both', expand=True)
#
#        ###CCC
#        self.butt_c = Button(self.frame_z)
#        self.butt_c['text'] = 'c'
#        self.butt_c['font'] = fonte_botoes
#        self.butt_c["command"] = self.key_c
#        self.butt_c.configure(bg='white',
#                                     activebackground='white')
#        self.butt_c.pack(side='left', fill='both', expand=True)
#
#        ###VVV
#        self.butt_v = Button(self.frame_z)
#        self.butt_v['text'] = 'v'
#        self.butt_v['font'] = fonte_botoes
#        self.butt_v["command"] = self.key_v
#        self.butt_v.configure(bg='white',
#                                     activebackground='white')
#        self.butt_v.pack(side='left', fill='both', expand=True)
#
#        ###BBB
#        self.butt_b = Button(self.frame_z)
#        self.butt_b['text'] = 'b'
#        self.butt_b['font'] = fonte_botoes
#        self.butt_b["command"] = self.key_b
#        self.butt_b.configure(bg='white',
#                                     activebackground='white')
#        self.butt_b.pack(side='left', fill='both', expand=True)
#
#        ###NNN
#        self.butt_n = Button(self.frame_z)
#        self.butt_n['text'] = 'n'
#        self.butt_n['font'] = fonte_botoes
#        self.butt_n["command"] = self.key_n
#        self.butt_n.configure(bg='white',
#                                     activebackground='white')
#        self.butt_n.pack(side='left', fill='both', expand=True)
#
#        ###MMM
#        self.butt_m = Button(self.frame_z)
#        self.butt_m['text'] = 'm'
#        self.butt_m['font'] = fonte_botoes
#        self.butt_m["command"] = self.key_m
#        self.butt_m.configure(bg='white',
#                                     activebackground='white')
#        self.butt_m.pack(side='left', fill='both', expand=True)
#

#
#        ###...
#        self.butt_ponto = Button(self.frame_z)
#        self.butt_ponto['text'] = '.'
#        self.butt_ponto['font'] = fonte_botoes
#        self.butt_ponto["command"] = self.key_ponto
#        self.butt_ponto.configure(bg='white',
#                                     activebackground='white')
#        self.butt_ponto.pack(side='left', fill='both', expand=True)
#
#        ###:::
#        self.butt_dois_ponto = Button(self.frame_z)
#        self.butt_dois_ponto['text'] = ':'
#        self.butt_dois_ponto['font'] = fonte_botoes
#        self.butt_dois_ponto["command"] = self.key_dois_ponto
#        self.butt_dois_ponto.configure(bg='white',
#                                     activebackground='white')
#        self.butt_dois_ponto.pack(side='left', fill='both', expand=True)
#
        #frame espaco
        self.frame_espaco = Frame(self)
        self.frame_espaco.configure(bg='white')
        self.frame_espaco.pack(fill='both', expand=True)
        
        #        ###,,,
        self.butt_virgula = Button(self.frame_espaco)
        self.butt_virgula['text'] = ','
        self.butt_virgula['font'] = fonte_botoes
        self.butt_virgula["command"] = self.key_virgula
        self.butt_virgula.configure(bg='white',
                                     activebackground='white')
        self.butt_virgula.pack(side='left', fill='both', expand=True)

#        ###$
#        self.butt_cifrao = Button(self.frame_espaco)
#        self.butt_cifrao['text'] = '$'
#        self.butt_cifrao['font'] = fonte_botoes
#        self.butt_cifrao["command"] = self.key_cifrao
#        self.butt_cifrao.configure(bg='white',
#                                     activebackground='white')
#        self.butt_cifrao.pack(side='left', fill='both', expand=True)


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

        ###espaco
#        self.butt_espaco = Button(self.frame_espaco)
#        self.butt_espaco['text'] = 'Espaco'
#        self.butt_espaco['font'] = fonte_botoes
#        self.butt_espaco["command"] = self.def_espaco
#        self.butt_espaco.configure(bg='white',
#                                     activebackground='white')
#        self.butt_espaco.pack(side='left', fill='both', expand=True)

        ###aceitar
        self.butt_confirmar = Button(self.frame_espaco)
        self.butt_confirmar['text'] = '✓'
        self.butt_confirmar['font'] = fonte_botoes
        self.butt_confirmar["command"] = self.salvar_novos_valores
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

#    #qwertyuiop
#    def key_q(self):
#        self.insert_text('q')
#
#    def key_w(self):
#        self.insert_text('w')
#
#    def key_e(self):
#        self.insert_text('e')
#
#    def key_r(self):
#        self.insert_text('r')
#
#    def key_t(self):
#        self.insert_text('t')
#
#    def key_y(self):
#        self.insert_text('y')
#
#    def key_u(self):
#        self.insert_text('u')
#
#    def key_i(self):
#        self.insert_text('i')
#
#    def key_o(self):
#        self.insert_text('o')
#
#    def key_p(self):
#        self.insert_text('p')
#
#    #asdfghjklç
#    def key_a(self):
#        self.insert_text('a')
#
#    def key_s(self):
#        self.insert_text('s')
#
#    def key_d(self):
#        self.insert_text('d')
#
#    def key_f(self):
#        self.insert_text('f')
#
#    def key_g(self):
#        self.insert_text('g')
#
#    def key_h(self):
#        self.insert_text('h')
#
#    def key_j(self):
#        self.insert_text('j')
#
#    def key_k(self):
#        self.insert_text('k')
#
#    def key_l(self):
#        self.insert_text('l')
#
#    def key_cedilha(self):
#        self.insert_text('ç')
#
#    #zxcvbnm
#    def key_z(self):
#        self.insert_text('z')
#
#    def key_x(self):
#        self.insert_text('x')
#
#    def key_c(self):
#        self.insert_text('c')
#
#    def key_v(self):
#        self.insert_text('v')
#
#    def key_b(self):
#        self.insert_text('b')
#
#    def key_n(self):
#        self.insert_text('n')
#
#    def key_m(self):
#        self.insert_text('m')
#        self.posicao()
#
    def key_virgula(self):
        self.insert_text(',')
#
#    def key_ponto(self):
#        self.insert_text('.')
#
#    def key_dois_ponto(self):
#        self.insert_text(':')
#
#    def key_cifrao(self):
#        self.insert_text('$')
    #cancelar
    def def_cancelar(self):
        self.destroy()

    #espaco
    def def_espaco(self):
        self.insert_text(' ')

    #apagar
    def def_backspace(self):
        if self.focus_get()==self.txt_linha:
            pos_fin = len(self.txt_linha.get()) -1
            self.txt_linha.delete(int(pos_fin))
        
        if self.focus_get()==self.txt_valor:
            pos_fin = len(self.txt_valor.get()) -1
            self.txt_valor.delete(int(pos_fin))            


    def insert_text(self, value):
        if self.focus_get()==self.txt_linha:
            self.txt_linha.insert(END, value.upper())

        if self.focus_get()==self.txt_valor:
            self.txt_valor.insert(END, value.upper())
#            valor = int(self.txt_valor.get().replace(",","").replace(".","")) 
#            locale.setlocale(locale.LC_ALL, 'pt_BR.UTF-8')
#            valor = locale.currency(valor, grouping=True, symbol=None)
#            self.txt_valor.delete(0, END)
#            self.txt_valor.insert(0,str(valor))

            
            
    def read_dados(self):
        logging.warning('Lendo configurações atuais!')
        try:
            arq = open('config.cfg', 'r')
            print ('Arquivo encontrado!')
            texto=arq.read()
            logging.warning('Configurações atuais: ')
            logging.warning(texto)
            return texto
        except IOError:
            print ('Arquivo não encontrado! Criando um arquivo padrão.')
            arq = open('config.cfg', 'w')
            texto = []
            texto.append('Linha 0000')
            texto.append(' - ')
            texto.append('5,00')
            arq.writelines(texto)
            arq.close()
            arq = open('config.cfg', 'r')
            t=arq.read()
            return t          
