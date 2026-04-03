# Python Web Project 2026 - Checklist

Estat revisat: 03/04/2026

## Lliurament

- [ ] Enllaç de GitHub preparat per entregar
- [ ] PDF manual per a usuaris finals

## Base del projecte (Flask + web)

- [x] Arquitectura client-servidor
- [x] Backend amb Flask
- [x] Frontend amb HTML + CSS + JavaScript
- [x] Estructura separada (`models`, `routes`, `templates`, `static`)

## Disseny orientat a objectes (obligatori)

- [x] Classe per a usuaris (`User`)
- [x] Classe per a jocs (`Game`)
- [x] Classe per a resultats/sessions (`GameSession`)
- [x] Model d'estat de joc (temps + puntuació) en tots els jocs — sense camp d'intents a l'API (decisió del projecte)

## Jocs obligatoris

- [x] Almenys 3 jocs diferents
- [x] Joc tipus Pong
- [x] Joc d'agilitat mental tipus T-REX/Estrop
- [x] Tercer joc tipus classic (Memory)

## Backend funcional

- [x] Rutes per carregar les pàgines dels jocs
- [x] Gestió de sessió d'usuari (login/logout)
- [x] Validacio robusta de dades rebudes del client
- [ ] Guardar historial complet de partides per usuari

## Frontend i interaccio

- [x] Accions de teclat
- [x] Moviment/clic del ratoli
- [x] Comunicacio amb el backend (API)

## Funcionalitats avaluables (obligatories)

- [x] Registrar i autenticar usuaris
- [x] Elegir entre almenys 3 jocs diferents
- [x] Guardar puntuació i temps
- [x] Mostrar un ranking per cada joc
- [x] Mostrar missatges de resultat al final de la partida
- [] Disseny responsive base per telèfon i tauleta (crec que no)

## Ampliacions (no obligatories)

- [] Dificultat progressiva (Memory amb nivells de graella; Pong/Trexpres sense progressió explícita)
- [x] API tipus REST per puntuacions (basica)
- [ ] Mode multijugador basic
- [ ] Sons i animacions addicionals
