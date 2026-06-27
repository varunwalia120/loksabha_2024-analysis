CREATE DATABASE IF NOT EXISTS loksabha_2024;
USE loksabha_2024;

CREATE TABLE IF NOT EXISTS constituencies (
    pc_name VARCHAR(100) PRIMARY KEY,
    state   VARCHAR(100) NOT NULL
);

CREATE TABLE IF NOT EXISTS candidates (
    id             INT AUTO_INCREMENT PRIMARY KEY,
    pc_name        VARCHAR(100) NOT NULL,
    candidate_name VARCHAR(200) NOT NULL,
    gender         VARCHAR(10),
    age            INT,
    category       VARCHAR(20),
    party_name     VARCHAR(100),
    total_votes    INT,
    valid_votes    INT,
    total_electors INT,
    FOREIGN KEY (pc_name) REFERENCES constituencies(pc_name)
);

CREATE TABLE IF NOT EXISTS winners (
    pc_name        VARCHAR(100) PRIMARY KEY,
    candidate_name VARCHAR(200),
    gender         VARCHAR(10),
    age            INT,
    party_name     VARCHAR(100),
    total_votes    INT,
    FOREIGN KEY (pc_name) REFERENCES constituencies(pc_name)
);

CREATE TABLE IF NOT EXISTS margins (
    pc_name VARCHAR(100) PRIMARY KEY,
    margin  INT,
    FOREIGN KEY (pc_name) REFERENCES constituencies(pc_name)
);

CREATE TABLE IF NOT EXISTS turnout (
    pc_name            VARCHAR(100) PRIMARY KEY,
    state              VARCHAR(100),
    total_electors     INT,
    total_votes_polled INT,
    turnout_pct        DECIMAL(5,2),
    FOREIGN KEY (pc_name) REFERENCES constituencies(pc_name)
);

CREATE TABLE IF NOT EXISTS nota (
    pc_name    VARCHAR(100) PRIMARY KEY,
    nota_votes INT,
    FOREIGN KEY (pc_name) REFERENCES constituencies(pc_name)
);