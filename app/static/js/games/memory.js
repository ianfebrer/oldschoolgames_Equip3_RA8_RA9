const icon = ['🍎', '🍌', '🍇', '🍓', '🍒', '🍍', '🥝', '🍋'];
//Esta variable el que fa es dublicar la varibale de dalt per a que siguen 16 cartes
let cards = icon.concat(icon);
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
barrejar(cards);


cards.forEach(icon => {
    // Creem una variable que el que fa es crear els div al html
    const card = document.createElement('div');

    // Afegirem la variable card a la clase card del CSS, per a que agafo els estils
    card.classList.add('card');

    // Aqui li guardem cada element de la llista a la carta.
    card.dataset.value = icon;

    //Esta funcio el que fara es donarli la volta a la carta quan fesem click
    card.addEventListener('click', flipCard);

    // Aqui afegirem la variable card dins del tablero que hem creat al html.
    gameboard.appendChild(card);
});

//Crearem estes variables que ens ajudaran a fer la següent funcio.
let hasFlippedCard = false;
let lockBoard = false;
let firstCard, secondCard;


function flipCard() {
    // Aqui si el tablero esta block o fem doble click no fara res
    if (lockBoard) return;
    if (this === firstCard) return;

    //Li afegim clase del css
    this.classList.add('flipped');
    //Guardem a la variable les icones
    this.textContent = this.dataset.value

    //Aqui comprovarem si la primera carta s'ha pegat la volta i quina
    if (!hasFlippedCard) {
        hasFlippedCard = true
        firstCard = this
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
    isMatch ? disableCards() : unflipCards();

}

//Esta funcio nomes se fara si les dos cartes son iguals
function disableCards() {
    //Li borrem el css de quan estaven boca avall
    firstCard.removeEventListener('click', flipCard);
    secondCard.removeEventListener('click', flipCard);
    //I fem un reset del tablero en esta funcio
    resetBoard();
}

//Esta funcio nomes se executa si son diferents
function unflipCards() {
    lockBoard = true;
    //Dixem 1 segon pa que puguesem vore les cartes i despues li peguem la volta
    setTimeout(() => {
        //Borrem el css de quan estaven boca a dalt
        firstCard.classList.remove('flipped');
        secondCard.classList.remove('flipped');

        //Tornem a tindre un valor buit
        firstCard.textContent = '';
        secondCard.textContent = '';

        resetBoard();
    }, 1000);
}

//I esta funcio fa un reset del tablero tan com si es guanya o perd
function resetBoard() {
    [hasFlippedCard, lockBoard] = [false, false];
    [firstCard, secondCard] = [null, null];
}