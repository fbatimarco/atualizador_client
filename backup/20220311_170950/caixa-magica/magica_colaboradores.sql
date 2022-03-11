--
-- PostgreSQL database dump
--

-- Dumped from database version 12.3
-- Dumped by pg_dump version 12.3

SET statement_timeout = 0;
SET lock_timeout = 0;
SET idle_in_transaction_session_timeout = 0;
SET client_encoding = 'UTF8';
SET standard_conforming_strings = on;
SELECT pg_catalog.set_config('search_path', '', false);
SET check_function_bodies = false;
SET xmloption = content;
SET client_min_messages = warning;
SET row_security = off;

--
-- Name: cube; Type: EXTENSION; Schema: -; Owner: -
--

CREATE EXTENSION IF NOT EXISTS cube WITH SCHEMA public;


--
-- Name: EXTENSION cube; Type: COMMENT; Schema: -; Owner: 
--

COMMENT ON EXTENSION cube IS 'data type for multidimensional cubes';


SET default_tablespace = '';

SET default_table_access_method = heap;

--
-- Name: beneficios; Type: TABLE; Schema: public; Owner: postgres
--

CREATE TABLE public.beneficios (
    id integer NOT NULL,
    id_atribuicao bigint,
    nomebeneficio character varying,
    tipodesconto character varying,
    valordesconto real,
    periodos character varying,
    conta bigint
);


ALTER TABLE public.beneficios OWNER TO postgres;

--
-- Name: beneficios_id_seq; Type: SEQUENCE; Schema: public; Owner: postgres
--

CREATE SEQUENCE public.beneficios_id_seq
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER TABLE public.beneficios_id_seq OWNER TO postgres;

--
-- Name: beneficios_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: postgres
--

ALTER SEQUENCE public.beneficios_id_seq OWNED BY public.beneficios.id;


--
-- Name: cartao; Type: TABLE; Schema: public; Owner: postgres
--

CREATE TABLE public.cartao (
    id_web bigint NOT NULL,
    numero character varying NOT NULL,
    conta bigint NOT NULL
);


ALTER TABLE public.cartao OWNER TO postgres;

--
-- Name: cobrancas; Type: TABLE; Schema: public; Owner: postgres
--

CREATE TABLE public.cobrancas (
    id integer NOT NULL,
    valor real,
    datahora character varying NOT NULL,
    tipopagamento character varying NOT NULL,
    tipoidentificacao integer NOT NULL,
    fotousuario character varying,
    enviada boolean NOT NULL,
    saldo bigint,
    beneficio bigint,
    viagemid bigint,
    geolocalizacao character
);


ALTER TABLE public.cobrancas OWNER TO postgres;

--
-- Name: cobrancas_id_seq; Type: SEQUENCE; Schema: public; Owner: postgres
--

CREATE SEQUENCE public.cobrancas_id_seq
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER TABLE public.cobrancas_id_seq OWNER TO postgres;

--
-- Name: cobrancas_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: postgres
--

ALTER SEQUENCE public.cobrancas_id_seq OWNED BY public.cobrancas.id;


--
-- Name: contas; Type: TABLE; Schema: public; Owner: postgres
--

CREATE TABLE public.contas (
    id bigint NOT NULL,
    id_web bigint NOT NULL,
    cpf character varying,
    nome character varying
);


ALTER TABLE public.contas OWNER TO postgres;

--
-- Name: contas_id_seq; Type: SEQUENCE; Schema: public; Owner: postgres
--

CREATE SEQUENCE public.contas_id_seq
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER TABLE public.contas_id_seq OWNER TO postgres;

--
-- Name: contas_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: postgres
--

ALTER SEQUENCE public.contas_id_seq OWNED BY public.contas.id;


--
-- Name: facial; Type: TABLE; Schema: public; Owner: postgres
--

CREATE TABLE public.facial (
    id integer NOT NULL,
    nome character varying(80) NOT NULL,
    data public.cube NOT NULL,
    conta bigint
);


ALTER TABLE public.facial OWNER TO postgres;

--
-- Name: facial_id_seq; Type: SEQUENCE; Schema: public; Owner: postgres
--

CREATE SEQUENCE public.facial_id_seq
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER TABLE public.facial_id_seq OWNER TO postgres;

--
-- Name: facial_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: postgres
--

ALTER SEQUENCE public.facial_id_seq OWNED BY public.facial.id;


--
-- Name: operadores; Type: TABLE; Schema: public; Owner: postgres
--

CREATE TABLE public.operadores (
    id bigint NOT NULL,
    id_web bigint NOT NULL,
    nome character varying NOT NULL,
    data character varying,
    id_qr character varying
);


ALTER TABLE public.operadores OWNER TO postgres;

--
-- Name: operadores_id_seq; Type: SEQUENCE; Schema: public; Owner: postgres
--

CREATE SEQUENCE public.operadores_id_seq
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER TABLE public.operadores_id_seq OWNER TO postgres;

--
-- Name: operadores_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: postgres
--

ALTER SEQUENCE public.operadores_id_seq OWNED BY public.operadores.id;


--
-- Name: saldo; Type: TABLE; Schema: public; Owner: postgres
--

CREATE TABLE public.saldo (
    id integer NOT NULL,
    id_web bigint NOT NULL,
    porvalor boolean NOT NULL,
    conta bigint NOT NULL,
    bloqueado boolean NOT NULL
);


ALTER TABLE public.saldo OWNER TO postgres;

--
-- Name: saldo_id_seq; Type: SEQUENCE; Schema: public; Owner: postgres
--

CREATE SEQUENCE public.saldo_id_seq
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER TABLE public.saldo_id_seq OWNER TO postgres;

--
-- Name: saldo_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: postgres
--

ALTER SEQUENCE public.saldo_id_seq OWNED BY public.saldo.id;


--
-- Name: temperatura; Type: TABLE; Schema: public; Owner: postgres
--

CREATE TABLE public.temperatura (
    id integer NOT NULL,
    data_e_hora character varying(255) NOT NULL,
    temperatura character varying(255) NOT NULL,
    localizacao character varying(255),
    usuario bigint,
    enviado boolean NOT NULL,
    ambiente character varying(255)
);


ALTER TABLE public.temperatura OWNER TO postgres;

--
-- Name: temperatura_id_seq; Type: SEQUENCE; Schema: public; Owner: postgres
--

CREATE SEQUENCE public.temperatura_id_seq
    AS integer
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER TABLE public.temperatura_id_seq OWNER TO postgres;

--
-- Name: temperatura_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: postgres
--

ALTER SEQUENCE public.temperatura_id_seq OWNED BY public.temperatura.id;


--
-- Name: beneficios id; Type: DEFAULT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.beneficios ALTER COLUMN id SET DEFAULT nextval('public.beneficios_id_seq'::regclass);


--
-- Name: cobrancas id; Type: DEFAULT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.cobrancas ALTER COLUMN id SET DEFAULT nextval('public.cobrancas_id_seq'::regclass);


--
-- Name: contas id; Type: DEFAULT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.contas ALTER COLUMN id SET DEFAULT nextval('public.contas_id_seq'::regclass);


--
-- Name: facial id; Type: DEFAULT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.facial ALTER COLUMN id SET DEFAULT nextval('public.facial_id_seq'::regclass);


--
-- Name: operadores id; Type: DEFAULT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.operadores ALTER COLUMN id SET DEFAULT nextval('public.operadores_id_seq'::regclass);


--
-- Name: saldo id; Type: DEFAULT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.saldo ALTER COLUMN id SET DEFAULT nextval('public.saldo_id_seq'::regclass);


--
-- Name: temperatura id; Type: DEFAULT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.temperatura ALTER COLUMN id SET DEFAULT nextval('public.temperatura_id_seq'::regclass);


--
-- Name: beneficios beneficios_pkey; Type: CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.beneficios
    ADD CONSTRAINT beneficios_pkey PRIMARY KEY (id);


--
-- Name: beneficios beneficios_un; Type: CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.beneficios
    ADD CONSTRAINT beneficios_un UNIQUE (id_atribuicao);


--
-- Name: cartao cartao_un; Type: CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.cartao
    ADD CONSTRAINT cartao_un UNIQUE (id_web);


--
-- Name: cartao cartao_un2; Type: CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.cartao
    ADD CONSTRAINT cartao_un2 UNIQUE (numero);


--
-- Name: cobrancas cobrancas_pkey; Type: CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.cobrancas
    ADD CONSTRAINT cobrancas_pkey PRIMARY KEY (id);


--
-- Name: contas contas_guid_key; Type: CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.contas
    ADD CONSTRAINT contas_guid_key UNIQUE (id_web);


--
-- Name: contas contas_pkey; Type: CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.contas
    ADD CONSTRAINT contas_pkey PRIMARY KEY (id);


--
-- Name: facial facial_pkey; Type: CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.facial
    ADD CONSTRAINT facial_pkey PRIMARY KEY (id);


--
-- Name: saldo saldo_pk; Type: CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.saldo
    ADD CONSTRAINT saldo_pk PRIMARY KEY (id);


--
-- Name: saldo saldo_un; Type: CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.saldo
    ADD CONSTRAINT saldo_un UNIQUE (id_web);


--
-- Name: temperatura temperatura_pk; Type: CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.temperatura
    ADD CONSTRAINT temperatura_pk PRIMARY KEY (id);


--
-- Name: contas_id_web_idx; Type: INDEX; Schema: public; Owner: postgres
--

CREATE UNIQUE INDEX contas_id_web_idx ON public.contas USING btree (id_web);


--
-- Name: beneficios beneficios_fk; Type: FK CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.beneficios
    ADD CONSTRAINT beneficios_fk FOREIGN KEY (conta) REFERENCES public.contas(id_web);


--
-- Name: cartao cartao_fk; Type: FK CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.cartao
    ADD CONSTRAINT cartao_fk FOREIGN KEY (conta) REFERENCES public.contas(id_web);


--
-- Name: cobrancas cobrancas_fk; Type: FK CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.cobrancas
    ADD CONSTRAINT cobrancas_fk FOREIGN KEY (beneficio) REFERENCES public.beneficios(id_atribuicao);


--
-- Name: cobrancas cobrancas_saldo; Type: FK CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.cobrancas
    ADD CONSTRAINT cobrancas_saldo FOREIGN KEY (saldo) REFERENCES public.saldo(id_web);


--
-- Name: facial facial_fk; Type: FK CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.facial
    ADD CONSTRAINT facial_fk FOREIGN KEY (conta) REFERENCES public.contas(id_web) ON UPDATE CASCADE ON DELETE CASCADE;


--
-- Name: saldo saldo_fk; Type: FK CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.saldo
    ADD CONSTRAINT saldo_fk FOREIGN KEY (conta) REFERENCES public.contas(id_web);


--
-- PostgreSQL database dump complete
--

