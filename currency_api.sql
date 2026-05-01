-- ============================================================
--  CURRENCY TRACKER API — DATABASE SETUP
--  CFG Data & MySQL Assignment - Topic Assignment 4
-- ============================================================
--  Description : Creates the database and table required for
--                the Currency Tracker Flask API.
--                Run this script once before starting the API.
-- ============================================================

DROP DATABASE IF EXISTS currency_tracker;
CREATE DATABASE currency_tracker;
USE currency_tracker;

-- ------------------------------------------------------------
-- Table: exchange_rates
-- Stores currency codes, names, symbols, and their USD rate.
-- updated_at records when the rate was last refreshed.
-- ------------------------------------------------------------
CREATE TABLE exchange_rates (
    id            INT           NOT NULL AUTO_INCREMENT,
    currency_code VARCHAR(3)    NOT NULL,
    currency_name VARCHAR(50)   NOT NULL,
    symbol        VARCHAR(5)    NOT NULL,
    usd_rate      DECIMAL(10,6) NOT NULL,
    updated_at    DATETIME      NOT NULL DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
    CONSTRAINT pk_exchange_rates  PRIMARY KEY (id),
    CONSTRAINT uq_currency_code   UNIQUE (currency_code),
    CONSTRAINT chk_usd_rate       CHECK (usd_rate > 0)
);

-- ------------------------------------------------------------
-- Seed data: GBP, USD, EUR and more
-- ------------------------------------------------------------
INSERT INTO exchange_rates (currency_code, currency_name, symbol, usd_rate) VALUES
    ('USD', 'US Dollar',          '$',   1.000000),
    ('GBP', 'British Pound',      '£',   1.270000),
    ('EUR', 'Euro',               '€',   1.090000),
    ('JPY', 'Japanese Yen',       '¥',   0.006700),
    ('CHF', 'Swiss Franc',        'CHF', 1.110000),
    ('CAD', 'Canadian Dollar',    'C$',  0.740000),
    ('AUD', 'Australian Dollar',  'A$',  0.660000),
    ('TRY', 'Turkish Lira',       '₺',   0.031000);
