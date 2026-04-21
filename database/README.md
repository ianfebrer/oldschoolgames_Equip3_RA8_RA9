# Database setup

Aquest directori conte l'estructura comuna de base de dades del projecte.

La idea es que aquest directori serveixi com a punt de coordinacio entre els tres membres de l'equip. El repositori guarda l'estructura i les instruccions, pero la base de dades real no es puja a GitHub.

## Fitxers

- `schema.sql`: crea la base de dades relacional i les taules ja definides.
- `seed.sql`: insereix dades inicials o dades de prova.
- `.env.example`: exemple de configuracio local per connectar Flask amb MariaDB i MongoDB.

## Estat actual

Ja esta definida la part d'Adria:

- Base de dades relacional proposada: `oldschoolgames`.
- Taula `users` per al registre, login i autenticacio.
- Taula `games` per al cataleg de jocs.
- Dades inicials dels jocs a `seed.sql`.

Encara no estan definides les parts de Gabriel i Ian. Les han d'afegir ells a les seves branques.

## Com usar-ho

Ara mateix nomes estan definides les taules de la part d'Adria: usuaris i cataleg de jocs.

Gabriel i Ian han d'omplir la seva part a les seves branques, sense modificar la part d'autenticacio si no cal.

Ordre recomanat:

```sql
SOURCE database/schema.sql;
SOURCE database/seed.sql;
```

Tambe es poden importar des de phpMyAdmin, MySQL Workbench o DBeaver.

## Repartiment

- Adria: usuaris, autenticacio, sessions i cataleg de jocs.
- Gabriel: logica core dels jocs, estats/logs/events amb MongoDB, sons i animacions.
- Ian: puntuacions, guardat de partides, leaderboard/top 10 i pantalla final.