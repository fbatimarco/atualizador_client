import sys
from core import db
import time

quit()

conn1=db.Conexao()

# Cria tabela de historico, caso nao exista
statement= """CREATE table if not exists public.historico_internet 
        (
	id serial NOT NULL,
	datahorautc timestamp NULL,
	status varchar(10) NULL
);"""
conn1.manipular(statement)

conn1.manipular("alter table cobrancas add column if not exists datahorafalhaintegr timestamptz")
conn1.manipular("alter table cobrancas add column if not exists status_internet varchar(10)")
conn1.manipular("alter table cobrancas add column if not exists datahoraenviada timestamp")
conn1.manipular("alter table temperatura add column if not exists dateinsert timestamp default (now() at time zone 'utc')")
conn1.manipular("alter table saldo add column if not exists dateinsert timestamp default (now() at time zone 'utc')")
conn1.manipular("alter table facial add column if not exists dateinsert timestamp default (now() at time zone 'utc')")
conn1.manipular("alter table beneficios add column if not exists dateinsert timestamp default (now() at time zone 'utc')")
conn1.manipular("alter table cartao add column if not exists dateinsert timestamp default (now() at time zone 'utc')")
conn1.manipular("alter table contas add column if not exists dateinsert timestamp default (now() at time zone 'utc')")
conn1.manipular("alter table operadores add column if not exists dateinsert timestamp default (now() at time zone 'utc')")

conn1.manipular("alter table temperatura add column if not exists dateupdate timestamp")
conn1.manipular("alter table saldo add column if not exists dateupdate timestamp")
conn1.manipular("alter table facial add column if not exists dateupdate timestamp")
conn1.manipular("alter table beneficios add column if not exists dateupdate timestamp")
conn1.manipular("alter table cartao add column if not exists dateupdate timestamp")
conn1.manipular("alter table contas add column if not exists dateupdate timestamp")
conn1.manipular("alter table operadores add column if not exists dateupdate timestamp")

# Cria tabela para controle de ID da caixa magica (util para acoes de journal)
conn1.manipular("create table if not exists caixa_magica (caixamagica_serial varchar(40))")

# Cria procedure para obtencao do serial no BD
statement = """create or replace function public.getserial()
                returns varchar
                language plpgsql
             as $function$
             declare v_caixamagica_serial varchar := '';
             begin
               select caixamagica_serial into v_caixamagica_serial from caixa_magica limit 1;

               return v_caixamagica_serial;
             end;
             $function$
            """
conn1.manipular(statement)

# Cria tabela journal para contas
statement = """CREATE table if not exists public.journal_contas (
	journal_id bigserial not null,
	journal_caixamagica_serial varchar(40) not null,
	journal_actiondate timestamp not null,
	journal_actiontype varchar(10) not null,
	new_id int8,
	new_id_web int8,
	new_cpf varchar,
	new_nome varchar,
        new_dateinsert timestamp,
        new_dateupdate timestamp,
        old_id int8,
        old_id_web int8,
        old_cpf varchar,
        old_nome varchar,
        old_dateinsert timestamp,
        old_dateupdate timestamp,
	CONSTRAINT journal_contas_pkey PRIMARY KEY (journal_id, journal_caixamagica_serial)
);"""
conn1.manipular(statement)

# Cria tabela journal para operadores
statement = """CREATE table if not exists public.journal_operadores (
	journal_id bigserial not null,
	journal_caixamagica_serial varchar(40) not null,
	journal_actiondate timestamp not null,
	journal_actiontype varchar(10) not null,
	new_id int8,
	new_id_web int8,
	new_nome varchar,
	new_data varchar,
	new_id_qr varchar,
	new_matricula varchar(30),
        new_dateinsert timestamp,
        new_dateupdate timestamp,
        old_id int8,
        old_id_web int8,
        old_nome varchar,
        old_data varchar,
        old_id_qr varchar,
        old_matricula varchar(30),
        old_dateinsert timestamp,
        old_dateupdate timestamp

);"""
conn1.manipular(statement)

# Cria tabela journal para facial
statement = """CREATE table if not exists public.journal_facial (
	journal_id bigserial not null,
	journal_caixamagica_serial varchar(40) not null,
	journal_actiondate timestamp not null,
	journal_actiontype varchar(10) not null,
	new_id int8,
	new_nome varchar(80),
	new_data cube,
	new_conta int8,
	new_dateinsert timestamp,
	new_dateupdate timestamp,
        old_id int8,
        old_nome varchar(80),
        old_data cube,
        old_conta int8,
        old_dateinsert timestamp,
        old_dateupdate timestamp        
);"""
conn1.manipular(statement)

# Cria tabela journal para saldo
statement = """CREATE TABLE if not exists public.journal_saldo (
	journal_id bigserial not null,
	journal_caixamagica_serial varchar(40) not null,
	journal_actiondate timestamp not null,
	journal_actiontype varchar(10) not null,
	new_id int8,
	new_id_web int8,
	new_porvalor bool,
	new_conta int8,
	new_bloqueado bool,
	new_dateinsert timestamp,
	new_dateupdate timestamp,
        old_id int8,
        old_id_web int8,
        old_porvalor bool,
        old_conta int8,
        old_bloqueado bool,
        old_dateinsert timestamp,
        old_dateupdate timestamp
);"""
conn1.manipular(statement)

# Cria tabela journal para cobrancas
statement = """CREATE table if not exists public.journal_cobrancas (
	journal_id bigserial not null,
	journal_caixamagica_serial varchar(40) not null,
	journal_actiondate timestamp not null,
	journal_actiontype varchar(10) not null,
	new_id int8,
	new_valor float4,
	new_datahora varchar,
	new_tipopagamento varchar,
	new_tipoidentificacao int4,
	new_fotousuario varchar,
	new_enviada bool,
	new_saldo int8,
	new_beneficio int8,
	new_viagemid int8,
	new_geolocalizacao varchar,
	new_datahorafalhaintegr timestamptz,
	new_status_internet varchar(10),
	new_dateinsert timestamp,
	new_dateupdate timestamp,
        old_id int8,
        old_valor float4,
        old_datahora varchar,
        old_tipopagamento varchar,
        old_tipoidentificacao int4,
        old_fotousuario varchar,
        old_enviada bool,
        old_saldo int8,
        old_beneficio int8,
        old_viagemid int8,
        old_geolocalizacao varchar,
        old_datahorafalhaintegr timestamptz,
        old_status_internet varchar(10),
        old_dateinsert timestamp,
        old_dateupdate timestamp
);"""
conn1.manipular(statement)

# Cria procedure que da inicio no processo de journal nas tabelas principais da caixa magica
statement = """create or replace procedure public.sp_startJournal()
  LANGUAGE plpgsql
as $procedure$
  declare v_cnt_regs integer;
  declare v_now timestamp := (now() at time zone 'utc');
  begin 
	  v_cnt_regs := 0;
	 
     -- conta o numero de registros na tabela journal de contas
	 select count(*) into v_cnt_regs from journal_contas;
	
	 -- se nao tem registros, iniciamos a tabela com a primeira posicao de cada registro
	 -- da tabela de contas
	if v_cnt_regs <= 0 then
		insert into journal_contas (journal_caixamagica_serial, journal_actiondate, journal_actiontype,
									new_id, new_id_web, new_cpf, new_nome, new_dateinsert, new_dateupdate)
		  select getSerial(), v_now, 'INSERT', ID, id_web, cpf, nome, dateinsert, dateupdate from contas;
	end if;

     -- conta o numero de registros na tabela journal de operadores
	 select count(*) into v_cnt_regs from journal_operadores;
	
	 -- se nao tem registros, iniciamos a tabela com a primeira posicao de cada registro
	 -- da tabela de operadores
	if v_cnt_regs <= 0 then
		insert into journal_operadores (journal_caixamagica_serial, journal_actiondate, journal_actiontype,
						new_id, new_id_web, new_nome, new_data, new_id_qr, new_matricula, new_dateinsert, new_dateupdate)
		  select getSerial(), v_now, 'INSERT', ID, id_web, nome, "data", id_qr, matricula, dateinsert, dateupdate 
		  from operadores;
	end if;

     -- conta o numero de registros na tabela journal de facial
	 select count(*) into v_cnt_regs from journal_facial;
	
	 -- se nao tem registros, iniciamos a tabela com a primeira posicao de cada registro
	 -- da tabela de facial
	if v_cnt_regs <= 0 then
		insert into journal_facial (journal_caixamagica_serial, journal_actiondate, journal_actiontype,
					new_id, new_nome, new_data, new_conta, new_dateinsert, new_dateupdate)
		  select getSerial(), v_now, 'INSERT', ID, nome, "data", conta, dateinsert, dateupdate 
		  from facial;
	end if;

     -- conta o numero de registros na tabela journal de saldo
	 select count(*) into v_cnt_regs from journal_saldo;
	
	 -- se nao tem registros, iniciamos a tabela com a primeira posicao de cada registro
	 -- da tabela de saldo
	if v_cnt_regs <= 0 then
		insert into journal_saldo (journal_caixamagica_serial, journal_actiondate, journal_actiontype,
						new_id, new_id_web, new_porvalor, new_conta,new_bloqueado, new_dateinsert, new_dateupdate)
		  select getSerial(), v_now, 'INSERT', ID, id_web, porvalor, conta, bloqueado, dateinsert, dateupdate 
		  from saldo;
	end if;

     -- conta o numero de registros na tabela journal de cobrancas
	 select count(*) into v_cnt_regs from journal_cobrancas;
	
	 -- se nao tem registros, iniciamos a tabela com a primeira posicao de cada registro
	 -- da tabela de cobrancas
	if v_cnt_regs <= 0 then
		insert into journal_cobrancas (journal_caixamagica_serial, journal_actiondate, journal_actiontype,
						new_id, new_valor, new_datahora, new_tipopagamento, new_tipoidentificacao, new_fotousuario, new_enviada, new_saldo, 
						new_beneficio, new_viagemid, new_geolocalizacao, new_datahorafalhaintegr, new_status_internet, 
						new_dateinsert, new_dateupdate)
		  select getSerial(), v_now, 'INSERT', 
				 id, valor, datahora, tipopagamento, tipoidentificacao, fotousuario, enviada, saldo, 
				 beneficio, viagemid, geolocalizacao, datahorafalhaintegr, status_internet, null, null
		  from cobrancas;
	end if;
  end;
$procedure$"""
conn1.manipular(statement)

# Cria funcao de trigger que jornaliza a tabela de contas
statement = """CREATE OR REPLACE FUNCTION setJournalContas()
RETURNS trigger 
language plpgsql
AS $BODY$
declare v_now timestamp := (now() at time zone 'utc');
BEGIN
  IF (TG_OP = 'INSERT') THEN
      insert into journal_contas (journal_caixamagica_serial, journal_actiondate, journal_actiontype,
                                  new_id, new_id_web, new_cpf, new_nome, new_dateinsert, new_dateupdate)
                       values (getSerial(), v_now, TG_OP, 
                       		   new.ID, new.id_web, new.cpf, new.nome, new.dateinsert, new.dateupdate);     
      RETURN NEW;
  elsif (TG_OP = 'UPDATE') then
      insert into journal_contas (journal_caixamagica_serial, journal_actiondate, journal_actiontype,
                                  new_id, new_id_web, new_cpf, new_nome, new_dateinsert, new_dateupdate,
                                  old_id, old_id_web, old_cpf, old_nome, old_dateinsert, old_dateupdate)
                       values (getSerial(), v_now, TG_OP, 
                       		   new.ID, new.id_web, new.cpf, new.nome, new.dateinsert, new.dateupdate,
                       		   old.ID, old.id_web, old.cpf, old.nome, old.dateinsert, old.dateupdate);    
  ELSE
      insert into journal_contas (journal_caixamagica_serial, journal_actiondate, journal_actiontype,
                                  old_id, old_id_web, old_cpf, old_nome, old_dateinsert, old_dateupdate)
                       values (getSerial(), v_now, TG_OP, 
                       		   OLD.ID, OLD.id_web, OLD.cpf, OLD.nome, OLD.dateinsert, OLD.dateupdate);
      RETURN OLD;
  END IF;
  RETURN NULL;
END;
$BODY$"""
conn1.manipular(statement)

# Cria a TRIGGER de journal da tabela de contas
conn1.manipular("drop trigger if exists trigger_journal_contas on contas;")
statement="""create trigger  trigger_journal_contas
AFTER INSERT OR UPDATE OR DELETE ON contas
FOR EACH ROW
EXECUTE PROCEDURE setJournalContas();"""
conn1.manipular(statement)


# Cria funcao de trigger que jornaliza a tabela de saldo
statement="""CREATE OR REPLACE FUNCTION setJournalSaldo()
RETURNS trigger 
language plpgsql
AS $BODY$
declare v_now timestamp := (now() at time zone 'utc');
BEGIN
  IF (TG_OP = 'INSERT') THEN
      insert into journal_saldo (journal_caixamagica_serial, journal_actiondate, journal_actiontype,
                                  new_id, new_id_web, new_porvalor, new_conta, new_bloqueado, new_dateinsert, new_dateupdate)
                       values (getSerial(), v_now, TG_OP, 
                       		   new.ID, new.id_web, new.porvalor, new.conta, new.bloqueado, new.dateinsert, new.dateupdate);     
      RETURN NEW;
  elsif (TG_OP = 'UPDATE') then
      insert into journal_saldo (journal_caixamagica_serial, journal_actiondate, journal_actiontype,
                                  new_id, new_id_web, new_porvalor, new_conta, new_bloqueado, new_dateinsert, new_dateupdate,
                                  old_id, old_id_web, old_porvalor, old_conta, old_bloqueado, old_dateinsert, old_dateupdate)
                       values (getSerial(), v_now, TG_OP, 
                       		   new.id, new.id_web, new.porvalor, new.conta, new.bloqueado, new.dateinsert, new.dateupdate,
                       		   old.id, old.id_web, old.porvalor, old.conta, old.bloqueado, old.dateinsert, old.dateupdate);    
  ELSE
      insert into journal_saldo (journal_caixamagica_serial, journal_actiondate, journal_actiontype,
                                 old_id, old_id_web, old_porvalor, old_conta, old_bloqueado, old_dateinsert, old_dateupdate)
                       values (getSerial(), v_now, TG_OP, 
                       		   old.id, old.id_web, old.porvalor, old.conta, old.bloqueado, old.dateinsert, old.dateupdate);
      RETURN OLD;
  END IF;
  RETURN NULL;
END;
$BODY$"""
conn1.manipular(statement)

# Cria TRIGGER para jornalizacao da tabela de saldo
conn1.manipular("drop trigger if exists trigger_journal_saldo on saldo;")
statement="""create trigger  trigger_journal_saldo
AFTER INSERT OR UPDATE OR DELETE ON saldo
FOR EACH ROW
EXECUTE PROCEDURE setJournalSaldo();"""
conn1.manipular(statement)

# Cria procedure de jornalizacao facial
statement = """CREATE OR REPLACE FUNCTION setJournalFacial()
RETURNS trigger 
language plpgsql
AS $BODY$
declare v_now timestamp := (now() at time zone 'utc');
BEGIN
  IF (TG_OP = 'INSERT') THEN
      insert into journal_facial (journal_caixamagica_serial, journal_actiondate, journal_actiontype,
                                  new_id, new_nome, new_data, new_conta, new_dateinsert, new_dateupdate)
                       values (getSerial(), v_now, TG_OP, 
                       		   new.ID, new.nome, new."data", new.conta, new.dateinsert, new.dateupdate);     
      RETURN NEW;
  elsif (TG_OP = 'UPDATE') then
      insert into journal_facial (journal_caixamagica_serial, journal_actiondate, journal_actiontype,
                                 new_id, new_nome, new_data, new_conta, new_dateinsert, new_dateupdate,
                                 old_id, old_nome, old_data, old_conta, old_dateinsert, old_dateupdate)
                       values (getSerial(), v_now, TG_OP, 
                       		   new.ID, new.nome, new."data", new.conta, new.dateinsert, new.dateupdate,
                       		   old.ID, old.nome, old."data", old.conta, old.dateinsert, old.dateupdate);    
  ELSE
      insert into journal_facial (journal_caixamagica_serial, journal_actiondate, journal_actiontype,
                                 old_id, old_nome, old_data, old_conta, old_dateinsert, old_dateupdate)
                       values (getSerial(), v_now, TG_OP, 
                       		   old.ID, old.nome, old."data", old.conta, old.dateinsert, old.dateupdate);
      RETURN OLD;
  END IF;
  RETURN NULL;
END;
$BODY$"""
conn1.manipular(statement)

# Cria TRIGGER para jornalizacao da tabela de facial
conn1.manipular("drop trigger if exists trigger_journal_facial on facial;")
statement="""create trigger  trigger_journal_facial
AFTER INSERT OR UPDATE OR DELETE ON facial
FOR EACH ROW
EXECUTE PROCEDURE setJournalFacial();"""
conn1.manipular(statement)


# Cria procedure de jornalizacao da tabela de cobrancas
statement="""CREATE OR REPLACE FUNCTION setJournalCobrancas()
RETURNS trigger 
language plpgsql
AS $BODY$
declare v_now timestamp := (now() at time zone 'utc');
BEGIN
  IF (TG_OP = 'INSERT') THEN
      insert into journal_cobrancas (journal_caixamagica_serial, journal_actiondate, journal_actiontype,
                                  new_id, new_valor, new_datahora, new_tipopagamento, new_tipoidentificacao, new_fotousuario,
                                  new_enviada, new_saldo, new_beneficio, new_viagemid, new_geolocalizacao, new_datahorafalhaintegr,
                                  new_status_internet)
                       values (getSerial(), v_now, TG_OP, 
                       		   new.id, new.valor, new.datahora, new.tipopagamento, new.tipoidentificacao, new.fotousuario,
                               new.enviada, new.saldo, new.beneficio, new.viagemid, new.geolocalizacao, new.datahorafalhaintegr,
                               new.status_internet);     
      RETURN NEW;
  elsif (TG_OP = 'UPDATE') then
      insert into journal_cobrancas (journal_caixamagica_serial, journal_actiondate, journal_actiontype,
                                  new_id, new_valor, new_datahora, new_tipopagamento, new_tipoidentificacao, new_fotousuario,
                                  new_enviada, new_saldo, new_beneficio, new_viagemid, new_geolocalizacao, new_datahorafalhaintegr,
                                  new_status_internet,      
                                 old_id, old_valor, old_datahora, old_tipopagamento, old_tipoidentificacao, old_fotousuario,
                                 old_enviada, old_saldo, old_beneficio, old_viagemid, old_geolocalizacao, old_datahorafalhaintegr,
                                 old_status_internet)
                       values (getSerial(), v_now, TG_OP, 
                       		   new.id, new.valor, new.datahora, new.tipopagamento, new.tipoidentificacao, new.fotousuario,
                               new.enviada, new.saldo, new.beneficio, new.viagemid, new.geolocalizacao, new.datahorafalhaintegr,
                               new.status_internet,
                       		   old.id, old.valor, old.datahora, old.tipopagamento, old.tipoidentificacao, old.fotousuario,
                               old.enviada, old.saldo, old.beneficio, old.viagemid, old.geolocalizacao, old.datahorafalhaintegr,
                               old.status_internet                               
                              );    
  ELSE
      insert into journal_cobrancas (journal_caixamagica_serial, journal_actiondate, journal_actiontype,
                                 old_id, old_valor, old_datahora, old_tipopagamento, old_tipoidentificacao, old_fotousuario,
                                 old_enviada, old_saldo, old_beneficio, old_viagemid, old_geolocalizacao, old_datahorafalhaintegr,
                                 old_status_internet)
                       values (getSerial(), v_now, TG_OP, 
                       		   old.id, old.valor, old.datahora, old.tipopagamento, old.tipoidentificacao, old.fotousuario,
                               old.enviada, old.saldo, old.beneficio, old.viagemid, old.geolocalizacao, old.datahorafalhaintegr,
                               old.status_internet);
      RETURN OLD;
  END IF;
  RETURN NULL;
END;
$BODY$"""
conn1.manipular(statement)

# Cria TRIGGER para jornalizacao da tabela de cobrancas
conn1.manipular("drop trigger if exists trigger_journal_cobrancas on cobrancas;")
statement="""create trigger  trigger_journal_cobrancas
AFTER INSERT OR UPDATE OR DELETE ON cobrancas
FOR EACH ROW
EXECUTE PROCEDURE setJournalCobrancas();"""
conn1.manipular(statement)

# todo: implementar a mesma rotina para operadores
statement="""CREATE OR REPLACE FUNCTION setJournalOperadores()
RETURNS trigger 
language plpgsql
AS $BODY$
declare v_now timestamp := (now() at time zone 'utc');
BEGIN
  IF (TG_OP = 'INSERT') THEN
      insert into journal_operadores (journal_caixamagica_serial, journal_actiondate, journal_actiontype,
                                  new_id, new_id_web, new_nome, new_data, new_id_qr, new_matricula, new_dateinsert,
                                  new_dateupdate)
                       values (getSerial(), v_now, TG_OP, 
                       		   new.id, new.id_web, new.nome, new."data", new.id_qr, new.matricula, new.dateinsert,
                               new.dateupdate);     
      RETURN NEW;
  elsif (TG_OP = 'UPDATE') then
      insert into journal_operadores (journal_caixamagica_serial, journal_actiondate, journal_actiontype,
                                  new_id, new_id_web, new_nome, new_data, new_id_qr, new_matricula, new_dateinsert,
                                  new_dateupdate,
                                  old_id, old_id_web, old_nome, old_data, old_id_qr, old_matricula, old_dateinsert,
                                  old_dateupdate
                                  )
                       values (getSerial(), v_now, TG_OP, 
                       		   new.id, new.id_web, new.nome, new."data", new.id_qr, new.matricula, new.dateinsert,
                               new.dateupdate,
                               old.id, old.id_web, old.nome, old."data", old.id_qr, old.matricula, old.dateinsert,
                               old.dateupdate
                              );    
  ELSE
      insert into journal_operadores (journal_caixamagica_serial, journal_actiondate, journal_actiontype,
								  old_id, old_id_web, old_nome, old_data, old_id_qr, old_matricula, old_dateinsert,
                                  old_dateupdate)
                       values (getSerial(), v_now, TG_OP, 
                       		   old.id, old.id_web, old.nome, old."data", old.id_qr, old.matricula, old.dateinsert,
                               old.dateupdate);
      RETURN OLD;
  END IF;
  RETURN NULL;
END;
$BODY$"""
conn1.manipular(statement)

# Cria trigger de journal para operadores
conn1.manipular("drop trigger if exists trigger_journal_operadores on operadores;")
statement="""create trigger trigger_journal_operadores
AFTER INSERT OR UPDATE OR DELETE ON operadores
FOR EACH ROW
EXECUTE PROCEDURE setJournalOperadores();"""
conn1.manipular(statement)


# Adiciona colunas de integracao 
conn1.manipular("alter table journal_contas add column if not exists journal_datahoraintegrada timestamp;")
conn1.manipular("alter table journal_contas add column if not exists journal_integrada boolean default false;")
conn1.manipular("alter table journal_saldo add column if not exists journal_datahoraintegrada timestamp;")
conn1.manipular("alter table journal_saldo add column if not exists journal_integrada boolean default false;")
conn1.manipular("alter table journal_operadores add column if not exists journal_datahoraintegrada timestamp;")
conn1.manipular("alter table journal_operadores add column if not exists journal_integrada boolean default false;")
conn1.manipular("alter table journal_cobrancas add column if not exists journal_datahoraintegrada timestamp;")
conn1.manipular("alter table journal_cobrancas add column if not exists journal_integrada boolean default false;")
conn1.manipular("alter table journal_facial add column if not exists journal_datahoraintegrada timestamp;")
conn1.manipular("alter table journal_facial add column if not exists journal_integrada boolean default false;")

conn1.manipular("alter table historico_internet add column if not exists datahoraenviado timestamp;")
conn1.manipular("alter table historico_internet add column if not exists enviado boolean default false;")

# Cria procedure de expurgo de casos ja integrados
statement = """create or replace procedure public.sp_expurgaJournalIntegrados()
  LANGUAGE plpgsql
as $procedure$
  begin 
	  -- expurga registros ja integrados da tabela de contas
	  delete from journal_contas where journal_integrada = true; 
	  -- expurga registros ja integrados da tabela de saldo
	  delete from journal_saldo where journal_integrada = true; 
	  -- expurga registros ja integrados da tabela de facial
	  delete from journal_facial where journal_integrada = true; 
	  -- expurga registros ja integrados da tabela de operadores
	  delete from journal_operadores where journal_integrada = true; 
	  -- expurga registros ja integrados da tabela de cobrancas
	  delete from journal_cobrancas where journal_integrada = true;
  end;
$procedure$"""
conn1.manipular(statement)

# Cria procedure de expurgo de casos ja integrados (historicos status internet)
statement = """create or replace procedure public.sp_expurgaHistoricoInternetIntegrados()
  LANGUAGE plpgsql
as $procedure$
  begin
          -- expurga registros ja integrados 
          delete from historico_internet where enviado = true;
          
  end;
$procedure$"""
conn1.manipular(statement)


# Cria procedure de expurgo de casos  expirados journal
statement = """create or replace procedure public.sp_expurgaJournalLegado(p_num_dias integer)
  LANGUAGE plpgsql
as $procedure$
  declare v_data timestamp;
  begin 
          v_data := ((now() at time zone 'utc')::DATE - p_num_dias);
	  
	  -- expurga registros ja integrados da tabela de contas, independentemente se foram ja integrados
	  delete from journal_contas where journal_actiondate < v_data; 
	  -- expurga registros ja integrados da tabela de saldo, independentemente se foram ja integrados
	  delete from journal_saldo where journal_actiondate < v_data; 
	  -- expurga registros ja integrados da tabela de facial, independentemente se foram ja integrados
	  delete from journal_facial where journal_actiondate < v_data; 
	  -- expurga registros ja integrados da tabela de operadores, independentemente se foram ja integrados
	  delete from journal_operadores where journal_actiondate < v_data; 
	  -- expurga registros ja integrados da tabela de cobrancas, independentemente se foram ja integrados
	  delete from journal_cobrancas where journal_actiondate < v_data;
  end;
$procedure$"""
conn1.manipular(statement)

# Cria procedure de expurgo de casos  expirados historico internet
statement = """create or replace procedure public.sp_expurgaHistoricoInternetLegado(p_num_dias integer)
  LANGUAGE plpgsql
as $procedure$
  declare v_data timestamp;
  begin
          v_data := ((now() at time zone 'utc')::DATE - p_num_dias);

          -- expurga registros ja integrados, independentemente se foram ja integrados
          delete from historico_internet  where datahorautc < v_data;
          
  end;
$procedure$"""
conn1.manipular(statement)

# Cria coluna para ser o cmapo de chave unica na tabela de cobrancas
conn1.manipular("alter table cobrancas add column if not exists chavecobranca varchar(100);")

# Cria procedure de determinacao da chave unica do registro de cobranca
statement = """CREATE OR REPLACE FUNCTION setChaveCobranca()
 RETURNS trigger
 LANGUAGE plpgsql
AS $function$
declare v_saida varchar(10);
declare v_guid varchar(100);
begin
  select pg_sleep(.1) into v_saida;
  select (md5(concat(replace(trim(to_char(EXTRACT(EPOCH FROM now() AT TIME ZONE 'UTC'), '9999999999999999999999999.9999999999')),'.', ''), '.', getSerial(), '.', new.id)))::uuid into v_guid; 
 
  NEW.chavecobranca = v_guid;
  RETURN NEW;
END;
$function$;"""
conn1.manipular(statement)

# Cria trigger
conn1.manipular("drop trigger if exists trigger_journal_cobrancas_bi on cobrancas;")
statement="""create trigger  trigger_journal_cobrancas_bi
BEFORE INSERT ON cobrancas
FOR EACH ROW
EXECUTE PROCEDURE setChaveCobranca();"""
conn1.manipular(statement)

# Cria Unique key para a coluna de cobranca
conn1.manipular("ALTER TABLE cobrancas DROP CONSTRAINT IF EXISTS cobrancas_uk1;")
conn1.manipular("ALTER TABLE cobrancas ADD constraint cobrancas_uk1 UNIQUE (chavecobranca);")

# Cria a tabela de controle de abertura/encerramento da viagem
statement="""create table if not exists viagem
(
   viagemid int8 not null,
   dataabertura timestamp,
   dataencerramento timestamp,
   tipoabertura varchar(10),
   tipoencerramento varchar(10),
   CONSTRAINT viagem_pk primary key(viagemid)
);"""
conn1.manipular(statement)

# Adiciona coluna de bloqueio, na tabela de conta
# Versao >= 1.5.2 passara a utilizar o bloqueio na conta e nao mais no saldo
# Adiciona tambem  tabela d econtrole com o historico do bloqueio/desblqoueio
conn1.manipular("alter table contas add column if not exists bloqueado boolean default false;")
conn1.manipular("alter table contas add column if not exists databloqueiostatus timestamptz(0);")

statement="""create table if not exists contas_historico_status_bloqueio
(
  id bigserial not null,
  id_web int8 not null,
  bloqueado boolean not null,
  databloqueiostatus timestamptz(0) not null,
  constraint contas_historico_status_bloqueio_pk primary key (id)
);"""
conn1.manipular(statement)

# Adiciona tabela com o itinerario da viagem
statement="""create table if not exists itinerario_viagem
(
  id bigserial not null,
  registroviagemid int8 not null,
  pontoid int8 not null,
  linhaid int8 not null,
  ordem int not null,
  sentidovolta boolean,
  geolocalizacao varchar(100),
  nome varchar(200),
  descricao varchar(200),
  bairro varchar(200),
  cidade varchar(200),
  uf varchar(10),
  cep varchar(20),
  logradouro varchar(200),
  numero varchar(100),
  datainsercao timestamptz(0),
  constraint itinerario_viagem_pk primary key(id)
);"""
conn1.manipular(statement)

# Adiciona tabela com o historico do registro da viagem
statement="""create table if not exists sentido_viagem
(
  id bigserial not null,
  registroviagemid int8 not null,
  dataregistro timestamptz(0) not null,
  sentido varchar(10),
  constraint sentido_viagem_pk primary key (id)
);"""
conn1.manipular(statement)

# Adiciona coluna para envio da informacao para uma central de dados
conn1.manipular("alter table contas_historico_status_bloqueio add column if not exists enviado boolean default false")
conn1.manipular("alter table contas_historico_status_bloqueio add column if not exists dataenviado timestamptz(0)")

# Adiciona tabela auxiliar de controle de  reconhecimento facial
statement = """create table if not exists aux_rec_facial 
(id bigserial not null,
 matriz_origem cube,
 matriz_encontrada cube,
 prioridade int,
 distancia_euclidiana float,
 contaid int8,
 constraint aux_rec_facial_pk primary key(id)
);"""
conn1.manipular(statement)

# Adiciona tabela de registros proximos de cobranca
statement = """create table if not exists cobrancas_prox_rec_facial 
(id bigserial not null,
 matriz_origem cube,
 matriz_encontrada cube,
 prioridade int,
 distancia_euclidiana float,
 cobrancaid int8,
 contaid int8,
 datahora timestamptz(0),
 constraint cobrancas_prox_rec_facial_pk primary key(id)
);"""
conn1.manipular(statement)

# Adiciona procedure a ser utilizada pela trigger de cobranca (para gravar os registros mais proximos)
statement = """CREATE OR REPLACE FUNCTION public.setCobrancasProxRecfacial()
 RETURNS trigger
 LANGUAGE plpgsql
AS $function$
declare v_now timestamp := (now() at time zone 'utc');
BEGIN
  IF (TG_OP = 'INSERT' and new.tipoidentificacao = 3) THEN 
      insert into cobrancas_prox_rec_facial (matriz_origem, matriz_encontrada, prioridade, distancia_euclidiana, 
      			  cobrancaid,datahora,contaid)
                select a.matriz_origem, a.matriz_encontrada, a.prioridade, a.distancia_euclidiana, new.id, v_now, a.contaid
                from aux_rec_facial a;
      delete from aux_rec_facial;
               
      RETURN NEW;
  END IF;
  RETURN NULL;
END;
$function$;"""
conn1.manipular(statement)

# recria trigger
statement="drop trigger if exists trigger_cobrancas_rec_facial_ai on cobrancas;"
conn1.manipular(statement)
statement="""create trigger  trigger_cobrancas_rec_facial_ai
after INSERT ON cobrancas
FOR EACH ROW
EXECUTE PROCEDURE setCobrancasProxRecfacial();"""
conn1.manipular(statement)

# Cria tabela de controle
statement="""create table if not exists controle_comprime_logs
(
  id serial not null,
  data_acao varchar(8) not null,
  path_file varchar(200) not null,
  constraint controle_comprime_logs_pk primary key(id),
  constraint controle_comprime_logs_uk unique (data_acao)
);"""
conn1.manipular(statement)

# Cria indice na tabela facial, por conta
statement = """DO
$do$
declare
  v_existe int;
BEGIN 
	SELECT count(*) into v_existe
	FROM pg_catalog.pg_indexes p 
	where p.indexname like 'facial_conta_idx%';

	if v_existe <= 0 then
		CREATE INDEX facial_conta_idx ON public.facial using GIST (conta);
	end if;
end
$do$"""
conn1.manipular(statement)

# Cria tabela de controle de particoes faciais
statement = """create table if not exists facial_range_contas
(
  id bigserial not null,
  particao varchar(100) not null,
  contaid_de int8 not null,
  contaid_ate int8 not null,
  constraint facial_range_contas_pk primary key(id),
  constraint facial_range_contas_uk1 unique (particao)
);"""
conn1.manipular(statement)

# Cria tabela de sentido da viagem, informado pelo motorista
statement = """create table if not exists viagem_sentido_motorista
(
  id bigserial not null,
  registroviagemid int8 not null,
  codigolinha varchar(30) not null,
  motoristaid int8 not null,
  dateinsert timestamptz(0) default now(),
  constraint viagem_sentido_motorista_pk primary key (id)
);"""
conn1.manipular(statement)

# Cria tabela de logs nos reconhecimentos faciais
statement = """create table if not exists facial_reconhecimento_logs
(
  id bigserial not null,
  foto_path varchar(1000),
  contaid int8,
  dist_euclidiana float,
  dateinsert timestamptz(0) default now(),
  constraint facial_reconhecimento_logs_pk primary key (id)
);"""
conn1.manipular(statement)

# Adiciona tabela para controle do saldo para cada conta/cliente
statement="""create table if not exists contas_saldos
(
  id bigserial not null,
  contaid int8 not null,
  saldo_valor float default 0,
  data_atualizacao_local timestamptz(0),
  data_atualizacao_servidor timestamptz(0),
  constraint contas_saldos_pk primary key (id),
  constraint contas_saldos_uk unique(contaid)
);"""
conn1.manipular(statement)

# Adiciona tabela para controle do valor da tarifa da viagem
statement="""create table if not exists tarifa_viagem
(
  id bigserial not null,
  viagemid int8 not null,
  valor float not null default 0,
  dataregistro timestamptz(0),
  constraint tarifa_viagem_pk primary key(id),
  constraint tarifa_viagem_uk unique(viagemid)
);"""
conn1.manipular(statement)


# Adiciona  trigger para controle dos status de bloqueio/desbloqueio

time.sleep(0.2)
