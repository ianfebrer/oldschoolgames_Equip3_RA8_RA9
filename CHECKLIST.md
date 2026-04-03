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
- [ ] Model complet d'estat de joc (temps + intents + puntuacio) en tots els jocs

## Jocs obligatoris

- [x] Almenys 3 jocs diferents
- [x] Joc tipus Pong
- [x] Joc d'agilitat mental tipus T-REX/Estrop
- [x] Tercer joc tipus classic (Memory)

## Backend funcional

- [x] Rutes per carregar les pagines dels jocs
- [x] Gestio de sessio d'usuari (login/logout)
- [ ] Validacio robusta de dades rebudes del client
- [ ] Guardar historial complet de partides per usuari

## Frontend i interaccio

- [x] Accions de teclat
- [x] Moviment/clic del ratoli
- [x] Comunicacio amb el backend (API)

## Funcionalitats avaluables (obligatories)

- [ ] Registrar i autenticar usuaris (parcial: login si, registre falla per bug)
- [x] Elegir entre almenys 3 jocs diferents
- [ ] Guardar puntuacions i temps de cada partida (parcial)
- [ ] Mostrar un ranking per cada joc (parcial)
- [ ] Mostrar missatges de resultat al final de cada partida en tots els jocs
- [x] Disseny responsive base per telefon i tauleta

## Ampliacions (no obligatories)

- [ ] Dificultat progressiva
- [x] API tipus REST per puntuacions (basica)
- [ ] Mode multijugador basic
- [ ] Sons i animacions addicionals
