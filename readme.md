# Old School Games
Projecte de classe DAW - Python Web Project 2026

Aplicacio web feta amb **Python + Flask** que inclou 3 jocs retro (Pong, Trexpres i Memory), autenticacio d'usuaris i ranking per joc.

## Equip
- Adria
- Gabriel
- Ian

## Objectiu del projecte
Aplicar arquitectura client-servidor amb Flask, frontend amb HTML/CSS/JS i programacio orientada a objectes per gestionar usuaris, jocs i resultats.

## Part d'Adria
- Registre i login connectats a MariaDB.
- Contrasenyes guardades amb hash.
- Cataleg de jocs carregat des de la taula `games`.
- Configuracio local amb `.env` i `.env.example`.

## Tecnologies
- Python 3
- Flask
- MariaDB
- MongoDB
- HTML
- CSS (Tailwind)
- JavaScript

## Estructura del projecte
- `app/models`: classes (`User`, `Game`, `GameSession`, `Base`)
- `app/routes`: rutes web i API
- `app/templates`: vistes HTML
- `app/static`: JS i imatges
- `database`: esquema SQL i dades inicials
- `app/data`: fitxers JSON legacy o de suport

## Instal.lacio i execucio (Windows PowerShell)
1. `py -m venv .venv`
2. `.\.venv\Scripts\Activate.ps1`
3. `pip install -r requirements.txt`
4. Crear un fitxer `.env` a partir de `.env.example`
5. Importar `database/schema.sql` i `database/seed.sql` a MariaDB
6. `python run.py`
7. Obrir `http://127.0.0.1:5000`

## Rutes principals
- `/`
- `/auth/register`
- `/auth/login`
- `/auth/logout`
- `/games/pong`
- `/games/trexpres`
- `/games/memory`

## API
- `POST /api/register`
- `POST /api/login`
- `POST /api/sessions`

## Manual d'usuari
- [Manual d'usuari (PDF)](manual%20d%27usuari.pdf)
