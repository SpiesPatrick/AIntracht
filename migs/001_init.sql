CREATE SCHEMA IF NOT EXISTS aintracht;

CREATE TABLE IF NOT EXISTS aintracht.saison (
    id int4 GENERATED ALWAYS AS IDENTITY(
        INCREMENT BY 1 MINVALUE 1 MAXVALUE 2147483647 START 1 CACHE 1 NO CYCLE
    ) NOT NULL,
    jahr varchar(5) NOT NULL,
    CONSTRAINT saison_jahr_key UNIQUE (jahr),
    CONSTRAINT saison_pkey PRIMARY KEY (id)
);

CREATE TABLE IF NOT EXISTS aintracht.spiele (
    id int4 GENERATED ALWAYS AS IDENTITY(
        INCREMENT BY 1 MINVALUE 1 MAXVALUE 2147483647 START 1 CACHE 1 NO CYCLE
    ) NOT NULL,
    spieltag int4 NULL,
    saison_id int4 NULL,
    CONSTRAINT spiele_pkey PRIMARY KEY (id),
    CONSTRAINT spiele_spieltag_saison_id_key UNIQUE (spieltag, saison_id),
    CONSTRAINT spiele_saison_id_fkey FOREIGN KEY (saison_id) REFERENCES aintracht.saison(id)
);

CREATE TABLE IF NOT EXISTS aintracht.begegnungen (
    id int4 GENERATED ALWAYS AS IDENTITY(
        INCREMENT BY 1 MINVALUE 1 MAXVALUE 2147483647 START 1 CACHE 1 NO CYCLE
    ) NOT NULL,
    heim_mannschaft text NULL,
    gast_mannschaft text NULL,
    heim_tore int4 NULL,
    gast_tore int4 NULL,
    spiele_id int4 NULL,
    CONSTRAINT begegnungen_pkey PRIMARY KEY (id),
    CONSTRAINT begegnungen_spiele_id_fkey FOREIGN KEY (spiele_id) REFERENCES aintracht.spiele(id)
);
