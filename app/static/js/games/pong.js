// ===============================
// BOARD CONFIGURATION
// ===============================

let board;
let context;

// ===============================
// PLAYER CONFIGURATION
// ===============================

let playerWidth = 10;
let playerHeight = 50;
let playerSpeed = 6;

// ===============================
// BALL CONFIGURATION
// ===============================

let ballSpeed = 4;
let ballWidth = 10;
let ballHeight = 10;

// ===============================
// GAME OBJECTS
// ===============================

// Player 1 object (left paddle)
let player1 = {
	x: 10,
	y: 0, // se actualizará en init
	width: playerWidth,
	height: playerHeight,
	velocityY: 0,
};

// Player 2 object (right paddle)
let player2 = {
	x: 0, // se actualizará en init
	y: 0, // se actualizará en init
	width: playerWidth,
	height: playerHeight,
	velocityY: 0,
};

// Ball object with position and velocity
let ball = {
	x: 0, // se actualizará en init
	y: 0, // se actualizará en init
	width: ballWidth,
	height: ballHeight,
	velocityX: ballSpeed,
	velocityY: ballSpeed,
};

// ===============================
// SCORE VARIABLES
// ===============================

let player1Score = 0;
let player2Score = 0;
let gameState = "idle"; // idle | running | paused | finished
let sessionStartTime = null;
let hasSavedSession = false;
let elapsedTimeMs = 0;
let lastTimerTick = null;
let lastRenderedSeconds = -1;

// ===============================
// INITIALIZATION
// ===============================

window.onload = function () {
	board = document.getElementById("board");
	context = board.getContext("2d");

	// inicializar tamaño y posiciones
	resizeCanvas();
	bindControlButtons();
	document.getElementById("player1-score").textContent =
		`La teua puntuació: ${player1Score}`;
	updateTimerDisplay(true);
	drawFrame();

	requestAnimationFrame(update);

	// controles
	board.addEventListener("mousemove", movePlayerWithMouse);
	document.addEventListener("keydown", keyDown);
	document.addEventListener("keyup", keyUp);

	// redimensionar al cambiar tamaño de ventana
	window.addEventListener("resize", resizeCanvas);
};

// ===============================
// RESIZE CANVAS
// ===============================

// Ajusta el canvas al tamaño del contenedor y recalcula posiciones
function resizeCanvas() {
	const container = board.parentElement;
	board.width = container.clientWidth;
	board.height = container.clientHeight;

	// posiciones iniciales responsive
	resetPlayersPosition();

	ball.x = board.width / 2 - ballWidth / 2;
	ball.y = board.height / 2 - ballHeight / 2;
}

function bindControlButtons() {
	const startButton = document.getElementById("start-game");
	const pauseButton = document.getElementById("pause-game");
	const endButton = document.getElementById("end-game");

	if (startButton) startButton.addEventListener("click", startGame);
	if (pauseButton) pauseButton.addEventListener("click", pauseGame);
	if (endButton) endButton.addEventListener("click", endGame);
}

function startGame() {
	if (gameState === "running") return;

	if (gameState === "idle" || gameState === "finished") {
		player1Score = 0;
		player2Score = 0;
		sessionStartTime = Date.now();
		hasSavedSession = false;
		elapsedTimeMs = 0;
		lastRenderedSeconds = -1;
		updateTimerDisplay(true);
		resetPlayersPosition();
		resetGame(Math.random() > 0.5 ? 1 : -1);
	}
	document.getElementById("player1-score").textContent =
		`La teua puntuació: ${player1Score}`;

	lastTimerTick = Date.now();
	gameState = "running";
}

function pauseGame() {
	if (gameState !== "running") return;
	advanceTimer();
	lastTimerTick = null;
	gameState = "paused";
	player1.velocityY = 0;
	player2.velocityY = 0;
}

function endGame() {
	if (gameState === "idle") return;
	if (gameState === "running") {
		advanceTimer();
	}
	saveSessionData();
	gameState = "idle";
	player1.velocityY = 0;
	player2.velocityY = 0;
	player1Score = 0;
	player2Score = 0;
	lastTimerTick = null;
	resetPlayersPosition();
	resetGame(Math.random() > 0.5 ? 1 : -1);
	document.getElementById("player1-score").textContent =
		"La teua puntuació: 0";
	elapsedTimeMs = 0;
	lastRenderedSeconds = -1;
	updateTimerDisplay(true);
}

function saveSessionData() {
	if (hasSavedSession || !sessionStartTime) return;

	hasSavedSession = true;
	fetch("/api/sessions", {
		method: "POST",
		body: JSON.stringify({
			username: localStorage.getItem("username"),
			game_id: "pong",
			start_time: sessionStartTime,
			end_time: Date.now(),
			score: player1Score,
			duration_ms: elapsedTimeMs,
		}),
		headers: {
			"Content-Type": "application/json",
		},
	})
		.then((response) => response.json())
		.then((data) => {
			if (!data.success) {
				console.error(
					"No se pudo guardar la sesion de Pong:",
					data.message,
				);
			}
		})
		.catch((error) => {
			console.error("Error guardando sesion de Pong:", error);
			hasSavedSession = false;
		});
}

// ===============================
// MAIN GAME LOOP
// ===============================

function update() {
	requestAnimationFrame(update);
	context.clearRect(0, 0, board.width, board.height);

	if (gameState === "running") {
		advanceTimer();
		let nextPlayer1Y = player1.y + player1.velocityY;
		if (!outOfBounds(nextPlayer1Y)) {
			player1.y = nextPlayer1Y;
		}

		let nextPlayer2Y = player2.y + player2.velocityY;
		if (!outOfBounds(nextPlayer2Y)) {
			player2.y = nextPlayer2Y;
		}

		ball.x += ball.velocityX;
		ball.y += ball.velocityY;

		if (ball.y <= 0 || ball.y + ballHeight >= board.height) {
			ball.velocityY *= -1;
		}

		// bounce
		if (detectCollision(ball, player1)) {
			if (ball.x <= player1.x + player1.width) {
				ball.velocityX *= -1;
			}
		} else if (detectCollision(ball, player2)) {
			if (ball.x + ballWidth >= player2.x) {
				ball.velocityX *= -1;
			}
		}

		// score
		if (ball.x < 0) {
			player2Score++;
			resetGame(1);
		} else if (ball.x + ballWidth > board.width) {
			player1Score++;
			document.getElementById("player1-score").textContent =
				`La teua puntuació: ${player1Score}`;
			resetGame(-1);
		}
	}

	drawFrame();
}

function advanceTimer() {
	if (lastTimerTick === null) return;
	const now = Date.now();
	elapsedTimeMs += now - lastTimerTick;
	lastTimerTick = now;
	updateTimerDisplay();
}

function updateTimerDisplay(force = false) {
	const timerElement = document.getElementById("game-timer");
	if (!timerElement) return;

	const totalSeconds = Math.floor(elapsedTimeMs / 1000);
	if (!force && totalSeconds === lastRenderedSeconds) return;

	lastRenderedSeconds = totalSeconds;
	const minutes = String(Math.floor(totalSeconds / 60)).padStart(2, "0");
	const seconds = String(totalSeconds % 60).padStart(2, "0");
	timerElement.textContent = `Temps de partida: ${minutes}:${seconds}`;
}

function drawFrame() {
	context.fillStyle = "skyblue";
	context.fillRect(player1.x, player1.y, playerWidth, playerHeight);
	context.fillRect(player2.x, player2.y, playerWidth, playerHeight);

	context.fillStyle = "white";
	context.fillRect(ball.x, ball.y, ballWidth, ballHeight);

	context.font = "45px sans-serif";
	context.fillText(player1Score, board.width / 5, 45);
	context.fillText(player2Score, (board.width * 4) / 5 - 45, 45);

	for (let i = 10; i < board.height; i += 25) {
		context.fillRect(board.width / 2 - 10, i, 5, 5);
	}

	if (gameState === "idle") {
		drawCenterMessage("PRESIONA INICIAR");
	} else if (gameState === "paused") {
		drawCenterMessage("PAUSA");
	} else if (gameState === "finished") {
		drawCenterMessage("PARTIDA FINALIZADA");
	}
}

function drawCenterMessage(message) {
	context.fillStyle = "rgba(0, 0, 0, 0.6)";
	context.fillRect(0, board.height / 2 - 40, board.width, 80);
	context.fillStyle = "#CCFF00";
	context.font = "28px sans-serif";
	context.textAlign = "center";
	context.fillText(message, board.width / 2, board.height / 2 + 10);
	context.textAlign = "start";
}

// ===============================
// HELPER FUNCTIONS
// ===============================

function outOfBounds(yPosition) {
	return yPosition < 0 || yPosition + playerHeight > board.height;
}

function detectCollision(a, b) {
	return (
		a.x < b.x + b.width &&
		a.x + a.width > b.x &&
		a.y < b.y + b.height &&
		a.y + a.height > b.y
	);
}

function resetPlayersPosition() {
	player1.x = 10;
	player1.y = board.height / 2 - playerHeight / 2;
	player2.x = board.width - playerWidth - 10;
	player2.y = board.height / 2 - playerHeight / 2;
}

function resetGame(direction) {
	ball.x = board.width / 2 - ballWidth / 2;
	ball.y = board.height / 2 - ballHeight / 2;
	ball.velocityX = ballSpeed * direction;
	ball.velocityY = ballSpeed;
}

// ===============================
// INPUT CONTROLS
// ===============================

function movePlayerWithMouse(e) {
	if (gameState !== "running") return;

	let rect = board.getBoundingClientRect();
	let mouseY = e.clientY - rect.top;
	player1.y = mouseY - playerHeight / 2;

	if (player1.y < 0) player1.y = 0;
	if (player1.y + playerHeight > board.height)
		player1.y = board.height - playerHeight;
}

function keyDown(e) {
	if (gameState !== "running") return;

	if (e.code == "ArrowUp") player2.velocityY = -playerSpeed;
	else if (e.code == "ArrowDown") player2.velocityY = playerSpeed;
}

function keyUp(e) {
	if (e.code == "ArrowUp" || e.code == "ArrowDown") player2.velocityY = 0;
}
