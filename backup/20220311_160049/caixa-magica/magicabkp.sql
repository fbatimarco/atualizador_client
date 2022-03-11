--
-- PostgreSQL database dump
--

-- Dumped from database version 10.10 (Ubuntu 10.10-0ubuntu0.18.04.1)
-- Dumped by pg_dump version 10.10 (Ubuntu 10.10-0ubuntu0.18.04.1)

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
-- Name: plpgsql; Type: EXTENSION; Schema: -; Owner: 
--

CREATE EXTENSION IF NOT EXISTS plpgsql WITH SCHEMA pg_catalog;


--
-- Name: EXTENSION plpgsql; Type: COMMENT; Schema: -; Owner: 
--

COMMENT ON EXTENSION plpgsql IS 'PL/pgSQL procedural language';


--
-- Name: cube; Type: EXTENSION; Schema: -; Owner: 
--

CREATE EXTENSION IF NOT EXISTS cube WITH SCHEMA public;


--
-- Name: EXTENSION cube; Type: COMMENT; Schema: -; Owner: 
--

COMMENT ON EXTENSION cube IS 'data type for multidimensional cubes';


SET default_tablespace = '';

SET default_with_oids = false;

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
    beneficio bigint
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
-- Name: saldo id; Type: DEFAULT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.saldo ALTER COLUMN id SET DEFAULT nextval('public.saldo_id_seq'::regclass);


--
-- Data for Name: beneficios; Type: TABLE DATA; Schema: public; Owner: postgres
--

COPY public.beneficios (id, id_atribuicao, nomebeneficio, tipodesconto, valordesconto, periodos, conta) FROM stdin;
\.


--
-- Data for Name: cobrancas; Type: TABLE DATA; Schema: public; Owner: postgres
--

COPY public.cobrancas (id, valor, datahora, tipopagamento, tipoidentificacao, fotousuario, enviada, saldo, beneficio) FROM stdin;
\.


--
-- Data for Name: contas; Type: TABLE DATA; Schema: public; Owner: postgres
--

COPY public.contas (id, id_web, cpf, nome) FROM stdin;
\.


--
-- Data for Name: facial; Type: TABLE DATA; Schema: public; Owner: postgres
--

COPY public.facial (id, nome, data, conta) FROM stdin;
\.


--
-- Data for Name: saldo; Type: TABLE DATA; Schema: public; Owner: postgres
--

COPY public.saldo (id, id_web, porvalor, conta, bloqueado) FROM stdin;
\.


--
-- Name: beneficios_id_seq; Type: SEQUENCE SET; Schema: public; Owner: postgres
--

SELECT pg_catalog.setval('public.beneficios_id_seq', 1, false);


--
-- Name: cobrancas_id_seq; Type: SEQUENCE SET; Schema: public; Owner: postgres
--

SELECT pg_catalog.setval('public.cobrancas_id_seq', 1, false);


--
-- Name: contas_id_seq; Type: SEQUENCE SET; Schema: public; Owner: postgres
--

SELECT pg_catalog.setval('public.contas_id_seq', 1, false);


--
-- Name: facial_id_seq; Type: SEQUENCE SET; Schema: public; Owner: postgres
--

SELECT pg_catalog.setval('public.facial_id_seq', 4, true);


--
-- Name: saldo_id_seq; Type: SEQUENCE SET; Schema: public; Owner: postgres
--

SELECT pg_catalog.setval('public.saldo_id_seq', 1, false);


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
-- Name: cobrancas cobrancas_pkey; Type: CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.cobrancas
    ADD CONSTRAINT cobrancas_pkey PRIMARY KEY (id);


--
-- Name: contas contas_cpf_key; Type: CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.contas
    ADD CONSTRAINT contas_cpf_key UNIQUE (cpf);


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
-- Name: contas_id_web_idx; Type: INDEX; Schema: public; Owner: postgres
--

CREATE UNIQUE INDEX contas_id_web_idx ON public.contas USING btree (id_web);


--
-- Name: beneficios beneficios_fk; Type: FK CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.beneficios
    ADD CONSTRAINT beneficios_fk FOREIGN KEY (conta) REFERENCES public.contas(id_web);


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

