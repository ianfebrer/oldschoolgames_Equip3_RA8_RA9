# Old School Games
Projecte de classe DAW - Python Web Project 2026

Aplicació web feta amb **Python + Flask** que inclou 3 jocs retro (Pong, Trexpres i Memory), autenticació d’usuaris i rànquing per joc.

## Equip
- Derek
- Miguel
- Roy

## Objectiu del projecte
Aplicar arquitectura client-servidor amb Flask, frontend amb HTML/CSS/JS i programació orientada a objectes per gestionar usuaris, jocs i resultats.

## Funcionalitats
- Registre i login d’usuaris
- Selecció entre 3 jocs
- Guardat de puntuació i temps
- Rànquing per joc
- Missatge final de partida
- Interacció amb teclat i ratolí

## Tecnologies
- Python 3
- Flask
- HTML
- CSS (Tailwind)
- JavaScript

## Estructura del projecte
- `app/models`: classes (`User`, `Game`, `GameSession`, `Base`)
- `app/routes`: rutes web i API
- `app/templates`: vistes HTML
- `app/static`: JS i imatges
- `app/data`: fitxers JSON de dades

## Instal·lació i execució (Windows PowerShell)
1. `py -m venv .venv`
2. `.\.venv\Scripts\Activate.ps1`
3. `pip install -r requirements.txt`
4. `python run.py`
5. Obrir `http://127.0.0.1:5000`

## Rutes principals
- `/` portada
- `/auth/register` registre
- `/auth/login` login
- `/auth/logout` logout
- `/games/pong`
- `/games/trexpres`
- `/games/memory`

## API
- `POST /api/register`
- `POST /api/login`
- `POST /api/sessions`

## Manual d’usuari
- [Manual d’usuari (PDF)](manual%20d%27usuari.pdf)
