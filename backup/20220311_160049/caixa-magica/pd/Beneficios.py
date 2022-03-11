from Banco import Banco
from datetime import datetime
import traceback

class Beneficios(object):

    def __init__(self, id = 0, guidAtribuicao = "", nomeBeneficio = "", tipoDesconto = "",
     valorDesconto = '0.00', limitePeriodo = "", usuario_id = 0):

        print('Construtor benefício')
        self.info = {}
        self.id = id
        self.guidAtribuicao = guidAtribuicao
        self.nomeBeneficio = nomeBeneficio
        self.tipoDesconto = tipoDesconto
        self.valorDesconto = valorDesconto
        self.limitePeriodo = limitePeriodo
        self.usuario_id = usuario_id
    
    def insert_beneficio(self):

        banco = Banco()
        try:

            c = banco.conexao.cursor()

            c.execute("insert into beneficio (guidAtribuicao, nomeBeneficio, tipoDesconto, valorDesconto, limitePeriodo, usuario_id) values ('" + self.guidAtribuicao  + "', '" + self.nomeBeneficio + "', '" + self.tipoDesconto + "','" + str(self.valorDesconto) + "', '" + self.limitePeriodo + "', '" + str(self.usuario_id) + "' )")
            
            lastId = c.lastrowid
            banco.conexao.commit()
            c.close()

            return lastId
        except:
            print('>>> traceback <<<')
            traceback.print_exc()
            print('>>> end of traceback <<<')  
            return "Ocorreu um erro na inserção do benefício"

    def update_beneficio(self):
  
        banco = Banco()
        try:
  
            c = banco.conexao.cursor()

            c.execute("""update beneficio set nomeBeneficio = ?, 
            tipoDesconto = ?, valorDesconto = ?, limitePeriodo = ? where id = ?,
             guidAtribuicao = ?;""", 
             (self.nomeBeneficio , self.tipoDesconto, str(self.valorDesconto), self.limitePeriodo,
               self.guidAtribuicao))

            banco.conexao.commit()
            c.close()
  
            print('benefício atualizado com sucesso!')
            return True
        except:
            print('>>> traceback <<<')
            traceback.print_exc()
            print('>>> end of traceback <<<')  

            print('Ocorreu um erro na alteração do benefício')
            return False
    
    def delete_beneficio(self):
  
        banco = Banco()
        try:
  
            c = banco.conexao.cursor()
  
            c.execute("delete from beneficio where id = ?", str(self.id))
  
            banco.conexao.commit()
            c.close()
  
            return "Benefício excluído com sucesso!"
        except:
            print('>>> traceback <<<')
            traceback.print_exc()
            print('>>> end of traceback <<<')  
            return "Ocorreu um erro na exclusão do benefício"


    def select_beneficio_by_id(self, id):
        banco = Banco()
        try:
  
            c = banco.conexao.cursor()
            
            c.execute("""select * from beneficio where id = ?; """, (str(id)))
              
            for linha in c:
                print(linha) 
                self.id = linha[0]
                self.guidAtribuicao = linha[1]
                self.nomeBeneficio = linha[2]
                self.tipoDesconto = linha[3]
                self.valorDesconto = linha[4]
                self.limitePeriodo = linha[5]
                self.usuario_id = linha[6]

            c.close()
  
            return "Busca feita com sucesso!"
        except:
            print('>>> traceback <<<')
            traceback.print_exc()
            print('>>> end of traceback <<<')  
            return "Ocorreu um erro na busca do benefício"

    def select_beneficio_by_usuario_id(self, usuario_id):
        banco = Banco()
        try:
            descontoMaximo = 0.0
            c = banco.conexao.cursor()
            periodo = Periodos()
            
            c.execute("""select * from beneficio where usuario_id = ?; """, (str(usuario_id)))
              
            for linha in c:   
                #print(linha)  
                self.id = linha[0]
                self.guidAtribuicao = linha[1]
                self.nomeBeneficio = linha[2]
                self.tipoDesconto = linha[3]
                self.valorDesconto = linha[4]
                self.limitePeriodo = linha[5]
                self.usuario_id = linha[6]

                isBeneficioValido = periodo.select_periodo_by_beneficio_id(self.id)

                if isBeneficioValido:
                    if descontoMaximo < float(linha[4]):
                        descontoMaximo = float(linha[4])

            c.close()
  
            return descontoMaximo
        except:
            print('>>> traceback <<<')
            traceback.print_exc()
            print('>>> end of traceback <<<')  
            return "Ocorreu um erro na busca do benefício"


class Periodos(object):

    def __init__(self, id = 0, beneficio_id = 0, diaSemana = "", consideradoFeriado = "",
     horaIni = "", horaFinal = ""):

        print('Construtor período do benefício')
        self.info = {}
        self.id = id
        self.beneficio_id = beneficio_id
        self.diaSemana = diaSemana
        self.consideradoFeriado = consideradoFeriado
        self.horaIni = horaIni
        self.horaFinal = horaFinal
        

    def insert_periodo(self):

        banco = Banco()
        try:

            c = banco.conexao.cursor()

            c.execute("insert into beneficio_periodo (beneficio_id, diaSemana, consideradoFeriado, horaIni, horaFinal) values ('" + str(self.beneficio_id)  + "', '" + self.diaSemana + "', '" + self.consideradoFeriado + "','" + self.horaIni + "', '" + self.horaFinal + "' )")

            banco.conexao.commit()
            c.close()

            return "Período do benefício cadastrado com sucesso!"
        except:
            print('>>> traceback <<<')
            traceback.print_exc()
            print('>>> end of traceback <<<')  
            return "Ocorreu um erro na inserção do período do benefício"


    def delete_periodo(self):
  
        banco = Banco()
        try:
  
            c = banco.conexao.cursor()
  
            c.execute("delete from beneficio_periodo where id = ?", str(self.id))
  
            banco.conexao.commit()
            c.close()
  
            return "Período do benefício exclusão com sucesso!"
        except:
            print('>>> traceback <<<')
            traceback.print_exc()
            print('>>> end of traceback <<<')  
            return "Ocorreu um erro na exclusão do período do benefício"
            

    def update_periodo(self):
  
        banco = Banco()
        try:
  
            c = banco.conexao.cursor()

            c.execute("""update beneficio_periodo set beneficio_id = ?, 
            diaSemana = ?, consideradoFeriado = ?, horaIni = ?, horaFinal = ? where id = ?;""", 
             (self.beneficio_id , self.diaSemana, self.consideradoFeriado, self.horaIni,
               self.horaFinal))

            banco.conexao.commit()
            c.close()
  
            print('Período atualizado com sucesso!')
            return True
        except:
            print('>>> traceback <<<')
            traceback.print_exc()
            print('>>> end of traceback <<<')  

            print('Ocorreu um erro na alteração do período')
            return False

    def select_periodo_by_id(self, id):
        banco = Banco()
        try:
  
            c = banco.conexao.cursor()
            
            c.execute("""select * from beneficio_periodo where id = ?; """, (str(id)))
              
            for linha in c:
                print(linha) 
                self.id = linha[0]
                self.beneficio_id = linha[1]
                self.diaSemana = linha[2]
                self.consideradoFeriado = linha[3]
                self.horaIni = linha[4]
                self.horaFinal = linha[5]

            c.close()
  
            return "Busca feita com sucesso!"
        except:
            print('>>> traceback <<<')
            traceback.print_exc()
            print('>>> end of traceback <<<')  
            return "Ocorreu um erro na busca do período"
        

    def select_periodo_by_beneficio_id(self, beneficio_id):
            
        banco = Banco()
        try:
            
            DIAS = ['Segunda-feira', 'Terça-feira', 'Quarta-feira', 'Quinta-Feira', 'Sexta-feira', 'Sábado', 'Domingo']
            
            beneficioValido = False
            
            c = banco.conexao.cursor()
            
            c.execute("""select * from beneficio_periodo where beneficio_id = ?; """, (str(beneficio_id)))
              
            for linha in c:
                #print(linha) 
                self.id = linha[0]
                self.beneficio_id = linha[1]
                self.diaSemana = linha[2]
                self.consideradoFeriado = linha[3]
                self.horaIni = linha[4]
                self.horaFinal = linha[5]
                
                today = datetime.now()
                datetime_in_string = "%H:%M:%S"
                dateHoraIni = datetime.strptime(self.horaIni, datetime_in_string)
                dateHoraFinal = datetime.strptime(self.horaFinal, datetime_in_string)
                
                indiceDiaSem = today.weekday()
                # O período funciona no dia da semana de hoje?
                if DIAS[indiceDiaSem] == self.diaSemana:
                    print(DIAS[indiceDiaSem])
                    # O período funciona na hora atual?
                    if today.time() >= dateHoraIni.time() and today.time() <= dateHoraFinal.time():
                        beneficioValido = True
     
            c.close()
  
            return beneficioValido
        except:
            print('>>> traceback <<<')
            traceback.print_exc()
            print('>>> end of traceback <<<')  
            return "Ocorreu um erro na busca do período"


    