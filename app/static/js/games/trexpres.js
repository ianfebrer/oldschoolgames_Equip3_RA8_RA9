// version muy simple estilo principiante

var canvas;
var ctx;

var cellSize = 80;
var boardX = 50;
var boardY = 50;

var phase = "idle";
var previousPhase = "idle";
var score = 0;
var round = 0;
var startTime = null;
var sessionSaved = false;
var memorizeTimer = null;

var board = [
	[null, null, null],
	[null, null, null],
	[null, null, null],
];

var pieceToPlace = "X";

var correctRow = 0;
var correctCol = 0;

var puzzles = [
	{
		board: [
			["X", "O", null],
			[null, "X", null],
			["O", "O", null],
		],
		piece: "X",
		winRow: 2,
		winCol: 2,
	},
	{
		board: [
			["X", "O", null],
			["X", null, null],
			[null, "O", null],
		],
		piece: "X",
		winRow: 2,
		winCol: 0,
	},
];

function startGame() {
	if (phase == "paused") {
		phase = previousPhase;
		draw();
		return;
	}

	if (phase != "idle") {
		return;
	}

	score = 0;
	round = 0;
	startTime = Date.now();
	sessionSaved = false;

	nextRound();
}

function nextRound() {
	round = round + 1;

	var index = (round - 1) % puzzles.length;
	var puzzle = puzzles[index];

	for (var r = 0; r < 3; r++) {
		for (var c = 0; c < 3; c++) {
			board[r][c] = puzzle.board[r][c];
		}
	}

	pieceToPlace = puzzle.piece;
	correctRow = puzzle.winRow;
	correctCol = puzzle.winCol;

	phase = "memorize";
	previousPhase = "memorize";

	draw();

	if (memorizeTimer) {
		clearTimeout(memorizeTimer);
	}

	memorizeTimer = setTimeout(function () {
		if (phase == "memorize") {
			phase = "place";
			previousPhase = "place";
			draw();
		}
	}, 900);
}

function draw() {
	if (!canvas || !ctx) {
		return;
	}

	ctx.clearRect(0, 0, canvas.width, canvas.height);

	if (phase == "idle") {
		drawHud();
		drawMessage("PRESIONA INICIAR");
		return;
	}

	drawGrid();

	if (phase == "memorize") {
		drawPieces();
	}

	if (phase == "place") {
		drawPieceHint();
	}

	if (phase == "paused") {
		if (previousPhase == "memorize") {
			drawPieces();
		} else if (previousPhase == "place") {
			drawPieceHint();
		}
		drawMessage("PAUSA");
	}

	drawHud();
}

function drawGrid() {
	ctx.strokeStyle = "#666";

	for (var i = 0; i <= 3; i++) {
		ctx.beginPath();
		ctx.moveTo(boardX, boardY + i * cellSize);
		ctx.lineTo(boardX + cellSize * 3, boardY + i * cellSize);
		ctx.stroke();

		ctx.beginPath();
		ctx.moveTo(boardX + i * cellSize, boardY);
		ctx.lineTo(boardX + i * cellSize, boardY + cellSize * 3);
		ctx.stroke();
	}
}

function drawPieces() {
	ctx.font = "36px sans-serif";
	ctx.textAlign = "center";
	ctx.textBaseline = "middle";

	for (var r = 0; r < 3; r++) {
		for (var c = 0; c < 3; c++) {
			var piece = board[r][c];

			if (piece != null) {
				var x = boardX + c * cellSize + cellSize / 2;
				var y = boardY + r * cellSize + cellSize / 2;

				ctx.fillText(piece, x, y);
			}
		}
	}
}

function drawHud() {
	ctx.fillStyle = "white";
	ctx.font = "16px monospace";

	ctx.fillText("Score: " + score, 10, 20);
	ctx.fillText("Round: " + round, 10, 40);
}

function drawPieceHint() {
	ctx.fillStyle = "#00F0FF";
	ctx.font = "bold 28px sans-serif";
	ctx.textAlign = "left";
	ctx.textBaseline = "top";
	ctx.fillText("Pieza: " + pieceToPlace, boardX + cellSize * 3 + 15, boardY);
}

function drawMessage(text) {
	ctx.fillStyle = "rgba(0,0,0,0.65)";
	ctx.fillRect(0, canvas.height / 2 - 35, canvas.width, 70);
	ctx.fillStyle = "#CCFF00";
	ctx.font = "bold 28px sans-serif";
	ctx.textAlign = "center";
	ctx.textBaseline = "middle";
	ctx.fillText(text, canvas.width / 2, canvas.height / 2);
}

function pauseGame() {
	if (phase == "idle") {
		return;
	}

	if (phase == "paused") {
		phase = previousPhase;
		draw();
		return;
	}

	previousPhase = phase;
	phase = "paused";
	draw();
}

function handleClick(x, y) {
	if (phase != "place") {
		return;
	}

	var col = Math.floor((x - boardX) / cellSize);
	var row = Math.floor((y - boardY) / cellSize);

	if (row == correctRow && col == correctCol) {
		score++;
		nextRound();
	} else {
		endGame();
	}
}

function endGame() {
	if (memorizeTimer) {
		clearTimeout(memorizeTimer);
		memorizeTimer = null;
	}

	phase = "idle";

	console.log("Game over. Score: " + score);
	saveSession();
	draw();
}

function saveSession() {
	if (sessionSaved || !startTime) {
		return;
	}

	sessionSaved = true;

	fetch("/api/sessions", {
		method: "POST",
		headers: {
			"Content-Type": "application/json",
		},
		body: JSON.stringify({
			username: localStorage.getItem("username"),
			game_id: "trexpres",
			start_time: startTime,
			end_time: Date.now(),
			score: score,
		}),
	}).catch(function () {
		sessionSaved = false;
	});
}

function resizeCanvas() {
	if (!canvas) {
		return;
	}

	var container = canvas.parentElement;
	canvas.width = container.clientWidth;
	canvas.height = container.clientHeight;

	boardX = Math.max(20, Math.floor((canvas.width - cellSize * 3) / 2));
	boardY = Math.max(70, Math.floor((canvas.height - cellSize * 3) / 2));

	draw();
}

document.addEventListener("DOMContentLoaded", function () {
	canvas = document.getElementById("board");
	if (!canvas) {
		return;
	}
	ctx = canvas.getContext("2d");

	resizeCanvas();
	window.addEventListener("resize", resizeCanvas);

	var startBtn = document.getElementById("start-game");
	var pauseBtn = document.getElementById("pause-game");
	var endBtn = document.getElementById("end-game");

	startBtn.addEventListener("click", function () {
		startGame();
	});
	pauseBtn.addEventListener("click", function () {
		pauseGame();
	});
	endBtn.addEventListener("click", function () {
		endGame();
	});

	canvas.addEventListener("click", function (e) {
		var rect = canvas.getBoundingClientRect();

		var x = e.clientX - rect.left;
		var y = e.clientY - rect.top;

		handleClick(x, y);
	});

	draw();
});
