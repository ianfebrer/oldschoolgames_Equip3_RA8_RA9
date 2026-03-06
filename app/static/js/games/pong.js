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
    x : 10,
    y : 0, // se actualizará en init
    width: playerWidth,
    height: playerHeight,
    velocityY : 0
}

// Player 2 object (right paddle)
let player2 = {
    x : 0, // se actualizará en init
    y : 0, // se actualizará en init
    width: playerWidth,
    height: playerHeight,
    velocityY : 0
}

// Ball object with position and velocity
let ball = {
    x : 0, // se actualizará en init
    y : 0, // se actualizará en init
    width: ballWidth,
    height: ballHeight,
    velocityX : ballSpeed,
    velocityY : ballSpeed
}

// ===============================
// SCORE VARIABLES
// ===============================

let player1Score = 0;
let player2Score = 0;

// ===============================
// INITIALIZATION
// ===============================

window.onload = function() {
    board = document.getElementById("board");
    context = board.getContext("2d"); 

    // inicializar tamaño y posiciones
    resizeCanvas();

    // dibujar paddle inicial
    context.fillStyle = "skyblue";
    context.fillRect(player1.x, player1.y, playerWidth, playerHeight);

    requestAnimationFrame(update);

    // controles
    board.addEventListener("mousemove", movePlayerWithMouse);
    document.addEventListener("keydown", keyDown);
    document.addEventListener("keyup", keyUp);

    // redimensionar al cambiar tamaño de ventana
    window.addEventListener("resize", resizeCanvas);
}

// ===============================
// RESIZE CANVAS
// ===============================

// Ajusta el canvas al tamaño del contenedor y recalcula posiciones
function resizeCanvas() {
    const container = board.parentElement;
    board.width = container.clientWidth;
    board.height = container.clientHeight;

    // posiciones iniciales responsive
    player1.x = 10;
    player1.y = board.height / 2 - playerHeight / 2;

    player2.x = board.width - playerWidth - 10;
    player2.y = board.height / 2 - playerHeight / 2;

    ball.x = board.width / 2 - ballWidth / 2;
    ball.y = board.height / 2 - ballHeight / 2;
}

// ===============================
// MAIN GAME LOOP
// ===============================

function update() {
    requestAnimationFrame(update);
    context.clearRect(0, 0, board.width, board.height);

    // player1
    context.fillStyle = "skyblue";
    let nextPlayer1Y = player1.y + player1.velocityY;
    if (!outOfBounds(nextPlayer1Y)) {
        player1.y = nextPlayer1Y;
    }
    context.fillRect(player1.x, player1.y, playerWidth, playerHeight);

    // player2
    context.fillStyle = "skyblue";
    let nextPlayer2Y = player2.y + player2.velocityY;
    if (!outOfBounds(nextPlayer2Y)) {
        player2.y = nextPlayer2Y;
    }
    context.fillRect(player2.x, player2.y, playerWidth, playerHeight);

    // ball
    context.fillStyle = "white";
    ball.x += ball.velocityX;
    ball.y += ball.velocityY;
    context.fillRect(ball.x, ball.y, ballWidth, ballHeight);

    if (ball.y <= 0 || (ball.y + ballHeight >= board.height)) { 
        ball.velocityY *= -1; 
    }

    // bounce
    if (detectCollision(ball, player1)) {
        if (ball.x <= player1.x + player1.width) {
            ball.velocityX *= -1;
        }
    }
    else if (detectCollision(ball, player2)) {
        if (ball.x + ballWidth >= player2.x) {
            ball.velocityX *= -1;
        }
    }

    // game over
    if (ball.x < 0) {
        player2Score++;
        resetGame(1);
    }
    else if (ball.x + ballWidth > board.width) {
        player1Score++;
        resetGame(-1);
    }

    // score
    context.font = "45px sans-serif";
    context.fillText(player1Score, board.width/5, 45);
    context.fillText(player2Score, board.width*4/5 - 45, 45);

    // dotted line
    for (let i = 10; i < board.height; i += 25) {
        context.fillRect(board.width / 2 - 10, i, 5, 5); 
    }
}

// ===============================
// HELPER FUNCTIONS
// ===============================

function outOfBounds(yPosition) {
    return (yPosition < 0 || yPosition + playerHeight > board.height);
}

function detectCollision(a, b) {
    return a.x < b.x + b.width &&
           a.x + a.width > b.x &&
           a.y < b.y + b.height &&
           a.y + a.height > b.y;
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
    let rect = board.getBoundingClientRect(); 
    let mouseY = e.clientY - rect.top;
    player1.y = mouseY - playerHeight / 2;

    if (player1.y < 0) player1.y = 0;
    if (player1.y + playerHeight > board.height) player1.y = board.height - playerHeight;
}

function keyDown(e) {
    if (e.code == "ArrowUp") player2.velocityY = -playerSpeed;
    else if (e.code == "ArrowDown") player2.velocityY = playerSpeed;
}

function keyUp(e) {
    if (e.code == "ArrowUp" || e.code == "ArrowDown") player2.velocityY = 0;
}
