const icon = ['🍎', '🍌', '🍇', '🍓', '🍒', '🍍', '🥝', '🍋'];
const gameboard = document.getElementById('board');

//Esta funcio el que fa es barrejar la llista "cards", creant una variable "j" que amb
// que amb el metode Math.random barreje les cartes, i despues fem un intercambi de posicio entre
// "i" i la "j"
function barrejar(llista) {
    for (let i = llista.length - 1; i > 0; --i) {
        const j = Math.floor(Math.random() * (i + 1));
        [llista[i], llista[j]] = [llista[j], llista[i]];
    }
}

function initGame() {
    gameboard.innerHTML = '';
    let cards = icon.concat(icon);
    barrejar(cards);

    cards.forEach(iconVal => {
        const card = document.createElement('div');
        card.classList.add('card');
        card.dataset.value = iconVal;
        card.addEventListener('click', flipCard);
        gameboard.appendChild(card);
    });

    score = 0;
    updateScore();
}

function bindControls() {
    const startButton = document.getElementById("start-game");
    const pauseButton = document.getElementById("pause-game");
    const endButton = document.getElementById("end-game");

    if (startButton) startButton.addEventListener("click", startGame);
    if (pauseButton) pauseButton.addEventListener("click", pauseGame);
    if (endButton) endButton.addEventListener("click", endGame);
}

function startGame() {
    if (gameState === "running") return;

    // Si estem aturats o al final, inicialitzem cartes
    if (gameState === "idle" || gameState === "finished") {
        initGame();
        [hasFlippedCard, lockBoard] = [false, false];
        [firstCard, secondCard] = [null, null];
    } else if (gameState === "paused") {
        // En reiniciar des de pausa, només desbloquegem targetes
        lockBoard = false;
    }

    gameState = "running";
}

function pauseGame() {
    if (gameState !== "running") return;
    gameState = "paused";
    lockBoard = true; // Bloquegem el taulell
}

function endGame() {
    if (gameState === "idle") return;
    gameState = "finished";
    lockBoard = true;
    gameboard.innerHTML = "";
    score = 0;
    updateScore();
}

function updateScore() {
    const scoreElement = document.getElementById("player1-score");
    if (scoreElement) {
        scoreElement.textContent = "La teua puntuació: " + score;
    }
}

function flipCard() {
    if (lockBoard) return;
    if (this === firstCard) return;

    this.classList.add('flipped');
    this.textContent = this.dataset.value;

    if (!hasFlippedCard) {
        hasFlippedCard = true;
        firstCard = this;
        return;
    }

    secondCard = this;
    checkForMatch();
}

function checkForMatch() {
    let isMatch = firstCard.dataset.value === secondCard.dataset.value;
    if (isMatch) {
        score += 10;
        updateScore();
        disableCards();
    } else {
        unflipCards();
    }
}

function disableCards() {
    firstCard.removeEventListener('click', flipCard);
    secondCard.removeEventListener('click', flipCard);
    resetBoard();
}

function unflipCards() {
    lockBoard = true;
    setTimeout(() => {
        firstCard.classList.remove('flipped');
        secondCard.classList.remove('flipped');
        firstCard.textContent = '';
        secondCard.textContent = '';
        resetBoard();
    }, 1000);
}

function resetBoard() {
    // Si estem en pausa, assegurem que el taulell segueixi bloquejat després d'amagar la carta incorrecta
    [hasFlippedCard, lockBoard] = [false, gameState !== "running"];
    [firstCard, secondCard] = [null, null];
}

bindControls();