---
name: oldschoolgames-implementation
overview: Plan de implementación para una app Flask orientada a objetos con 3 juegos retro, autenticación, sesiones y rankings, repartiendo el trabajo entre 3 personas generalistas con rotación por fases.
todos:
  - id: phase1-bootstrap
    content: Definir scaffold Flask (factory, config, extensions, modelos base) y auth funcional
    status: pending
  - id: phase2-oo-domain
    content: Implementar modelo OO de juegos/sesiones/resultados con validación backend
    status: pending
  - id: phase3-games-ui
    content: Construir 3 juegos frontend conectados al backend y guardar resultados
    status: pending
  - id: phase4-ranking-results
    content: Implementar ranking por juego, historial y mensajes de fin de partida
    status: pending
  - id: phase5-cierre
    content: Pruebas manuales, documentación de uso y demo final
    status: pending
  - id: team-rotation
    content: Aplicar rotación semanal A/B/C para que todos toquen backend, frontend y cierre
    status: pending
isProject: false
---

# Old School Games - Plan super simple (principiantes)

## Objetivo (en una frase)

Hacer una web con Flask donde un usuario se registra, juega a 3 juegos retro y se guardan sus puntuaciones para ver rankings.

## Lo que SI haremos ahora

- Registro, login y logout.
- Menú para elegir 3 juegos.
- Guardar puntuación y tiempo de cada partida.
- Ranking por cada juego.
- Mensaje final al terminar partida.
- Sin versión móvil (solo escritorio).

## Lo que NO haremos ahora

- Multiplayer.
- API pública externa.
- Efectos avanzados de audio/animación.

## Qué tenéis que aprender (mínimo) antes de empezar

- Flask básico: rutas, plantillas y formularios.
- JSON y archivos: leer/escribir con `json` de la stdlib.
- Sesiones/login en Flask (`Flask-Login`).
- JavaScript básico para teclado/ratón.
- Peticiones `fetch` (enviar datos del juego al backend).

## Estructura simple del proyecto

- [run.py](run.py) -> arranca la app
- [app/**init**.py](app/__init__.py) -> crea la app Flask
- [app/data/](app/data/) -> archivos JSON (`users.json`, `scores.json`, etc.)
- [app/models/](app/models/) -> clases OO que leen/escriben en JSON (sin base de datos)
- [app/routes/](app/routes/) -> endpoints y páginas
- [app/templates/](app/templates/) -> HTML
- [app/static/js/games/](app/static/js/games/) -> lógica JS de los 3 juegos

## Persistencia: archivos JSON (sin base de datos)

Usamos JSON porque es simple, legible y no requiere dependencias. Un archivo por entidad:

- `users.json` -> lista de usuarios (username, password_hash)
- `games.json` -> lista de juegos (id, name, description) — se crea al inicio
- `scores.json` -> lista de resultados (user_id, game_id, points, time, date)

Regla fácil: cada clase tiene métodos para cargar/guardar desde su archivo JSON.

## Clases OO obligatorias (muy simple)

- `User` -> usuario y contraseña (lee/escribe `users.json`)
- `Game` -> información del juego (`name`, `description`) (lee `games.json`)
- `GameSession` -> una partida concreta (inicio, fin, estado)
- `Score` -> resultado final (puntos, tiempo, fecha) (lee/escribe `scores.json`)

Regla fácil: si algo representa “una cosa del dominio”, haced una clase.

## Plan por semanas (paso a paso)

### Semana 1 - Base + Login

1. Crear proyecto Flask mínimo.
2. Crear carpeta `app/data/` y archivo `users.json` vacío `[]`.
3. Crear modelo `User` con métodos para leer/escribir en JSON.
4. Hacer páginas: registro y login.
5. Proteger ruta `/lobby` para usuarios logueados.
6. Probar manualmente: registrar usuario, cerrar sesión, volver a entrar.

### Semana 2 - Modelos de juego y menú

1. Crear modelos `Game`, `GameSession`, `Score` con métodos JSON.
2. Crear `games.json` con los 3 juegos iniciales (`Pong`, `Trexpres`, `AtencioFlash`).
3. Crear página `/lobby` con botones a los 3 juegos.
4. Crear plantillas vacías de cada juego.
5. Probar manualmente: entrar al lobby y ver que los 3 juegos aparecen.

### Semana 3 - Juego 1 completo (Pong)

1. JS de Pong con teclado.
2. Endpoint para recibir resultado (`POST /api/scores`).
3. Validar datos en backend (usuario logueado, juego válido, puntos válidos).
4. Guardar score y tiempo en `scores.json`.
5. Mostrar mensaje final de partida.
6. Probar manualmente: jugar una partida, terminar y comprobar que el score aparece en `scores.json`.

### Semana 4 - Juegos 2 y 3 completos

1. Hacer `Trexpres` (teclado + clic).
2. Hacer `AtencioFlash` (ratón).
3. Reutilizar el mismo endpoint de score.
4. Mostrar mensaje final en ambos.
5. Probar manualmente: jugar a los 3 juegos y comprobar que cada uno guarda su score correctamente.

### Semana 5 - Rankings + cierre

1. Página ranking por juego (`/ranking/<game_id>`).
2. Mostrar top 10 ordenado.
3. Página de historial del usuario actual.
4. Revisión final: probar todo el flujo (registro, login, 3 juegos, ranking, historial).
5. README con pasos de instalación y uso para que otro pueda arrancar el proyecto.

## Reparto entre 3 personas (todos hacen de todo)

No hay especialistas. Todos rotan cada semana.

- Semana 1:
  - Persona A: backend login
  - Persona B: HTML login/register
  - Persona C: CSS base + probar flujo de registro/login
- Semana 2:
  - A: modelos JSON
  - B: rutas y lobby
  - C: estilos del lobby + probar navegación
- Semana 3:
  - A: JS Pong
  - B: endpoint score + validaciones
  - C: mensaje final + probar guardado de scores
- Semana 4:
  - A: JS Trexpres
  - B: JS AtencioFlash
  - C: integración backend + probar los 3 juegos
- Semana 5:
  - A: ranking
  - B: historial usuario
  - C: README + demo final y pruebas manuales completas

Regla de rotación: la siguiente semana cada persona cambia de tipo de tarea.

## Checklist de “terminado” para cada funcionalidad

- Funciona en local sin errores.
- Se ha probado manualmente en el navegador.
- Se ve bien en pantalla.
- Se guarda en archivos JSON (si aplica).
- Otro compañero lo ha revisado.

## Entrega final

- App Flask funcional con 3 juegos.
- Login/registro funcionando.
- Scores y tiempos guardados.
- Ranking por juego.
- README de instalación para principiantes.

