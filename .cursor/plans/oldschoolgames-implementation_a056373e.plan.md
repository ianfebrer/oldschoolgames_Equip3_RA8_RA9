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
    - id: phase5-qa-docs
      content: Completar tests críticos, pruebas integradas y documentación de uso
      status: pending
    - id: team-rotation
      content: Aplicar rotación semanal A/B/C para que todos toquen backend, frontend y testing
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
- Multiplayer.
- API pública externa.
- Efectos avanzados de audio/animación.

## Lo que NO haremos ahora

-

## Qué tenéis que aprender (mínimo) antes de empezar

- Flask básico: rutas, plantillas y formularios.
- SQLAlchemy básico: modelos y guardar datos.
- Sesiones/login en Flask (`Flask-Login`).
- JavaScript básico para teclado/ratón.
- Peticiones `fetch` (enviar datos del juego al backend).

## Estructura simple del proyecto

- [run.py](run.py) -> arranca la app
- [app/**init**.py](app/__init__.py) -> crea la app Flask
- [app/models/](app/models/) -> clases de base de datos
- [app/routes/](app/routes/) -> endpoints y páginas
- [app/templates/](app/templates/) -> HTML
- [app/static/js/games/](app/static/js/games/) -> lógica JS de los 3 juegos
- [tests/](tests/) -> pruebas básicas

## Clases OO obligatorias (muy simple)

- `User` -> usuario y contraseña
- `Game` -> información del juego (`name`, `description`)
- `GameSession` -> una partida concreta (inicio, fin, estado)
- `Score` -> resultado final (puntos, tiempo, fecha)

Regla fácil: si algo representa “una cosa del dominio”, haced una clase.

## Plan por semanas (paso a paso)

### Semana 1 - Base + Login

1. Crear proyecto Flask mínimo.
2. Configurar base de datos SQLite.
3. Crear modelo `User`.
4. Hacer páginas: registro y login.
5. Proteger ruta `/lobby` para usuarios logueados.
6. Test simple: registrar y loguear usuario.

### Semana 2 - Modelos de juego y menú

1. Crear modelos `Game`, `GameSession`, `Score`.
2. Insertar 3 juegos iniciales en DB (`Pong`, `Trexpres`, `AtencioFlash`).
3. Crear página `/lobby` con botones a los 3 juegos.
4. Crear plantillas vacías de cada juego.
5. Test simple: ver lista de juegos logueado.

### Semana 3 - Juego 1 completo (Pong)

1. JS de Pong con teclado.
2. Endpoint para recibir resultado (`POST /api/scores`).
3. Validar datos en backend (usuario logueado, juego válido, puntos válidos).
4. Guardar score y tiempo en DB.
5. Mostrar mensaje final de partida.
6. Test API: guarda score correctamente.

### Semana 4 - Juegos 2 y 3 completos

1. Hacer `Trexpres` (teclado + clic).
2. Hacer `AtencioFlash` (ratón).
3. Reutilizar el mismo endpoint de score.
4. Mostrar mensaje final en ambos.
5. Test API: guarda score de los 3 juegos.

### Semana 5 - Rankings + cierre

1. Página ranking por juego (`/ranking/<game_id>`).
2. Mostrar top 10 ordenado.
3. Página de historial del usuario actual.
4. Revisión final de errores y limpieza de código.
5. README con pasos de instalación y uso.

## Reparto entre 3 personas (todos hacen de todo)

No hay especialistas. Todos rotan cada semana.

- Semana 1:
    - Persona A: backend login
    - Persona B: HTML login/register
    - Persona C: tests básicos
- Semana 2:
    - A: modelos DB
    - B: rutas y lobby
    - C: tests de rutas/modelos
- Semana 3:
    - A: JS Pong
    - B: endpoint score + validaciones
    - C: test API + mensaje final
- Semana 4:
    - A: JS Trexpres
    - B: JS AtencioFlash
    - C: backend integración + tests
- Semana 5:
    - A: ranking
    - B: historial usuario
    - C: README + pruebas finales

Regla de rotación: la siguiente semana cada persona cambia de tipo de tarea.

## Checklist de “terminado” para cada funcionalidad

- Funciona en local sin errores.
- Tiene al menos 1 test.
- Se ve en pantalla (demo manual).
- Se guarda en base de datos (si aplica).
- Otro compañero lo revisa.

## Entrega final

- App Flask funcional con 3 juegos.
- Login/registro funcionando.
- Scores y tiempos guardados.
- Ranking por juego.
- README de instalación para principiantes.
