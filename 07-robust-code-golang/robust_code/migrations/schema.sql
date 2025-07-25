--
-- PostgreSQL database dump
--

-- Dumped from database version 16.9
-- Dumped by pg_dump version 16.9

SET statement_timeout = 0;
SET lock_timeout = 0;
SET idle_in_transaction_session_timeout = 0;
SET client_encoding = 'WIN1252';
SET standard_conforming_strings = on;
SELECT pg_catalog.set_config('search_path', '', false);
SET check_function_bodies = false;
SET xmloption = content;
SET client_min_messages = warning;
SET row_security = off;

SET default_tablespace = '';

SET default_table_access_method = heap;

--
-- Name: schema_migration; Type: TABLE; Schema: public; Owner: root
--

CREATE TABLE public.schema_migration (
    version character varying(14) NOT NULL
);


ALTER TABLE public.schema_migration OWNER TO root;

--
-- Name: users; Type: TABLE; Schema: public; Owner: root
--

CREATE TABLE public.users (
    id uuid NOT NULL,
    name character varying(255) NOT NULL,
    email character varying(255) NOT NULL,
    email_verified_at timestamp without time zone,
    password character varying(255) NOT NULL,
    remember_token character varying(100),
    created_at timestamp without time zone NOT NULL,
    updated_at timestamp without time zone NOT NULL
);


ALTER TABLE public.users OWNER TO root;

--
-- Name: schema_migration schema_migration_pkey; Type: CONSTRAINT; Schema: public; Owner: root
--

ALTER TABLE ONLY public.schema_migration
    ADD CONSTRAINT schema_migration_pkey PRIMARY KEY (version);


--
-- Name: users users_pkey; Type: CONSTRAINT; Schema: public; Owner: root
--

ALTER TABLE ONLY public.users
    ADD CONSTRAINT users_pkey PRIMARY KEY (id);


--
-- Name: schema_migration_version_idx; Type: INDEX; Schema: public; Owner: root
--

CREATE UNIQUE INDEX schema_migration_version_idx ON public.schema_migration USING btree (version);


--
-- PostgreSQL database dump complete
--

