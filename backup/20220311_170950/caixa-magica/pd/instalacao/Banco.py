#importando módulo do SQlite
import sqlite3

class Banco():
  
    def __init__(self):
        self.conexao = sqlite3.connect('banco.db')
        self.create_table()
  
    def create_table(self):
        c = self.conexao.cursor()
  
        # Criação da tabela dos usuarios.
        c.execute("""create table if not exists usuario (
                     id integer primary key autoincrement,
                     cpf text,
                     numero_passagens text,
                     valor_credito text,
                     arq_digitais text,
                     arq_facial text,
                     cartao text,
                     guid text,
                     unique (guid))""")
        
        # Criação da tabela dos benefício.
        c.execute("""create table if not exists beneficio (
                    id integer primary key autoincrement,
                    guidAtribuicao text,
                    nomeBeneficio text,
                    tipoDesconto text,                   
                    valorDesconto float check (valorDesconto >= 0) NOT NULL,
                    limitePeriodo text,
                    usuario_id integer references usuario(id) on update cascade on delete cascade NOT NULL)
                    """)
        
        # Criação da tabela com os periodos dos benefícios
        c.execute("""create table if not exists beneficio_periodo(
                    id integer primary key autoincrement,
                    beneficio_id integer references beneficio(id) on update cascade on delete cascade NOT NULL,
                    diaSemana text check (diaSemana in ('Domingo', 'Segunda-feira', 'Terça-feira',
                    'Quarta-feira', 'Quinta-feira', 'Sexta-feira', 'Sábado')) NOT NULL,
                    consideradoFeriado text NOT NULL,
                    horaIni text NOT NULL,
                    horaFinal text NOT NULL,
                    unique (beneficio_id, diaSemana, horaIni, horaFinal))
                    """)

        # Criação da tabela que armazena os dados de instalação.
        c.execute("""create table if not exists instalacao(
            id integer primary key autoincrement,
            num_serie text NOT NULL,
            instalacao text NOT NULL,
            veiculo text NOT NULL,
            token text NOT NULL,
            operadora text NOT NULL,
            acesso text NOT NULL
        )""")

        # Criação da tabela que armazena os dados requisitados na inicalização.
        c.execute("""create table if not exists matriz_horaria(
            id integer primary key autoincrement,
            veiculo text NOT NULL,
            chave_responsavel text NOT NULL,
            feriado character varying(5) check(feriado in ('True','False')) NOT NULL,
            id_linha integer NOT NULL,
            nome_linha text NOT NULL,
            dia_semana text check (dia_semana in ('Domingo', 'Segunda-feira', 'Terça-feira',
                    'Quarta-feira', 'Quinta-feira', 'Sexta-feira', 'Sábado')) NOT NULL,
            horario text NOT NULL,
            motivo text NOT NULL,
            tipo_viagem character varying(7) check(tipo_viagem in ('Comum', 'Urgente'))
            )""")
            