"use strict";
class App {
    // Estado del juego
    cardsArray = [
        { id: 1, content: 'Ikigai', pairId: 1 },
        { id: 2, content: 'Propósito de vida', pairId: 1 },
        { id: 3, content: 'Kaizen', pairId: 2 },
        { id: 4, content: 'Mejora continua', pairId: 2 },
        { id: 5, content: 'Wa', pairId: 3 },
        { id: 6, content: 'Armonía social', pairId: 3 },
        { id: 7, content: 'Familia', pairId: 4 },
        { id: 8, content: 'Apoyo mutuo', pairId: 4 },
        { id: 9, content: 'Resiliencia', pairId: 5 },
        { id: 10, content: 'Echarle ganas', pairId: 5 },
        { id: 11, content: 'Tiempo Flexible', pairId: 6 },
        { id: 12, content: 'Vivir el presente', pairId: 6 },
    ];
    hasFlippedCard = false;
    lockBoard = false;
    firstCard = null;
    secondCard = null;
    attempts = 0;
    matchedPairs = 0;
    constructor() {
        this.initGame();
    }
    // --- NAVEGACIÓN ---
    showAuthorScreen() {
        document.getElementById('screen-main')?.classList.remove('active');
        document.getElementById('screen-author')?.classList.add('active');
    }
    showMainScreen() {
        document.getElementById('screen-author')?.classList.remove('active');
        document.getElementById('screen-main')?.classList.add('active');
    }
    // --- LÓGICA DEL MEMORAMA ---
    initGame() {
        const grid = document.getElementById('memory-game');
        if (!grid)
            return;
        grid.innerHTML = ''; // Limpiar tablero
        this.resetVariables();
        // Actualizar UI de intentos
        const attemptsEl = document.getElementById('attempts');
        if (attemptsEl)
            attemptsEl.innerText = this.attempts.toString();
        // Mezclar cartas aleatoriamente
        const shuffledCards = [...this.cardsArray].sort(() => 0.5 - Math.random());
        // Crear elementos HTML para cada carta
        shuffledCards.forEach(cardData => {
            const cardElement = document.createElement('div');
            cardElement.classList.add('memory-card');
            cardElement.dataset.pairId = cardData.pairId.toString();
            const front = document.createElement('div');
            front.classList.add('card-front');
            const back = document.createElement('div');
            back.classList.add('card-back');
            back.innerText = cardData.content;
            cardElement.appendChild(front);
            cardElement.appendChild(back);
            // Escuchar el click
            cardElement.addEventListener('click', () => this.flipCard(cardElement));
            grid.appendChild(cardElement);
        });
    }
    flipCard(card) {
        if (this.lockBoard)
            return;
        if (card === this.firstCard)
            return; // Evitar doble click en la misma carta
        card.classList.add('flip');
        if (!this.hasFlippedCard) {
            // Es la primera carta que se voltea
            this.hasFlippedCard = true;
            this.firstCard = card;
            return;
        }
        // Es la segunda carta
        this.secondCard = card;
        this.attempts++;
        const attemptsEl = document.getElementById('attempts');
        if (attemptsEl)
            attemptsEl.innerText = this.attempts.toString();
        this.checkForMatch();
    }
    checkForMatch() {
        if (!this.firstCard || !this.secondCard)
            return;
        const isMatch = this.firstCard.dataset.pairId === this.secondCard.dataset.pairId;
        isMatch ? this.disableCards() : this.unflipCards();
    }
    disableCards() {
        // Son pareja, se quedan volteadas y quitamos el evento click
        this.firstCard?.removeEventListener('click', this.flipCard);
        this.secondCard?.removeEventListener('click', this.flipCard);
        this.matchedPairs++;
        this.resetBoard();
        // Comprobar si ganó
        if (this.matchedPairs === this.cardsArray.length / 2) {
            setTimeout(() => {
                alert(`¡Felicidades! Completaste el memorama en ${this.attempts} intentos.`);
            }, 500);
        }
    }
    unflipCards() {
        // No son pareja, las volteamos de nuevo después de un breve tiempo
        this.lockBoard = true;
        setTimeout(() => {
            this.firstCard?.classList.remove('flip');
            this.secondCard?.classList.remove('flip');
            this.resetBoard();
        }, 1200);
    }
    resetBoard() {
        this.hasFlippedCard = false;
        this.lockBoard = false;
        this.firstCard = null;
        this.secondCard = null;
    }
    resetVariables() {
        this.attempts = 0;
        this.matchedPairs = 0;
        this.resetBoard();
    }
    // Método público para el botón del HTML
    resetGame() {
        this.initGame();
    }
}
// Inicializar la aplicación y exponerla globalmente para que el HTML pueda llamar a sus métodos (onclick)
const app = new App();
window.app = app;
