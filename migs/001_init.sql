CREATE SCHEMA IF NOT EXISTS aintracht;

DROP TABLE IF EXISTS aintracht.begegnungen CASCADE;
DROP TABLE IF EXISTS aintracht.spiele CASCADE;
DROP TABLE IF EXISTS aintracht.saison CASCADE;

CREATE TABLE aintracht.spiele (
    saison INT NOT NULL,
    spieltag INT NOT NULL,
    getippt BOOL DEFAULT FALSE,
    CONSTRAINT spiele_pkey PRIMARY KEY (saison, spieltag)
);

CREATE TABLE aintracht.begegnungen (
    id SERIAL PRIMARY KEY,
    heim_mannschaft TEXT NOT NULL,
    gast_mannschaft TEXT NOT NULL,
    heim_tore INT,
    gast_tore INT,
    saison INT NOT NULL,
    spieltag INT NOT NULL,
    CONSTRAINT fk_spiele
        FOREIGN KEY (saison, spieltag)
        REFERENCES aintracht.spiele (saison, spieltag)
        ON DELETE CASCADE
);
