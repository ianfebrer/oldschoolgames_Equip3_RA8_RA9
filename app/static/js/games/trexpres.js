class Trexpres {
	constructor() {
		this.canvas = document.getElementById("simulation-canvas");
		this.ctx = this.canvas.getContext("2d");

		this.player = {
			x: 50,
			y: 200,
			width: 30,
			height: 30,
			vy: 0,
			onGround: true,
		};

		this.groundY = 250;

		this.playing = false;
		this.score = 0;
		this.startTime = null;

		this.obstacles = [];
		this.obstacleSpeed = 5;
		this.spawnCounter = 0;
	}

	jump() {
		if (this.player.onGround && this.playing) {
			this.player.vy = -12;
			this.player.onGround = false;
		}
	}

	update() {
		if (!this.playing) return;

		this.player.vy += 0.8;
		this.player.y += this.player.vy;

		// si el jugador ha arribat o passat el nivell del terra, el col·loquem anterra i parem la caiguda
		if (this.player.y >= this.groundY - this.player.height) {
			this.player.y = this.groundY - this.player.height;
			this.player.vy = 0;
			this.player.onGround = true;
		}

		this.spawnCounter++;
		if (this.spawnCounter > 80) {
			this.spawnCounter = 0;
			this.obstacles.push({
				x: this.canvas.width,
				y: this.groundY - 30,
				width: 20,
				height: 40,
			});
		}

		for (let i = this.obstacles.length - 1; i >= 0; i--) {
			this.obstacles[i].x -= this.obstacleSpeed;
			if (this.obstacles[i].x + this.obstacles[i].width < 0) {
				this.obstacles.splice(i, 1);
			}
		}

		for (const obs of this.obstacles) {
			if (this.collides(this.player, obs)) {
				this.stop();
				return;
			}
		}
		this.score = Math.floor((Date.now() - this.startTime) / 500);
	}

	collides(a, b) {
		return (
			a.x < b.x + b.width &&
			a.x + a.width > b.x &&
			a.y < b.y + b.height &&
			a.y + a.height > b.y
		);
	}

	draw() {
		this.ctx.clearRect(0, 0, this.canvas.width, this.canvas.height);

		this.ctx.fillStyle = "#333";
		this.ctx.fillRect(
			0,
			this.groundY,
			this.canvas.width,
			this.canvas.height - this.groundY,
		);

		this.ctx.fillStyle = "#ff4444";
		for (const obs of this.obstacles) {
			this.ctx.fillRect(obs.x, obs.y, obs.width, obs.height);
		}

		this.ctx.fillStyle = "#33ff33";
		this.ctx.fillRect(
			this.player.x,
			this.player.y,
			this.player.width,
			this.player.height,
		);

		const elapsedMs = this.startTime ? Date.now() - this.startTime : 0;
		const seconds = Math.floor(elapsedMs / 1000) % 60;
		const minutes = Math.floor(elapsedMs / 60000);
		const timeString = `${minutes.toString().padStart(2, "0")}:${seconds.toString().padStart(2, "0")}`;

		this.ctx.fillStyle = "#00000";
		this.ctx.font = "20px monospace";
		this.ctx.fillText("Score: " + this.score, 10, 30);
		this.ctx.fillText("Time: " + timeString, 10, 55);
	}

	gameLoop() {
		this.update();
		this.draw();
		if (this.playing) {
			requestAnimationFrame(() => this.gameLoop());
		}
	}

	start() {
		this.playing = true;
		this.startTime = Date.now();
		this.gameLoop();
	}

	stop() {
		this.playing = false;
		console.log("Game over! Score: " + this.score);
		fetch("/games/api/sessions", {
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
}

document.addEventListener("DOMContentLoaded", () => {
	const game = new Trexpres();

	document
		.getElementById("start-simulation")
		.addEventListener("click", () => {
			game.start();
		});

	document.addEventListener("keydown", (event) => {
		if (event.code === "Space") {
			event.preventDefault();
			game.jump();
		}
	});

	document.addEventListener("click", () => game.jump());
});
