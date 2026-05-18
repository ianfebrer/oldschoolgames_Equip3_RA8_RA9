<div align="center">
  <h1>🕹️ Old School Games</h1>
  <p><strong>Projecte de classe DAW - Python Web Project 2026</strong></p>
  <p>Una aplicació web retro desenvolupada amb Python i Flask per reviure la màgia dels jocs d'arcade clàssics.</p>

  <!-- Badges -->
  <img src="https://img.shields.io/badge/Python-3776AB?style=for-the-badge&logo=python&logoColor=white" alt="Python" />
  <img src="https://img.shields.io/badge/Flask-000000?style=for-the-badge&logo=flask&logoColor=white" alt="Flask" />
  <img src="https://img.shields.io/badge/MariaDB-003545?style=for-the-badge&logo=mariadb&logoColor=white" alt="MariaDB" />
  <img src="https://img.shields.io/badge/MongoDB-4EA94B?style=for-the-badge&logo=mongodb&logoColor=white" alt="MongoDB" />
  <img src="https://img.shields.io/badge/Tailwind_CSS-38B2AC?style=for-the-badge&logo=tailwind-css&logoColor=white" alt="Tailwind CSS" />
</div>

---

## 🌟 Característiques Principals

Aquesta aplicació implementa una arquitectura client-servidor basada en **Programació Orientada a Objectes (POO)** per modelar els dominis de l'aplicació, combinant bases de dades relacionals i NoSQL per a un rendiment òptim.

- 🎮 **3 Jocs Retro Inclosos**: Pong, Trexpres i Memory.
- 🔐 **Autenticació i Gestió d'Usuaris**: Registre segur, login i emmagatzematge de contrasenyes amb hash.
- 🏆 **Rànquings i Puntuacions**: Sistema de *Top 10* i historial de resultats per joc.
- 💾 **Persistència de Dades Híbrida**: Ús combinat de MariaDB (dades estructurades) i MongoDB (esdeveniments en temps real i logs).

## 🛠️ Tecnologies i Arquitectura

- **Frontend**: HTML5, CSS3 (Tailwind CSS), JavaScript (Animacions, lògica de jocs).
- **Backend**: Python 3, Flask (Rutes, API REST).
- **Bases de Dades**:
  - **MariaDB**: Usuaris, autenticació, catàleg de jocs, puntuacions finals.
  - **MongoDB**: Esdeveniments del joc (col·lisions, moviments), estats en temps real, logs de partides.

## 📁 Estructura del Projecte

```bash
📦 oldschoolgames
 ┣ 📂 app
 ┃ ┣ 📂 models      # Classes POO (User, Game, GameSession, GameState...)
 ┃ ┣ 📂 routes      # Rutes web i endpoints de l'API
 ┃ ┣ 📂 templates   # Vistes HTML (Jinja2)
 ┃ ┣ 📂 static      # Arxius estàtics (JS, CSS, imatges, sons)
 ┃ ┗ 📂 data        # Fitxers JSON o dades de suport
 ┣ 📂 database      # Esquemes SQL i dades inicials (seed)
 ┣ 📜 .env.example  # Plantilla de variables d'entorn
 ┣ 📜 run.py        # Punt d'entrada de l'aplicació Flask
 ┗ 📜 requirements.txt # Dependències de Python
```

## 🚀 Instal·lació i Execució (Local)

1. **Clonar el repositori i preparar l'entorn virtual**:
   ```powershell
   py -m venv .venv
   .\.venv\Scripts\Activate.ps1
   ```

2. **Instal·lar les dependències**:
   ```powershell
   pip install -r requirements.txt
   ```

3. **Configuració de l'entorn**:
   Crea un fitxer `.env` a l'arrel del projecte copiant `.env.example` i ajustant les variables (connexions a BD, claus secretes).

4. **Preparar la Base de Dades (MariaDB)**:
   Importa els fitxers de la carpeta `database/`:
   - Primer `schema.sql` (creació de taules).
   - Després `seed.sql` (dades inicials i jocs disponibles).

5. **Executar l'aplicació**:
   ```powershell
   python run.py
   ```
   *L'aplicació estarà disponible a: `http://127.0.0.1:5000`*

## 🌐 Rutes i API Disponibles

**Rutes Web Principals:**
- `/` - Pàgina principal / Landing
- `/auth/register` & `/auth/login` - Gestió d'accessos
- `/games/pong` | `/games/trexpres` | `/games/memory` - Jocs actius

**Endpoints API:**
- `POST /api/register`
- `POST /api/login`
- `POST /api/sessions`

## 👥 Equip de Desenvolupament (Equip 3)

- **Adrià**: Sistema d'usuaris i autenticació (POO/Flask), base de dades relacional MariaDB i UI de login, registre i catàleg.
- **Gabriel**: Lògica core de jocs (estats), integració amb MongoDB (esdeveniments/logs), sons/animacions i creació del vídeo-resum.
- **Ian**: Resultats i guardat de partides, puntuacions (Top 10 MariaDB i dades Mongo), API REST/WebSockets i UI del rànquing.

---

📄 **Manual d'Usuari**: Per a més detalls sobre l'ús de l'aplicació, pots consultar el [Manual d'usuari (PDF)](manual%20d%27usuari.pdf).
