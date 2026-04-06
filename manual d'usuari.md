# Manual d'Usuari - OldSchoolGames
## 1. Introducció

OldSchoolGames és una aplicació web per a jugar títols arcade clàssics des del navegador. El seu objectiu és oferir partides ràpides, competitives i fàcils d'entendre, amb una interfície retro centrada en l'acció. En aquesta guia trobessis, en ordre d'ús real, com entrar, crear compte, jugar, guardar resultats i consultar el rànquing.

Aquest manual aquesta pensat per a usuaris finals sense perfil tècnic. Per això es prioritzen instruccions clares, rutes concretes de pantalla i resolució de problemes freqüents sense entrar en els detalls interns del sistema.
## 2. Inici ràpid

Si vols començar en menys de cinc minuts, obre la pàgina principal (`/`) i comprova que accedeixes al panell de jocs. Si encara no tens compte, entra en `'/auth/register'`, escriu el teu usuari i contrasenya i completa el registre. Quan rebis el missatge d'alta correcta, passa a `'/auth/login'`, inicia sessió i torna automàticament a la portada.

Amb la sessió activa, tria un dels tres jocs disponibles (Pong, Trexpres o Memory) i prem `START GAME`. Dins de la pantalla del joc, prem `INICIAR` per a començar. En acabar, usa `FINALITZAR` per a tancar la partida i permetre que el sistema intenti guardar el teu puntuació alrànquing del joc corresponent.
## 3. Navegació principal

L'aplicació s'organitza en una ruta d'inici (`/`), rutes de autenticació (`/auth/login`, `/auth/register`, `/auth/logout`) i rutes de joc (`/games/pong`, `/games/trexpres`, `/games/memory`). Des de la portada pots saltar a qualsevol joc i, al mateix temps, veure el leaderboard del joc seleccionat.

El flux recomanat per a un usuari nou és entrar en la portada, crear compte, iniciar sessió i començar la seva primera partida. El flux habitual per a un usuari recurrent és iniciar sessió, jugar diverses partides i tornar a la portada per a revisar la seva posició al rànquing.
## 4. Compte i sessió

Per a crear un compte, entra en `'/auth/register'`, completa els camps d'usuari i contrasenya i prem `REGISTRAR-SE`. Si el nom d'usuari no existeix, la pàgina t'avisarà i te portará a la pàgina del login. Si el nom ja está en ús, veuràs un missatge perquè provis amb un altre usuari.

Per a iniciar sessió, entra a `'/auth/login'`, introdueix les teves credencials i prem `INICIA SESSIO`. Amb accés correcte, tornaràs a la portada i hauràs habilitat el joc amb guardat de resultats. Si apareix el missatge de credencials incorrectes, revisa que no hi hagi errors d'escriptura abans de tornar a intentar.

Per a tancar sessió, accedeix a `'/auth/logout'`. El sistema elimina la sessió activa i redirigeix al login. És recomanable tancar sessió quan acabis, especialment si comparteixes dispositiu.
## 5. Jocs disponibles

Els tres jocs comparteixen una estructura comuna: accés des de la portada, botó `INICIAR` per a començar, `PAUSAR` per parar temporalment i `FINALITZAR` per a tancar la partida. Mentre jugues, veuràs informació de temps i puntuació al panell lateral.
### 5.1 Pong

En Pong, l'objectiu és retornar la bola i sumar punts quan superes a la defensa rival. El control principal es realitza amb el ratolí sobre el tauler, movent la pala del jugador. La partida pot tancar-se manualment amb `FINALITZAR`.
### 5.2 Trexpres

Trexpres combina memòria visual i rapidesa de decision. Primer es mostra un patron de referència i després has de seleccionar la casella correcta per a continuar. Si encertes, avances i puges puntuació; si falles, la partida acaba i es mostra el resum final.
### 5.3 Memory

En Memory has de trobar parelles de cartes fent clic sobre el tauler. A mesura que completes nivells, augmenta la complexitat del tauler i l'exigència de memòria. Quan finalitzes, es mostra nivell aconseguit, temps total i puntuació obtinguda.
## 6. Puntuacions i leaderboard

El sistema registra resultats en finalitzar cada partida, sempre que tinguis sessió iniciada. Cada envio inclou joc, puntuació i temps de partida. Si no hi ha sessió activa, el resultat no es guarda en rànquing.

Al leaderboard de la portada es mostra el TOP 5 per joc. El criteri principal d'ordre és la puntuació mes alta i, en cas d'empat, es prioritza el menor temps. Per a cada usuari es manté la seva millor marca per joc, per la qual cosa una partida pitjor no reemplaça un resultat anterior mes alt.
## 7. FAQ i solució de problemes

Si no pots registrar-te perquè l'usuari ja existeix, intenta iniciar sessió amb aquest nom o crea un altre diferent. Si no pots iniciar sessió, revisa acuradament usuari i contrasenya, incloent majúscules, minúscules i espais accidentals.

Si entres en un joc però no et deixa jugar o no guarda puntuació, el primer és confirmar que la sessió continua activa. Després, acaba la partida amb el flux normal de joc i torna a la portada per a revisar el rànquing del joc correcte.

Si no puges posicions en la taula, recorda que només compta el teu millor puntuació per joc i que, en empat, el temps decideix l'ordre. Si el rànquing mostrat no coincideix amb el joc que acabes de jugar, canvia el filtre en la portada a Pong, Trexpres o Memory segons correspongui.