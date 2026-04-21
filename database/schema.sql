-- Esquema inicial per acordar l'estructura de bases de dades.
-- Aquest fitxer crea la base relacional i les taules de la part d'Adria.
-- Gabriel i Ian haureu d'omplir la vostra seccio quan treballeu a la vostra branca.

-- NOM PROPOSAT DE LA BASE DE DADES RELACIONAL:
-- oldschoolgames

CREATE DATABASE IF NOT EXISTS oldschoolgames
    CHARACTER SET utf8mb4
    COLLATE utf8mb4_unicode_ci;

USE oldschoolgames;

-- =========================================================
-- ADRIA: usuaris, autenticacio i cataleg de jocs
-- =========================================================
-- Objectiu:
-- - Definir les taules necessaries per al registre/login.
-- - Definir la taula o estructura relacional per al cataleg de jocs.
-- - Evitar guardar contrasenyes en text pla.

CREATE TABLE IF NOT EXISTS users (
    id INT AUTO_INCREMENT PRIMARY KEY,
    username VARCHAR(50) NOT NULL UNIQUE,
    password_hash VARCHAR(255) NOT NULL,
    created_at TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP
);

CREATE TABLE IF NOT EXISTS games (
    id INT AUTO_INCREMENT PRIMARY KEY,
    slug VARCHAR(50) NOT NULL UNIQUE,
    name VARCHAR(100) NOT NULL,
    description TEXT NOT NULL,
    image VARCHAR(255),
    created_at TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP
);

-- =========================================================
-- GABRIEL: logica core, estats i logs amb MongoDB
-- =========================================================
-- Objectiu:
-- - Decidir quines dades dinamiques dels jocs van a MongoDB.
-- - Definir col.leccions i format dels documents.
-- - No dependre de taules SQL per dades molt variables.

-- Pendent d'implementar per Gabriel:
-- MongoDB collections / document structure

-- =========================================================
-- IAN: puntuacions, guardat de partides i leaderboard
-- =========================================================
-- Objectiu:
-- - Definir com es guarden puntuacions/resultats.
-- - Decidir relacio amb usuaris i jocs.
-- - Preparar consultes per al Top 10.

-- Pendent d'implementar per Ian:
-- CREATE TABLE ...
