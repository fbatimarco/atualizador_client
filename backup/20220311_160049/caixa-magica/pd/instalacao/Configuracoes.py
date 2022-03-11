from Banco import Banco
import traceback

class Instalacao(object):

    def __init__(self, id = 0, num_serie = "", instalacao = "", veiculo = "", token = "", operadora = "",
     acesso = ""):

        print('Construtor instalação')
        self.info = {}
        self.id = id
        self.num_serie = num_serie
        self.instalacao = instalacao
        self.veiculo = veiculo
        self.token = token
        self.operadora = operadora
        self.acesso = acesso
    
    def insert_instalacao(self):

        banco = Banco()
        try:

            c = banco.conexao.cursor()

            c.execute("insert into instalacao (num_serie, instalacao, veiculo, token, operadora, acesso) values ('" + self.num_serie  + "', '" + self.instalacao + "', '" + self.veiculo + "', '" + self.token + "', '" + self.operadora + "', '" + self.acesso + "' )")
            
            banco.conexao.commit()
            c.close()

            return "Dados de instalação armazenados com sucesso!"
        except:
            print('>>> traceback <<<')
            traceback.print_exc()
            print('>>> end of traceback <<<')  
            return "Ocorreu um erro na inserção dos dados de instalação"

    def update_instalacao(self):
  
        banco = Banco()
        try:
  
            c = banco.conexao.cursor()

            c.execute("""update instalacao set num_serie = ?, 
            instalacao = ?, veiculo = ?, token = ?, operadora = ?, acesso = ? where id = ?;""", 
             (self.num_serie, self.instalacao, self.veiculo, self.token, self.operadora,
               self.acesso, self.id))

            banco.conexao.commit()
            c.close()
  
            print('Dados de instalação atualizados com sucesso!')
            return True
        except:
            print('>>> traceback <<<')
            traceback.print_exc()
            print('>>> end of traceback <<<')  

            print('Ocorreu um erro na atualização dos dados de instalação')
            return False
    
    def delete_instalacao(self):
  
        banco = Banco()
        try:
  
            c = banco.conexao.cursor()
  
            c.execute("delete from instalacao where id = ?", str(self.id))
  
            banco.conexao.commit()
            c.close()
  
            return "Dados de instalação excluídos com sucesso!"
        except:
            print('>>> traceback <<<')
            traceback.print_exc()
            print('>>> end of traceback <<<')  
            return "Ocorreu um erro na exclusão dos dados de instalação"


    def select_instalacao_by_id(self, id):
        banco = Banco()
        try:
  
            c = banco.conexao.cursor()
            
            c.execute("""select * from instalacao where id = ?; """, (str(id)))
              
            for linha in c:
                print(linha) 
                self.id = linha[0]
                self.num_serie = linha[1]
                self.instalacao = linha[2]
                self.veiculo = linha[3]
                self.token = linha[4]
                self.operadora = linha[5]
                self.acesso = linha[6]

            c.close()
  
            return "Busca feita com sucesso!"
        except:
            print('>>> traceback <<<')
            traceback.print_exc()
            print('>>> end of traceback <<<')  
            return "Ocorreu um erro na busca dos dados de instalação"


    def select_instalacao_by_num_serie(self, num_serie):
        banco = Banco()
        try:
  
            c = banco.conexao.cursor()
            
            c.execute("""select * from instalacao where num_serie like ?; """, ('%'+num_serie+'%',))
              
            for linha in c:
                print(linha) 
                self.id = linha[0]
                self.num_serie = linha[1]
                self.instalacao = linha[2]
                self.veiculo = linha[3]
                self.token = linha[4]
                self.operadora = linha[5]
                self.acesso = linha[6]

            c.close()
  
            return "Busca feita com sucesso!"
        except:
            print('>>> traceback <<<')
            traceback.print_exc()
            print('>>> end of traceback <<<')  
            return "Ocorreu um erro na busca dos dados de instalação"
        

class MatrizHoraria(object):

    def __init__(self, id = 0, veiculo = "", chave_responsavel = "", feriado = "", id_linha = 0, nome_linha = "",
     dia_semana = "", horario = "", motivo = "", tipo_viagem = ""):

        print('Construtor requisição de inicialização')
        self.info = {}
        self.id = id
        self.veiculo = veiculo
        self.chave_responsavel = chave_responsavel
        self.feriado = feriado
        self.id_linha = id_linha
        self.nome_linha = nome_linha
        self.dia_semana = dia_semana
        self.horario = horario
        self.motivo = motivo
        self.tipo_viagem = tipo_viagem

    
    def insert_matriz_horaria(self):

        banco = Banco()
        try:

            c = banco.conexao.cursor()

            c.execute("insert into matriz_horaria (veiculo, chave_responsavel, feriado, id_linha, nome_linha, dia_semana, horario, motivo, tipo_viagem) values ('" + self.veiculo + "', '" + self.chave_responsavel + "', '" + self.feriado + "', '" + str(self.id_linha) + "','" + self.nome_linha + "', '" + self.dia_semana + "', '" + self.horario + "', '" + self.motivo + "', '" + self.tipo_viagem + "')")
            
            banco.conexao.commit()
            c.close()

            return "Matríz horária inserida!"
        except:
            print('>>> traceback <<<')
            traceback.print_exc()
            print('>>> end of traceback <<<')  
            return "Ocorreu um erro na inserção da matríz horária"

    def update_matriz_horaria(self):
  
        banco = Banco()
        try:
  
            c = banco.conexao.cursor()

            c.execute("""update instalacao set veiculo = ?, chave_responsavel = ?, 
            feriado = ?, id_linha = ?, nome_linha = ?, dia_semana = ?, horario = ?, motivo = ?, tipo_viagem = ? where id = ?;""", 
             (self.veiculo, self.chave_responsavel , self.feriado, str(self.id_linha), self.nome_linha,
               self.dia_semana, self.horario, self.motivo, self.tipo_viagem))

            banco.conexao.commit()
            c.close()
  
            print('Matríz horária atualizada com sucesso!')
            return True
        except:
            print('>>> traceback <<<')
            traceback.print_exc()
            print('>>> end of traceback <<<')  

            print('Ocorreu um erro na atualização da matríz horária')
            return False

    def delete_matriz_horaria(self):
  
        banco = Banco()
        try:
  
            c = banco.conexao.cursor()
  
            c.execute("delete from matriz_horaria")
  
            banco.conexao.commit()
            c.close()
  
            return "Matríz horária excluída com sucesso!"
        except:
            print('>>> traceback <<<')
            traceback.print_exc()
            print('>>> end of traceback <<<')  
            return "Ocorreu um erro na exclusão da matríz horária"



    def delete_matriz_horaria_by_id(self, id):
  
        banco = Banco()
        try:
  
            c = banco.conexao.cursor()
  
            c.execute("delete from matriz_horaria where id = ?", str(id))
  
            banco.conexao.commit()
            c.close()
  
            return "Matríz horária excluída com sucesso!"
        except:
            print('>>> traceback <<<')
            traceback.print_exc()
            print('>>> end of traceback <<<')  
            return "Ocorreu um erro na exclusão da matríz horária"


    def select_matriz_horaria_by_id(self, id):
        banco = Banco()
        try:
  
            c = banco.conexao.cursor()
            
            c.execute("""select * from matriz_horaria where id = ?; """, (str(id)))
              
            for linha in c:
                print(linha) 
                self.id = linha[0]
                self.veiculo = linha[1]
                self.chave_responsavel = linha[2]
                self.feriado = linha[3]
                self.id_linha = linha[4]
                self.nome_linha = linha[5]
                self.dia_semana = linha[6]
                self.horario = linha[7]
                self.motivo = linha[8]
                self.tipo_viagem = linha[9]

            c.close()
  
            return "Busca feita com sucesso!"
        except:
            print('>>> traceback <<<')
            traceback.print_exc()
            print('>>> end of traceback <<<')  
            return "Ocorreu um erro na busca da matríz horária"

    def select_matriz_horaria_by_veiculo(self, veiculo):
        banco = Banco()
        try:
  
            c = banco.conexao.cursor()
            
            c.execute("""select * from matriz_horaria where veiculo like ?; """, ('%'+veiculo+'%',))
              
            for linha in c:
                print(linha) 
                self.id = linha[0]
                self.veiculo = linha[1]
                self.chave_responsavel = linha[2]
                self.feriado = linha[3]
                self.id_linha = linha[4]
                self.nome_linha = linha[5]
                self.dia_semana = linha[6]
                self.horario = linha[7]
                self.motivo = linha[8]
                self.tipo_viagem = linha[9]

            c.close()
  
            return "Busca feita com sucesso!"
        except:
            print('>>> traceback <<<')
            traceback.print_exc()
            print('>>> end of traceback <<<')  
            return "Ocorreu um erro na busca da matríz horária"

