// Chess Game Engine
class ChessGame {
    constructor() {
        this.gameMode = 'ai'; // 'ai' or 'player'
        this.difficulty = 2;
        this.currentPlayer = 'white';
        this.selected = null;
        this.possibleMoves = [];
        this.board = null;
        this.gameState = 'playing';
        this.moveHistory = [];
        this.scores = { white: 0, black: 0 };
        this.gameOver = false;
        
        this.chessSymbols = {
            'K': '♔', 'Q': '♕', 'R': '♖', 'B': '♗', 'N': '♘', 'P': '♙',
            'k': '♚', 'q': '♛', 'r': '♜', 'b': '♝', 'n': '♞', 'p': '♟'
        };
        
        this.initializeEventListeners();
        this.newGame();
    }
    
    initializeEventListeners() {
        // Controls
        document.getElementById('game-mode').addEventListener('change', (e) => {
            this.gameMode = e.target.value;
            this.updateDifficultyVisibility();
            this.newGame();
        });
        
        document.getElementById('difficulty').addEventListener('change', (e) => {
            this.difficulty = parseInt(e.target.value);
        });
        
        document.getElementById('reset-btn').addEventListener('click', () => this.resetGame());
    }
    
    updateDifficultyVisibility() {
        const difficultyContainer = document.getElementById('difficulty-container');
        difficultyContainer.style.display = this.gameMode === 'ai' ? 'block' : 'none';
    }
    
    newGame() {
        this.currentPlayer = 'white';
        this.selected = null;
        this.possibleMoves = [];
        this.gameState = 'playing';
        this.moveHistory = [];
        this.gameOver = false;
        
        this.board = this.getInitialChessBoard();
        
        this.renderBoard();
        this.updateUI();
    }
    
    resetGame() {
        this.scores = { white: 0, black: 0 };
        this.updateScoreBoard();
        this.newGame();
    }
    
    getInitialChessBoard() {
        return [
            ['r','n','b','q','k','b','n','r'],
            ['p','p','p','p','p','p','p','p'],
            [null,null,null,null,null,null,null,null],
            [null,null,null,null,null,null,null,null],
            [null,null,null,null,null,null,null,null],
            [null,null,null,null,null,null,null,null],
            ['P','P','P','P','P','P','P','P'],
            ['R','N','B','Q','K','B','N','R']
        ];
    }
    
    renderBoard() {
        const boardElement = document.getElementById('game-board');
        boardElement.innerHTML = '';
        
        for (let r = 0; r < 8; r++) {
            for (let c = 0; c < 8; c++) {
                const square = document.createElement('div');
                square.className = `square ${(r + c) % 2 === 0 ? 'white' : 'black'}`;
                square.dataset.r = r;
                square.dataset.c = c;
                
                // Add selection and move highlighting
                if (this.selected && this.selected[0] === r && this.selected[1] === c) {
                    square.classList.add('selected');
                }
                if (this.possibleMoves.some(([rr, cc]) => rr === r && cc === c)) {
                    square.classList.add('move');
                }
                
                const piece = this.board[r][c];
                if (piece) {
                    const pieceElement = this.createPieceElement(piece);
                    square.appendChild(pieceElement);
                }
                
                square.addEventListener('click', () => this.onSquareClick(r, c));
                boardElement.appendChild(square);
            }
        }
    }
    
    createPieceElement(piece) {
        const pieceElement = document.createElement('span');
        pieceElement.className = `piece chess-piece ${/[A-Z]/.test(piece) ? 'white' : 'black'}`;
        pieceElement.textContent = this.chessSymbols[piece] || piece;
        return pieceElement;
    }
    
    onSquareClick(r, c) {
        if (this.gameOver) return;
        
        // Prevent moves when it's AI's turn
        if (this.gameMode === 'ai' && this.currentPlayer === 'black') return;
        
        const piece = this.board[r][c];
        
        if (this.selected) {
            // Try to move
            if (this.possibleMoves.some(([rr, cc]) => rr === r && cc === c)) {
                this.makeMove(this.selected[0], this.selected[1], r, c);
                this.selected = null;
                this.possibleMoves = [];
                this.renderBoard();
                
                // AI move after a delay
                if (this.gameMode === 'ai' && !this.gameOver && this.currentPlayer === 'black') {
                    this.showLoading(true);
                    setTimeout(() => {
                        this.makeAIMove();
                        this.showLoading(false);
                    }, 500);
                }
                return;
            }
            
            // Deselect if clicking elsewhere
            this.selected = null;
            this.possibleMoves = [];
            this.renderBoard();
        }
        
        // Select piece if it belongs to current player
        if (piece && this.isOwnPiece(piece)) {
            this.selected = [r, c];
            this.possibleMoves = this.getPossibleMoves(r, c);
            this.renderBoard();
        }
    }
    
    isOwnPiece(piece) {
        return (this.currentPlayer === 'white') === /[A-Z]/.test(piece);
    }
    
    makeMove(fromR, fromC, toR, toC) {
        const piece = this.board[fromR][fromC];
        const capturedPiece = this.board[toR][toC];
        
        // Move the piece
        this.board[toR][toC] = piece;
        this.board[fromR][fromC] = null;
        
        // Chess notation (simplified)
        const pieceSymbol = piece.toUpperCase() === 'P' ? '' : piece.toUpperCase();
        const captureSymbol = capturedPiece ? '×' : '';
        const square = `${String.fromCharCode(97 + toC)}${8 - toR}`;
        let moveNotation = `${pieceSymbol}${captureSymbol}${square}`;
        
        // Pawn promotion (auto-promote to Queen)
        if (piece.toLowerCase() === 'p' && (toR === 0 || toR === 7)) {
            this.board[toR][toC] = piece === 'P' ? 'Q' : 'q';
            moveNotation += '=Q';
        }
        
        // Special chess rules
        this.handleSpecialChessRules(piece, fromR, fromC, toR, toC);
        
        // Add move to history
        this.addMoveToHistory(moveNotation);
        
        // Switch players
        this.currentPlayer = this.currentPlayer === 'white' ? 'black' : 'white';
        
        // Update game state
        this.updateGameState();
        this.updateUI();
    }
    
    handleSpecialChessRules(piece, fromR, fromC, toR, toC) {
        // Handle castling (simplified implementation)
        if (piece.toLowerCase() === 'k' && Math.abs(toC - fromC) === 2) {
            // Castling - move the rook
            if (toC === 6) { // King-side castling
                this.board[fromR][5] = this.board[fromR][7];
                this.board[fromR][7] = null;
            } else if (toC === 2) { // Queen-side castling
                this.board[fromR][3] = this.board[fromR][0];
                this.board[fromR][0] = null;
            }
        }
        
        // Handle en passant (simplified - not fully implemented)
        if (piece.toLowerCase() === 'p' && Math.abs(toC - fromC) === 1 && !this.board[toR][toC]) {
            // En passant capture
            this.board[fromR][toC] = null;
        }
    }
    
    getPossibleMoves(r, c) {
        return this.getChessMoves(r, c);
    }
    
    getChessMoves(r, c) {
        const piece = this.board[r][c];
        const moves = [];
        const isWhite = /[A-Z]/.test(piece);
        
        if (piece.toLowerCase() === 'p') {
            // Pawn moves
            const dir = isWhite ? -1 : 1;
            const startRow = isWhite ? 6 : 1;
            
            // Forward moves
            if (r + dir >= 0 && r + dir < 8 && !this.board[r + dir][c]) {
                moves.push([r + dir, c]);
                
                // Double move from starting position
                if (r === startRow && !this.board[r + 2 * dir][c]) {
                    moves.push([r + 2 * dir, c]);
                }
            }
            
            // Diagonal captures
            for (const dc of [-1, 1]) {
                if (c + dc >= 0 && c + dc < 8 && r + dir >= 0 && r + dir < 8) {
                    const target = this.board[r + dir][c + dc];
                    if (target && /[A-Z]/.test(target) !== isWhite) {
                        moves.push([r + dir, c + dc]);
                    }
                }
            }
        } else if (piece.toLowerCase() === 'r') {
            // Rook moves - horizontal and vertical
            for (const [dr, dc] of [[0, 1], [0, -1], [1, 0], [-1, 0]]) {
                for (let i = 1; i < 8; i++) {
                    const newR = r + dr * i;
                    const newC = c + dc * i;
                    
                    if (newR < 0 || newR >= 8 || newC < 0 || newC >= 8) break;
                    
                    const target = this.board[newR][newC];
                    if (!target) {
                        moves.push([newR, newC]);
                    } else {
                        if (/[A-Z]/.test(target) !== isWhite) {
                            moves.push([newR, newC]);
                        }
                        break; // Can't continue past any piece
                    }
                }
            }
        } else if (piece.toLowerCase() === 'b') {
            // Bishop moves - diagonal
            for (const [dr, dc] of [[1, 1], [1, -1], [-1, 1], [-1, -1]]) {
                for (let i = 1; i < 8; i++) {
                    const newR = r + dr * i;
                    const newC = c + dc * i;
                    
                    if (newR < 0 || newR >= 8 || newC < 0 || newC >= 8) break;
                    
                    const target = this.board[newR][newC];
                    if (!target) {
                        moves.push([newR, newC]);
                    } else {
                        if (/[A-Z]/.test(target) !== isWhite) {
                            moves.push([newR, newC]);
                        }
                        break; // Can't continue past any piece
                    }
                }
            }
        } else if (piece.toLowerCase() === 'q') {
            // Queen moves - combination of rook and bishop
            for (const [dr, dc] of [[0, 1], [0, -1], [1, 0], [-1, 0], [1, 1], [1, -1], [-1, 1], [-1, -1]]) {
                for (let i = 1; i < 8; i++) {
                    const newR = r + dr * i;
                    const newC = c + dc * i;
                    
                    if (newR < 0 || newR >= 8 || newC < 0 || newC >= 8) break;
                    
                    const target = this.board[newR][newC];
                    if (!target) {
                        moves.push([newR, newC]);
                    } else {
                        if (/[A-Z]/.test(target) !== isWhite) {
                            moves.push([newR, newC]);
                        }
                        break; // Can't continue past any piece
                    }
                }
            }
        } else if (piece.toLowerCase() === 'n') {
            // Knight moves - L-shaped
            const knightMoves = [[-2, -1], [-2, 1], [-1, -2], [-1, 2], [1, -2], [1, 2], [2, -1], [2, 1]];
            for (const [dr, dc] of knightMoves) {
                const newR = r + dr;
                const newC = c + dc;
                
                if (newR >= 0 && newR < 8 && newC >= 0 && newC < 8) {
                    const target = this.board[newR][newC];
                    if (!target || /[A-Z]/.test(target) !== isWhite) {
                        moves.push([newR, newC]);
                    }
                }
            }
        } else if (piece.toLowerCase() === 'k') {
            // King moves - one square in any direction
            for (let dr = -1; dr <= 1; dr++) {
                for (let dc = -1; dc <= 1; dc++) {
                    if (dr === 0 && dc === 0) continue;
                    
                    const newR = r + dr;
                    const newC = c + dc;
                    
                    if (newR >= 0 && newR < 8 && newC >= 0 && newC < 8) {
                        const target = this.board[newR][newC];
                        if (!target || /[A-Z]/.test(target) !== isWhite) {
                            // Check if this move would put king in check (simplified)
                            if (!this.wouldBeInCheck(newR, newC, isWhite)) {
                                moves.push([newR, newC]);
                            }
                        }
                    }
                }
            }
            
            // Castling (simplified - assumes king and rook haven't moved)
            if (!this.isInCheck(isWhite)) {
                // King-side castling
                if (c === 4 && !this.board[r][5] && !this.board[r][6] && 
                    this.board[r][7] && this.board[r][7].toLowerCase() === 'r') {
                    if (!this.wouldBeInCheck(r, 5, isWhite) && !this.wouldBeInCheck(r, 6, isWhite)) {
                        moves.push([r, 6]);
                    }
                }
                
                // Queen-side castling
                if (c === 4 && !this.board[r][3] && !this.board[r][2] && !this.board[r][1] &&
                    this.board[r][0] && this.board[r][0].toLowerCase() === 'r') {
                    if (!this.wouldBeInCheck(r, 3, isWhite) && !this.wouldBeInCheck(r, 2, isWhite)) {
                        moves.push([r, 2]);
                    }
                }
            }
        }
        
        // Filter out moves that would put own king in check
        return moves.filter(([toR, toC]) => {
            return !this.wouldMoveResultInCheck(r, c, toR, toC, isWhite);
        });
    }
    
    isInCheck(isWhite) {
        // Find the king
        let kingR = -1, kingC = -1;
        for (let r = 0; r < 8; r++) {
            for (let c = 0; c < 8; c++) {
                const piece = this.board[r][c];
                if (piece && piece.toLowerCase() === 'k' && (/[A-Z]/.test(piece) === isWhite)) {
                    kingR = r;
                    kingC = c;
                    break;
                }
            }
            if (kingR !== -1) break;
        }
        
        if (kingR === -1) return false; // No king found
        
        return this.wouldBeInCheck(kingR, kingC, isWhite);
    }
    
    wouldBeInCheck(kingR, kingC, isWhite) {
        // Check if any enemy piece can attack this position
        for (let r = 0; r < 8; r++) {
            for (let c = 0; c < 8; c++) {
                const piece = this.board[r][c];
                if (piece && (/[A-Z]/.test(piece) !== isWhite)) {
                    if (this.canPieceAttack(piece, r, c, kingR, kingC)) {
                        return true;
                    }
                }
            }
        }
        return false;
    }
    
    canPieceAttack(piece, fromR, fromC, toR, toC) {
        const isWhite = /[A-Z]/.test(piece);
        
        if (piece.toLowerCase() === 'p') {
            const dir = isWhite ? -1 : 1;
            return (fromR + dir === toR && Math.abs(fromC - toC) === 1);
        } else if (piece.toLowerCase() === 'r') {
            return (fromR === toR || fromC === toC) && this.isPathClear(fromR, fromC, toR, toC);
        } else if (piece.toLowerCase() === 'b') {
            return Math.abs(fromR - toR) === Math.abs(fromC - toC) && this.isPathClear(fromR, fromC, toR, toC);
        } else if (piece.toLowerCase() === 'q') {
            return ((fromR === toR || fromC === toC) || (Math.abs(fromR - toR) === Math.abs(fromC - toC))) && 
                   this.isPathClear(fromR, fromC, toR, toC);
        } else if (piece.toLowerCase() === 'n') {
            const dr = Math.abs(fromR - toR);
            const dc = Math.abs(fromC - toC);
            return (dr === 2 && dc === 1) || (dr === 1 && dc === 2);
        } else if (piece.toLowerCase() === 'k') {
            return Math.abs(fromR - toR) <= 1 && Math.abs(fromC - toC) <= 1;
        }
        
        return false;
    }
    
    isPathClear(fromR, fromC, toR, toC) {
        const dr = Math.sign(toR - fromR);
        const dc = Math.sign(toC - fromC);
        
        let r = fromR + dr;
        let c = fromC + dc;
        
        while (r !== toR || c !== toC) {
            if (this.board[r][c] !== null) return false;
            r += dr;
            c += dc;
        }
        
        return true;
    }
    
    wouldMoveResultInCheck(fromR, fromC, toR, toC, isWhite) {
        // Temporarily make the move
        const originalPiece = this.board[toR][toC];
        const movingPiece = this.board[fromR][fromC];
        
        this.board[toR][toC] = movingPiece;
        this.board[fromR][fromC] = null;
        
        const inCheck = this.isInCheck(isWhite);
        
        // Restore the board
        this.board[fromR][fromC] = movingPiece;
        this.board[toR][toC] = originalPiece;
        
        return inCheck;
    }
    
    makeAIMove() {
        const allMoves = [];
        
        // Get all legal moves for current player
        for (let r = 0; r < 8; r++) {
            for (let c = 0; c < 8; c++) {
                const piece = this.board[r][c];
                if (piece && this.isOwnPiece(piece)) {
                    const moves = this.getPossibleMoves(r, c);
                    for (const move of moves) {
                        allMoves.push([r, c, move[0], move[1]]);
                    }
                }
            }
        }
        
        if (allMoves.length === 0) return;
        
        let bestMove;
        
        if (this.difficulty === 1) {
            // Easy: Random move
            bestMove = allMoves[Math.floor(Math.random() * allMoves.length)];
        } else if (this.difficulty === 2) {
            // Medium: Prefer captures
            const captureMoves = allMoves.filter(([fromR, fromC, toR, toC]) => {
                return this.board[toR][toC] !== null;
            });
            
            if (captureMoves.length > 0) {
                bestMove = captureMoves[Math.floor(Math.random() * captureMoves.length)];
            } else {
                bestMove = allMoves[Math.floor(Math.random() * allMoves.length)];
            }
        } else {
            // Hard: Basic minimax
            bestMove = this.getBestMoveMinimaxSimple(allMoves);
        }
        
        if (bestMove) {
            this.makeMove(bestMove[0], bestMove[1], bestMove[2], bestMove[3]);
            this.selected = null;
            this.possibleMoves = [];
            this.renderBoard();
        }
    }
    
    getBestMoveMinimaxSimple(moves) {
        let bestMove = null;
        let bestScore = -Infinity;
        
        for (const move of moves) {
            const [fromR, fromC, toR, toC] = move;
            const originalPiece = this.board[toR][toC];
            
            // Make temporary move
            this.board[toR][toC] = this.board[fromR][fromC];
            this.board[fromR][fromC] = null;
            
            // Evaluate position
            const score = this.evaluatePosition();
            
            // Restore position
            this.board[fromR][fromC] = this.board[toR][toC];
            this.board[toR][toC] = originalPiece;
            
            if (score > bestScore) {
                bestScore = score;
                bestMove = move;
            }
        }
        
        return bestMove;
    }
    
    evaluatePosition() {
        const pieceValues = {
            'p': 1, 'n': 3, 'b': 3, 'r': 5, 'q': 9, 'k': 100,
            'P': 1, 'N': 3, 'B': 3, 'R': 5, 'Q': 9, 'K': 100
        };
        
        let score = 0;
        
        for (let r = 0; r < 8; r++) {
            for (let c = 0; c < 8; c++) {
                const piece = this.board[r][c];
                if (piece) {
                    const value = pieceValues[piece] || 0;
                    score += /[a-z]/.test(piece) ? value : -value;
                }
            }
        }
        
        return score;
    }
    
    updateGameState() {
        // Check if current player has any legal moves
        let hasLegalMoves = false;
        
        for (let r = 0; r < 8; r++) {
            for (let c = 0; c < 8; c++) {
                const piece = this.board[r][c];
                if (piece && this.isOwnPiece(piece)) {
                    if (this.getPossibleMoves(r, c).length > 0) {
                        hasLegalMoves = true;
                        break;
                    }
                }
            }
            if (hasLegalMoves) break;
        }
        
        if (!hasLegalMoves) {
            this.gameOver = true;
            
            const isWhite = this.currentPlayer === 'white';
            if (this.isInCheck(isWhite)) {
                // Checkmate
                this.gameState = 'checkmate';
                const winner = this.currentPlayer === 'white' ? 'Black' : 'White';
                this.updateScore(winner.toLowerCase());
                setTimeout(() => {
                    alert(`Checkmate! ${winner} wins!`);
                }, 100);
            } else {
                // Stalemate
                this.gameState = 'stalemate';
                setTimeout(() => {
                    alert('Stalemate! The game is a draw.');
                }, 100);
            }
        } else {
            this.gameState = 'playing';
            
            // Check for check
            const isWhite = this.currentPlayer === 'white';
            if (this.isInCheck(isWhite)) {
                this.gameState = 'check';
            }
        }
    }
    
    updateScore(winner) {
        this.scores[winner]++;
        this.updateScoreBoard();
    }
    
    updateScoreBoard() {
        document.getElementById('white-score').textContent = this.scores.white;
        document.getElementById('black-score').textContent = this.scores.black;
    }
    
    addMoveToHistory(notation) {
        this.moveHistory.push(notation);
        this.updateMoveHistory();
    }
    
    updateMoveHistory() {
        const movesList = document.getElementById('moves-list');
        movesList.innerHTML = '';
        
        for (let i = 0; i < this.moveHistory.length; i += 2) {
            const moveNumber = Math.floor(i / 2) + 1;
            const whiteMove = this.moveHistory[i];
            const blackMove = this.moveHistory[i + 1] || '';
            
            const moveDiv = document.createElement('div');
            moveDiv.className = 'move-pair';
            moveDiv.innerHTML = `
                <span class="move-number">${moveNumber}.</span>
                <span class="move white-move">${whiteMove}</span>
                <span class="move black-move">${blackMove}</span>
            `;
            movesList.appendChild(moveDiv);
        }
        
        movesList.scrollTop = movesList.scrollHeight;
    }
    
    updateUI() {
        // Update current turn
        const turnElement = document.getElementById('current-turn');
        if (this.gameOver) {
            turnElement.textContent = 'Game Over';
        } else {
            turnElement.textContent = `${this.currentPlayer.charAt(0).toUpperCase() + this.currentPlayer.slice(1)}'s Turn`;
        }
        
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
                const winner = this.currentPlayer === 'white' ? 'Black' : 'White';
                statusText = `Checkmate! ${winner} wins!`;
                statusClass = 'status-checkmate';
                break;
            case 'stalemate':
                statusText = 'Stalemate - Draw!';
                statusClass = 'status-stalemate';
                break;
            default:
                statusText = 'Game in progress';
                statusClass = '';
        }
        
        statusElement.textContent = statusText;
        statusElement.className = `status-display game-status ${statusClass}`;
    }
    
    showLoading(show) {
        const loadingElement = document.getElementById('loading');
        loadingElement.style.display = show ? 'flex' : 'none';
    }
}

// Initialize game when page loads
document.addEventListener('DOMContentLoaded', () => {
    window.game = new ChessGame();
});
