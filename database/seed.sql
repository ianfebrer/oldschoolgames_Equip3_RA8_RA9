-- Plantilla d'orientacio per dades inicials.
-- Cada membre pot afegir aqui dades de prova quan la seva part estigui definida.

USE oldschoolgames;

-- ADRIA:
-- - Jocs inicials del cataleg, si finalment es guarden a MariaDB.
INSERT INTO games (slug, name, description, image) VALUES
    ('pong', 'Pong', 'Juego de Pong', 'pong.gif'),
    ('trexpres', 'Trexpres', 'Juego de Trexpres', 'trexpres.gif'),
    ('memory', 'Memory', 'Juego de Memory', 'joc-memoria.gif')
ON DUPLICATE KEY UPDATE
    name = VALUES(name),
    description = VALUES(description),
    image = VALUES(image);

-- GABRIEL:
-- - Dades de prova de MongoDB, si cal documentar-les.

-- IAN:
-- - Puntuacions o resultats de prova, si cal.
