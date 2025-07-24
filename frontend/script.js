class Game {
    constructor() {
        this.currentGame = 'chess'; // 'chess' or 'checkers'
        this.gameMode = 'ai'; // 'ai' or 'player'
        this.difficulty = 2;
        this.currentPlayer = 'white';
        this.selectedSquare = null;
        this.possibleMoves = [];
        this.board = null;
        this.gameState = 'playing'; // 'playing', 'check', 'checkmate', 'stalemate', 'draw'
        this.moveHistory = [];
        this.scores = { white: 0, black: 0 };
        
        // API base URL
        this.apiUrl = 'http://localhost:5000';
        
        this.initializeEventListeners();
        this.initializeGame();
    }

    initializeEventListeners() {
        // Game selection buttons
        document.getElementById('chess-btn').addEventListener('click', () => this.switchGame('chess'));
        document.getElementById('checkers-btn').addEventListener('click', () => this.switchGame('checkers'));
        
        // Game controls
        document.getElementById('game-mode').addEventListener('change', (e) => {
            this.gameMode = e.target.value;
            this.updateDifficultyVisibility();
            this.newGame();
        });
        
        document.getElementById('difficulty').addEventListener('change', (e) => {
            this.difficulty = parseInt(e.target.value);
        });
        
        document.getElementById('new-game-btn').addEventListener('click', () => this.newGame());
        document.getElementById('reset-btn').addEventListener('click', () => this.resetGame());
    }

    switchGame(game) {
        this.currentGame = game;
        
        // Update button states
        document.querySelectorAll('.game-btn').forEach(btn => btn.classList.remove('active'));
        document.getElementById(`${game}-btn`).classList.add('active');
        
        // Update board class
        const board = document.getElementById('game-board');
        board.className = `${game}-board`;
        
        this.newGame();
    }

    updateDifficultyVisibility() {
        const difficultyContainer = document.getElementById('difficulty-container');
        difficultyContainer.style.display = this.gameMode === 'ai' ? 'block' : 'none';
    }

    async newGame() {
        this.currentPlayer = 'white';
        this.selectedSquare = null;
        this.possibleMoves = [];
        this.gameState = 'playing';
        this.moveHistory = [];
        
        try {
            const response = await fetch(`${this.apiUrl}/new_game`, {
                method: 'POST',
                headers: { 'Content-Type': 'application/json' },
                body: JSON.stringify({
                    game_type: this.currentGame,
                    mode: this.gameMode,
                    difficulty: this.difficulty
                })
            });
            
            const data = await response.json();
            this.board = data.board;
            this.createBoard();
            this.updateUI();
        } catch (error) {
            console.error('Error starting new game:', error);
            // Fallback to local initialization
            this.initializeLocalBoard();
        }
    }

    resetGame() {
        this.scores = { white: 0, black: 0 };
        this.updateScoreBoard();
        this.newGame();
    }

    initializeLocalBoard() {
        if (this.currentGame === 'chess') {
            this.board = this.getInitialChessBoard();
        } else {
            this.board = this.getInitialCheckersBoard();
        }
        this.createBoard();
        this.updateUI();
    }

    getInitialChessBoard() {
        return [
            ['r', 'n', 'b', 'q', 'k', 'b', 'n', 'r'],
            ['p', 'p', 'p', 'p', 'p', 'p', 'p', 'p'],
            [null, null, null, null, null, null, null, null],
            [null, null, null, null, null, null, null, null],
            [null, null, null, null, null, null, null, null],
            [null, null, null, null, null, null, null, null],
            ['P', 'P', 'P', 'P', 'P', 'P', 'P', 'P'],
            ['R', 'N', 'B', 'Q', 'K', 'B', 'N', 'R']
        ];
    }

    getInitialCheckersBoard() {
        const board = Array(8).fill(null).map(() => Array(8).fill(null));
        
        // Place black pieces
        for (let row = 0; row < 3; row++) {
            for (let col = 0; col < 8; col++) {
                if ((row + col) % 2 === 1) {
                    board[row][col] = 'b';
                }
            }
        }
        
        // Place white pieces
        for (let row = 5; row < 8; row++) {
            for (let col = 0; col < 8; col++) {
                if ((row + col) % 2 === 1) {
                    board[row][col] = 'w';
                }
            }
        }
        
        return board;
    }

    createBoard() {
        const boardElement = document.getElementById('game-board');
        boardElement.innerHTML = '';
        
        for (let row = 0; row < 8; row++) {
            for (let col = 0; col < 8; col++) {
                const square = document.createElement('div');
                square.className = `square ${(row + col) % 2 === 0 ? 'white' : 'black'}`;
                square.dataset.row = row;
                square.dataset.col = col;
                
                const piece = this.board[row][col];
                if (piece) {
                    const pieceElement = this.createPieceElement(piece);
                    square.appendChild(pieceElement);
                }
                
                square.addEventListener('click', () => this.handleSquareClick(row, col));
                boardElement.appendChild(square);
            }
        }
    }

    createPieceElement(piece) {
        if (this.currentGame === 'chess') {
            return this.createChessPiece(piece);
        } else {
            return this.createCheckerPiece(piece);
        }
    }

    createChessPiece(piece) {
        const pieceElement = document.createElement('div');
        pieceElement.className = `piece ${piece === piece.toUpperCase() ? 'white' : 'black'}`;
        
        const pieceSymbols = {
            'k': '♚', 'K': '♔',
            'q': '♛', 'Q': '♕',
            'r': '♜', 'R': '♖',
            'b': '♝', 'B': '♗',
            'n': '♞', 'N': '♘',
            'p': '♟', 'P': '♙'
        };
        
        pieceElement.textContent = pieceSymbols[piece] || piece;
        return pieceElement;
    }

    createCheckerPiece(piece) {
        const pieceElement = document.createElement('div');
        const isKing = piece.toUpperCase() === piece && piece !== piece.toLowerCase();
        const color = (piece.toLowerCase() === 'w') ? 'white' : 'black';
        
        pieceElement.className = `checker ${color} ${isKing ? 'king' : ''}`;
        return pieceElement;
    }

    async handleSquareClick(row, col) {
        if (this.gameState !== 'playing' || (this.gameMode === 'ai' && this.currentPlayer === 'black')) {
            return;
        }

        const clickedPiece = this.board[row][col];
        
        // If no piece is selected
        if (!this.selectedSquare) {
            if (clickedPiece && this.isPieceOwnedByCurrentPlayer(clickedPiece)) {
                this.selectSquare(row, col);
                await this.showPossibleMoves(row, col);
            }
            return;
        }

        // If clicking the same square, deselect
        if (this.selectedSquare.row === row && this.selectedSquare.col === col) {
            this.deselectSquare();
            return;
        }

        // If clicking another own piece, select it instead
        if (clickedPiece && this.isPieceOwnedByCurrentPlayer(clickedPiece)) {
            this.selectSquare(row, col);
            await this.showPossibleMoves(row, col);
            return;
        }

        // Try to make a move
        if (this.isPossibleMove(row, col)) {
            await this.makeMove(this.selectedSquare.row, this.selectedSquare.col, row, col);
        } else {
            this.deselectSquare();
        }
    }

    isPieceOwnedByCurrentPlayer(piece) {
        if (this.currentGame === 'chess') {
            return this.currentPlayer === 'white' ? piece === piece.toUpperCase() : piece === piece.toLowerCase();
        } else {
            return (this.currentPlayer === 'white' && piece.toLowerCase() === 'w') ||
                   (this.currentPlayer === 'black' && piece.toLowerCase() === 'b');
        }
    }

    selectSquare(row, col) {
        this.deselectSquare();
        this.selectedSquare = { row, col };
        
        const square = document.querySelector(`[data-row="${row}"][data-col="${col}"]`);
        square.classList.add('selected');
    }

    deselectSquare() {
        if (this.selectedSquare) {
            const square = document.querySelector(`[data-row="${this.selectedSquare.row}"][data-col="${this.selectedSquare.col}"]`);
            square.classList.remove('selected');
        }
        
        this.selectedSquare = null;
        this.clearPossibleMoves();
    }

    async showPossibleMoves(row, col) {
        this.clearPossibleMoves();
        
        try {
            const response = await fetch(`${this.apiUrl}/possible_moves`, {
                method: 'POST',
                headers: { 'Content-Type': 'application/json' },
                body: JSON.stringify({
                    game_type: this.currentGame,
                    board: this.board,
                    from_row: row,
                    from_col: col,
                    current_player: this.currentPlayer
                })
            });
            
            const data = await response.json();
            this.possibleMoves = data.moves || [];
        } catch (error) {
            console.error('Error getting possible moves:', error);
            this.possibleMoves = [];
        }
        
        this.highlightPossibleMoves();
    }

    highlightPossibleMoves() {
        this.possibleMoves.forEach(move => {
            const square = document.querySelector(`[data-row="${move[0]}"][data-col="${move[1]}"]`);
            if (square) {
                square.classList.add('possible-move');
            }
        });
    }

    clearPossibleMoves() {
        document.querySelectorAll('.possible-move').forEach(square => {
            square.classList.remove('possible-move');
        });
        this.possibleMoves = [];
    }

    isPossibleMove(row, col) {
        return this.possibleMoves.some(move => move[0] === row && move[1] === col);
    }

    async makeMove(fromRow, fromCol, toRow, toCol) {
        this.showLoading(true);
        
        try {
            const response = await fetch(`${this.apiUrl}/move/${this.currentGame}`, {
                method: 'POST',
                headers: { 'Content-Type': 'application/json' },
                body: JSON.stringify({
                    board: this.board,
                    from_row: fromRow,
                    from_col: fromCol,
                    to_row: toRow,
                    to_col: toCol,
                    current_player: this.currentPlayer,
                    mode: this.gameMode,
                    difficulty: this.difficulty
                })
            });
            
            const data = await response.json();
            
            if (data.valid) {
                this.board = data.board;
                this.gameState = data.game_state;
                this.addMoveToHistory(data.move_notation || `${fromRow},${fromCol} -> ${toRow},${toCol}`);
                
                this.deselectSquare();
                this.createBoard();
                this.switchPlayer();
                this.updateUI();
                
                // Handle AI move
                if (this.gameMode === 'ai' && data.ai_move && this.gameState === 'playing') {
                    setTimeout(() => {
                        this.board = data.ai_board;
                        this.gameState = data.ai_game_state;
                        this.addMoveToHistory(data.ai_move_notation || 'AI Move');
                        
                        this.createBoard();
                        this.switchPlayer();
                        this.updateUI();
                        this.showLoading(false);
                    }, 1000);
                } else {
                    this.showLoading(false);
                }
                
                // Check for game end
                if (this.gameState !== 'playing') {
                    this.handleGameEnd();
                }
            } else {
                alert(data.message || 'Invalid move');
                this.showLoading(false);
            }
        } catch (error) {
            console.error('Error making move:', error);
            alert('Error making move. Please try again.');
            this.showLoading(false);
        }
    }

    switchPlayer() {
        this.currentPlayer = this.currentPlayer === 'white' ? 'black' : 'white';
    }

    addMoveToHistory(notation) {
        this.moveHistory.push({
            player: this.currentPlayer,
            notation: notation,
            moveNumber: Math.floor(this.moveHistory.length / 2) + 1
        });
        this.updateMoveHistory();
    }

    updateMoveHistory() {
        const movesList = document.getElementById('moves-list');
        movesList.innerHTML = '';
        
        for (let i = 0; i < this.moveHistory.length; i += 2) {
            const moveNumber = Math.floor(i / 2) + 1;
            const whiteMove = this.moveHistory[i];
            const blackMove = this.moveHistory[i + 1];
            
            const moveEntry = document.createElement('div');
            moveEntry.className = 'move-entry';
            moveEntry.textContent = `${moveNumber}. ${whiteMove.notation}`;
            
            if (blackMove) {
                moveEntry.textContent += ` ${blackMove.notation}`;
            }
            
            movesList.appendChild(moveEntry);
        }
        
        movesList.scrollTop = movesList.scrollHeight;
    }

    handleGameEnd() {
        let message = '';
        
        switch (this.gameState) {
            case 'checkmate':
                message = `Checkmate! ${this.currentPlayer === 'white' ? 'Black' : 'White'} wins!`;
                this.updateScore(this.currentPlayer === 'white' ? 'black' : 'white');
                break;
            case 'stalemate':
                message = 'Stalemate! Game is a draw.';
                break;
            case 'draw':
                message = 'Game ended in a draw.';
                break;
            case 'win':
                message = `${this.currentPlayer === 'white' ? 'Black' : 'White'} wins!`;
                this.updateScore(this.currentPlayer === 'white' ? 'black' : 'white');
                break;
        }
        
        setTimeout(() => {
            alert(message);
        }, 500);
    }

    updateScore(winner) {
        this.scores[winner]++;
        this.updateScoreBoard();
    }

    updateScoreBoard() {
        document.getElementById('white-score').textContent = this.scores.white;
        document.getElementById('black-score').textContent = this.scores.black;
    }

    updateUI() {
        // Update current turn
        const turnElement = document.getElementById('current-turn');
        turnElement.textContent = `${this.currentPlayer.charAt(0).toUpperCase() + this.currentPlayer.slice(1)}'s Turn`;
        
        // Update game status
        const statusElement = document.getElementById('game-status');
        let statusText = 'Game in progress';
        let statusClass = '';
        
        switch (this.gameState) {
            case 'check':
                statusText = 'Check!';
                statusClass = 'status-check';
                break;
            case 'checkmate':
                statusText = 'Checkmate!';
                statusClass = 'status-checkmate';
                break;
            case 'stalemate':
                statusText = 'Stalemate!';
                statusClass = 'status-stalemate';
                break;
            case 'draw':
                statusText = 'Draw!';
                statusClass = 'status-stalemate';
                break;
            case 'win':
                statusText = 'Game Over!';
                statusClass = 'status-checkmate';
                break;
        }
        
        statusElement.textContent = statusText;
        statusElement.className = statusClass;
    }

    showLoading(show) {
        const loadingElement = document.getElementById('loading');
        loadingElement.style.display = show ? 'flex' : 'none';
    }

    initializeGame() {
        this.updateDifficultyVisibility();
        this.newGame();
    }
}

// Initialize the game when the page loads
document.addEventListener('DOMContentLoaded', () => {
    window.game = new Game();
});

// Add some utility functions for local play when backend is unavailable
function getLocalPossibleMoves(board, fromRow, fromCol, currentPlayer, gameType) {
    // Basic implementation for offline play
    const moves = [];
    const piece = board[fromRow][fromCol];
    
    if (!piece) return moves;
    
    if (gameType === 'checkers') {
        // Basic checker moves
        const isWhite = piece.toLowerCase() === 'w';
        const direction = isWhite ? -1 : 1;
        const isKing = piece.toUpperCase() === piece && piece !== piece.toLowerCase();
        
        // Normal moves
        const directions = isKing ? [-1, 1] : [direction];
        
        for (const dir of directions) {
            for (const colDir of [-1, 1]) {
                const newRow = fromRow + dir;
                const newCol = fromCol + colDir;
                
                if (newRow >= 0 && newRow < 8 && newCol >= 0 && newCol < 8) {
                    if (!board[newRow][newCol]) {
                        moves.push([newRow, newCol]);
                    }
                }
            }
        }
    }
    
    return moves;
}
