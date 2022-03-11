from Banco import Banco
import traceback

class Usuarios(object):
  
    def __init__(self, id = 0, cpf = "", numero_passagens = '0.00', 
    valor_credito = '0.00', arq_digitais = "", arq_facial = "", 
    cartao = "", guid = ""):

        print('Construtor usuario')
        self.info = {}
        self.id = id
        self.cpf = cpf
        self.numero_passagens = numero_passagens
        self.valor_credito = valor_credito
        self.arq_digitais = arq_digitais
        self.arq_facial = arq_facial
        self.cartao = cartao
        self.guid = guid
        
  
  
    def insert_user(self):
  
        banco = Banco()
        try:
  
            c = banco.conexao.cursor()
  
            c.execute("insert into usuario (cpf, numero_passagens, valor_credito, arq_digitais, arq_facial, cartao, guid) values ('" + self.cpf + "', '" + str(self.numero_passagens) + "', '" + str(self.valor_credito) + "', '" + self.arq_digitais + "', '" + self.arq_facial + "', '" + self.cartao + "', '" + self.guid + "')")
        
            lastId = c.lastrowid
            banco.conexao.commit()

            c.close()
  
            return lastId
        except:
            print('>>> traceback <<<')
            traceback.print_exc()
            print('>>> end of traceback <<<')  
            return "Ocorreu um erro na inserção do usuário"
  
    def update_user(self):
  
        banco = Banco()
        try:

            c = banco.conexao.cursor()

            c.execute("update usuario set cpf = ?, numero_passagens = ?, valor_credito = ?, arq_digitais = ?, arq_facial = ? , cartao = ?, guid = ? where id = ?;", 
             (self.cpf , self.numero_passagens, self.valor_credito, self.arq_digitais,
              self.arq_facial, self.cartao, self.guid, str(self.id)))

            banco.conexao.commit()
            c.close()
  
            print('Usuário atualizado com sucesso!')
            return True
        except:
            print('>>> traceback <<<')
            traceback.print_exc()
            print('>>> end of traceback <<<')  

            print('Ocorreu um erro na alteração do usuário')
            return False
  
    def delete_user(self):
  
        banco = Banco()
        try:
  
            c = banco.conexao.cursor()
  
            c.execute("delete from usuario where id = ?", str(self.id))
  
            banco.conexao.commit()
            c.close()
  
            return "Usuário excluído com sucesso!"
        except:
            print('>>> traceback <<<')
            traceback.print_exc()
            print('>>> end of traceback <<<')  
            return "Ocorreu um erro na exclusão do usuário"
  
    def select_user_by_id(self, id):
        banco = Banco()
        try:
  
            c = banco.conexao.cursor()
            
            c.execute("""select * from usuario where id = ?; """, (str(id)))
              
            for linha in c:
                print(linha) 
                self.id_usuario = linha[0]
                self.cpf = linha[1]
                self.numero_passagens = linha[2]
                self.valor_credito = linha[3]
                self.arq_digitais = linha[4]
                self.arq_facial = linha[5]
                self.cartao = linha[6]
                self.guid = linha[7]

            c.close()
  
            return "Busca feita com sucesso!"
        except:
            print('>>> traceback <<<')
            traceback.print_exc()
            print('>>> end of traceback <<<')  
            return "Ocorreu um erro na busca do usuário"


    def select_user_by_cpf(self, cpf):
        banco = Banco()
        try:
            c = banco.conexao.cursor()
            
            c.execute("""select * from usuario where cpf like ?; """, ('%'+cpf+'%',))
  
            for linha in c:
                self.id = linha[0]
                self.cpf = linha[1]
                self.numero_passagens = linha[2]
                self.valor_credito = linha[3]
                self.arq_digitais = linha[4]
                self.arq_facial = linha[5]
                self.cartao = linha[6]
                self.guid = linha[7]
  
            c.close()
  
            return "Busca feita com sucesso!"
        except:
            print('>>> traceback <<<')
            traceback.print_exc()
            print('>>> end of traceback <<<')  

            return "Ocorreu um erro na busca do usuário"


    def select_user_by_cartao(self, cartao):
        banco = Banco()
        try:
            c = banco.conexao.cursor()
            
            c.execute("""select * from usuario where cartao like ?; """, ('%'+cartao+'%',))

            for linha in c:
                self.id = linha[0]
                self.cpf = linha[1]
                self.numero_passagens = linha[2]
                self.valor_credito = linha[3]
                self.arq_digitais = linha[4]
                self.arq_facial = linha[5]
                self.cartao = linha[6]
                self.guid = linha[7]

            c.close()

            return "Busca feita com sucesso!"
        except:
            print('>>> traceback <<<')
            traceback.print_exc()
            print('>>> end of traceback <<<')  

            return "Ocorreu um erro na busca do usuário"