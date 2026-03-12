class Trexpres {
	constructor() {
		this.canvas = document.getElementById("simulation-canvas");
		this.ctx = this.canvas.getContext("2d");
		this.cellSize = 80;
		this.boardOffset = { x: 50, y: 50 };

		this.phase = "idle";
		this.board = [];
		this.pieceToPlace = null;
		this.correctCell = { row: 0, col: 0 };
		this.phaseStartTime = 0;
		this.memorizeDuration = 500;
		this.score = 0;
		this.round = 0;
		this.startTime = null;

		this.puzzles = this.generatePuzzles();
	}

	generatePuzzles() {
		return [
			{
				board: [
					["X", "O", null],
					[null, "X", null],
					["O", "O", null],
				],
				piece: "X",
				win: [2, 2],
			},
			{
				board: [
					["X", "O", null],
					["X", null, null],
					[null, "O", null],
				],
				piece: "X",
				win: [2, 0],
			},
			{
				board: [
					[null, null, "X"],
					["O", "O", null],
					["X", null, null],
				],
				piece: "O",
				win: [1, 2],
			},
		];
	}

	start() {
		this.score = 0;
		this.round = 0;
		this.startTime = Date.now();
		this.nextRound();
	}

	nextRound() {
		this.round++;
		const p = this.puzzles[(this.round - 1) % this.puzzles.length];
		this.board = p.board.map((row) => [...row]);
		this.pieceToPlace = p.piece;
		this.correctCell = { row: p.win[0], col: p.win[1] };
		this.phase = "memorize";
		this.phaseStartTime = Date.now();
		this.gameLoop();
	}

	update() {
		if (
			this.phase === "memorize" &&
			Date.now() - this.phaseStartTime > this.memorizeDuration
		) {
			this.phase = "place";
			this.phaseStartTime = Date.now();
		}
	}

	handleClick(canvasX, canvasY) {
		if (this.phase !== "place") return;

		const col = Math.floor((canvasX - this.boardOffset.x) / this.cellSize);
		const row = Math.floor((canvasY - this.boardOffset.y) / this.cellSize);
		if (row < 0 || row > 2 || col < 0 || col > 2) return;

		const correct =
			row === this.correctCell.row && col === this.correctCell.col;
		const timeBonus = Math.max(0, 500 - (Date.now() - this.phaseStartTime));
		this.score += correct ? 100 + Math.floor(timeBonus / 100) : 0;

		if (correct) {
			this.phase = "result";
			setTimeout(() => this.nextRound(), 1000);
		} else {
			this.stop();
		}
	}

	stop() {
		this.phase = "idle";
		console.log("Game over! Score: " + this.score);
		fetch("/api/sessions", {
			method: "POST",
			body: JSON.stringify({
				username: localStorage.getItem("username"),
				game_id: "trexpres",
				start_time: this.startTime,
				end_time: Date.now(),
				score: this.score,
			}),
			headers: {
				"Content-Type": "application/json",
			},
		});
	}

	draw() {
		this.ctx.clearRect(0, 0, this.canvas.width, this.canvas.height);

		if (this.phase === "idle") return;

		const { x: ox, y: oy } = this.boardOffset;
		const size = this.cellSize;

		// grid de 3 per 3
		this.ctx.strokeStyle = "#666";
		this.ctx.lineWidth = 2;
		for (let i = 0; i <= 3; i++) {
			this.ctx.beginPath();
			this.ctx.moveTo(ox, oy + i * size);
			this.ctx.lineTo(ox + 3 * size, oy + i * size);
			this.ctx.stroke();

			this.ctx.beginPath();
			this.ctx.moveTo(ox + i * size, oy);
			this.ctx.lineTo(ox + i * size, oy + 3 * size);
			this.ctx.stroke();
		}

		// fase memorize: dibuixar peçes al grid
		if (this.phase === "memorize") {
			for (let r = 0; r < 3; r++) {
				for (let c = 0; c < 3; c++) {
					const piece = this.board[r][c];
					if (piece) {
						const cx = ox + c * size + size / 2;
						const cy = oy + r * size + size / 2;
						this.ctx.font = "bold 36px sans-serif";
						this.ctx.textAlign = "center";
						this.ctx.textBaseline = "middle";
						this.ctx.fillStyle =
							piece === "X" ? "#e74c3c" : "#3498db";
						this.ctx.fillText(piece, cx, cy);
					}
				}
			}
		}

		// fase place: dibuixar peça a la posició seleccionada
		if (this.phase === "place") {
			this.ctx.font = "bold 32px sans-serif";
			this.ctx.textAlign = "center";
			this.ctx.textBaseline = "middle";
			this.ctx.fillStyle =
				this.pieceToPlace === "X" ? "#e74c3c" : "#3498db";
			this.ctx.fillText(this.pieceToPlace, ox + 3 * size + 30, oy + 15);
		}

		// score y ronda
		this.ctx.fillStyle = "#fff";
		this.ctx.font = "16px monospace";
		this.ctx.textAlign = "left";
		this.ctx.textBaseline = "top";
		this.ctx.fillText(`Score: ${this.score}`, 10, 10);
		this.ctx.fillText(`Ronda: ${this.round}`, 10, 30);
	}

	gameLoop() {
		this.update();
		this.draw();
		if (this.phase !== "idle") {
			requestAnimationFrame(() => this.gameLoop());
		}
	}
}

document.addEventListener("DOMContentLoaded", () => {
	const game = new Trexpres();

	document
		.getElementById("start-simulation")
		.addEventListener("click", () => {
			game.start();
		});

	game.canvas.addEventListener("click", (e) => {
		const rect = game.canvas.getBoundingClientRect();
		const x = e.clientX - rect.left;
		const y = e.clientY - rect.top;
		game.handleClick(x, y);
	});
});
