const gameboard = document.getElementById("board");

const EMOJIS = [
	"🍎",
	"🍌",
	"🍇",
	"🍓",
	"🍒",
	"🍍",
	"🥝",
	"🍋",
	"🍊",
	"🍉",
	"🍑",
	"🥭",
	"🍈",
	"🍐",
	"🫐",
	"🍏",
	"🍅",
	"🥑",
	"🌶",
	"🍄",
	"🥕",
	"🌽",
	"🥔",
	"🧅",
	"🥦",
	"🥬",
	"🫛",
	"🫑",
	"🥒",
	"🫒",
];

const LEVEL_GRIDS = [
	{ f: 2, c: 2 },
	{ f: 2, c: 3 },
	{ f: 2, c: 4 },
	{ f: 3, c: 4 },
	{ f: 4, c: 4 },
	{ f: 4, c: 5 },
	{ f: 5, c: 6 },
	{ f: 6, c: 6 },
];

let estat = "idle";
let nivellIndex = 0;
let score = 0;
let parsMatched = 0;
let totalPars = 0;

let hasFlippedCard = false;
let bloquejarBoard = false;
let firstCard = null;
let secondCard = null;

function getGridForLevel(idx) {
	const i = Math.min(Math.max(0, idx), LEVEL_GRIDS.length - 1);
	return LEVEL_GRIDS[i];
}

function emojiVarietyForLevel(idx) {
	const base = 6 + idx * 2;
	return Math.min(EMOJIS.length, Math.max(8, base));
}

//Esta funcio el que fa es barrejar la llista "cards", creant una variable "j" que amb
// que amb el metode Math.random barreje les cartes, i despues fem un intercambi de posicio entre
// "i" i la "j"
function barrejar(llista) {
	for (let i = llista.length - 1; i > 0; i--) {
		const j = Math.floor(Math.random() * (i + 1));
		[llista[i], llista[j]] = [llista[j], llista[i]];
	}
	return llista;
}

function buildDeckForLevel(idx, numPar) {
	const variety = emojiVarietyForLevel(idx);
	const poolSlice = EMOJIS.slice(0, variety);
	barrejar(poolSlice);
	const triat = poolSlice.slice(0, numPar);
	const baralla = triat.concat(triat);
	barrejar(baralla);
	return baralla;
}

function setGraellaBoard(files, columnes) {
	if (!gameboard) return;
	gameboard.style.display = "grid";
	gameboard.style.gridTemplateColumns = `repeat(${columnes}, minmax(0, 1fr))`;
	gameboard.style.gridTemplateRows = `repeat(${files}, minmax(0, 1fr))`;
	gameboard.style.gap = "10px";
	gameboard.style.width = "100%";
	gameboard.style.height = "100%";
	gameboard.style.padding = "20px";
	gameboard.style.boxSizing = "border-box";
	gameboard.style.alignContent = "center";
}

function tamanyFontCarta(files, columnes) {
	const n = files * columnes;
	if (n <= 6) return "3rem";
	if (n <= 12) return "2.25rem";
	if (n <= 20) return "1.75rem";
	if (n <= 30) return "1.35rem";
	return "1.1rem";
}

function actualitzarHud() {
	const el = document.getElementById("player1-score");
	if (el) el.textContent = `Nivell: ${nivellIndex + 1} · Puntuació: ${score}`;
}

function limpiarBoard() {
	if (!gameboard) return;
	gameboard.replaceChildren();
}

function començarNivell(idx) {
	if (!gameboard) return;

	nivellIndex = idx;
	const { f, c } = getGridForLevel(nivellIndex);
	totalPars = (f * c) / 2;
	parsMatched = 0;

	limpiarBoard();
	setGraellaBoard(f, c);
	const fontSize = tamanyFontCarta(f, c);
	const baralla = buildDeckForLevel(nivellIndex, totalPars);

	baralla.forEach((value) => {
		const carta = document.createElement("div");
		carta.classList.add("card");
		carta.dataset.value = value;
		carta.style.fontSize = fontSize;
		carta.addEventListener("click", flipCard);
		gameboard.appendChild(carta);
	});

	actualitzarHud();
}

function alFinalitzar() {
	bloquejarBoard = true;
	score += 1;
	actualitzarHud();
	setTimeout(() => {
		bloquejarBoard = false;
		començarNivell(nivellIndex + 1);
	}, 650);
}

function flipCard() {
	// Aqui si el tablero esta block o fem doble click no fara res
	if (estat !== "running") return;
	if (bloquejarBoard) return;
	if (this === firstCard) return;

	//Li afegim clase del css
	this.classList.add("flipped");
	//Guardem a la variable les icones
	this.textContent = this.dataset.value;

	//Aqui comprovarem si la primera carta s'ha pegat la volta i quina
	if (!hasFlippedCard) {
		hasFlippedCard = true;
		firstCard = this;
		return;
	}
	// Una vegada a pegat la volta la primera li diem que la segona tmb
	secondCard = this;
	// I a esta funcio comprovarem si son iguals o no
	checkForMatch();
}

// Esta es la funcio anterior que comprovem
function checkForMatch() {
	//Aqui creem una variable que guarda un true o false. Si les dos cartes son iguals sera true
	// si no sera false
	let isMatch = firstCard.dataset.value === secondCard.dataset.value;
	//I aqui si isMatch es true, fara la funcio disableCards, si no fara l'altra
	if (isMatch) disableCards();
	else unflipCards();
}

//Esta funcio nomes se fara si les dos cartes son iguals
function disableCards() {
	firstCard.removeEventListener("click", flipCard);
	secondCard.removeEventListener("click", flipCard);
	firstCard.dataset.matched = true;
	secondCard.dataset.matched = true;
	parsMatched += 1;
	resetBoard();

	if (parsMatched >= totalPars) alFinalitzar();
}

//Esta funcio nomes se executa si son diferents
function unflipCards() {
	bloquejarBoard = true;
	//Dixem 1 segon pa que puguesem vore les cartes i despues li peguem la volta
	setTimeout(() => {
		//Borrem el css de quan estaven boca a dalt
		firstCard.classList.remove("flipped");
		secondCard.classList.remove("flipped");

		//Tornem a tindre un valor buit
		firstCard.textContent = "";
		secondCard.textContent = "";

		resetBoard();
	}, 1000);
}

//I esta funcio fa un reset del tablero tan com si es guanya o perd
function resetBoard() {
	hasFlippedCard = false;
	bloquejarBoard = false;
	firstCard = null;
	secondCard = null;
}

function iniciarJoc() {
	if (estat === "paused") {
		estat = "running";
		return;
	}
	if (estat === "running") return;

	estat = "running";
	nivellIndex = 0;
	score = 0;
	sessionStartTime = Date.now();
	teSessioGuardada = false;
	començarNivell(0);
}

function pausarJoc() {
	if (estat === "idle") return;
	if (estat === "paused") {
		estat = "running";
		return;
	}
	estat = "paused";
}

function finalitzarJoc() {
	if (estat === "idle") return;
	estat = "idle";
	bloquejarBoard = false;
	hasFlippedCard = false;
	firstCard = null;
	secondCard = null;

	guardarSessio();
	limpiarBoard();
	if (gameboard) {
		gameboard.style.display = "";
		gameboard.style.gridTemplateColumns = "";
		gameboard.style.gridTemplateRows = "";
	}
	const el = document.getElementById("player1-score");
	if (el) el.textContent = "La teua puntació:";
}

function guardarSessio() {
	if (teSessioGuardada || !sessionStartTime) return;

	teSessioGuardada = true;
	fetch("/api/sessions", {
		method: "POST",
		body: JSON.stringify({
			username: localStorage.getItem("username"),
			game_id: "memory",
			start_time: sessionStartTime,
			end_time: Date.now(),
			score: score,
		}),
		headers: { "Content-Type": "application/json" },
	})
		.then((response) => response.json())
		.then((data) => {
			if (!data.success)
				console.error(
					"No s'ha pogut guardar la sessió de Memory:",
					data.message,
				);
		})
		.catch((error) => {
			console.error("Error guardando sesión de Memory:", error);
			teSessioGuardada = false;
		});
}

function bindControls() {
	const startBtn = document.getElementById("start-game");
	const pauseBtn = document.getElementById("pause-game");
	const endBtn = document.getElementById("end-game");

	if (startBtn) startBtn.addEventListener("click", iniciarJoc);
	if (pauseBtn) pauseBtn.addEventListener("click", pausarJoc);
	if (endBtn) endBtn.addEventListener("click", finalitzarJoc);
}

if (gameboard) bindControls();
