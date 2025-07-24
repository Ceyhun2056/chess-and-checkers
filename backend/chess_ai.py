import random
import copy

class ChessGame:
    def __init__(self):
        self.board = self.get_initial_board()
        self.current_player = 'white'
        self.game_state = 'playing'  # 'playing', 'check', 'checkmate', 'stalemate'
        self.move_history = []
        self.castling_rights = {
            'white': {'kingside': True, 'queenside': True},
            'black': {'kingside': True, 'queenside': True}
        }
        self.en_passant_target = None
        
    def get_initial_board(self):
        """Get the initial chess board setup"""
        return [
            ['r', 'n', 'b', 'q', 'k', 'b', 'n', 'r'],  # Black pieces
            ['p', 'p', 'p', 'p', 'p', 'p', 'p', 'p'],  # Black pawns
            [None, None, None, None, None, None, None, None],
            [None, None, None, None, None, None, None, None],
            [None, None, None, None, None, None, None, None],
            [None, None, None, None, None, None, None, None],
            ['P', 'P', 'P', 'P', 'P', 'P', 'P', 'P'],  # White pawns
            ['R', 'N', 'B', 'Q', 'K', 'B', 'N', 'R']   # White pieces
        ]
    
    def get_board(self):
        """Get current board state"""
        return copy.deepcopy(self.board)
    
    def set_board(self, board):
        """Set board state"""
        self.board = copy.deepcopy(board)
    
    def is_white_piece(self, piece):
        """Check if piece belongs to white"""
        return piece and piece.isupper()
    
    def is_black_piece(self, piece):
        """Check if piece belongs to black"""
        return piece and piece.islower()
    
    def is_own_piece(self, piece, player):
        """Check if piece belongs to current player"""
        if player == 'white':
            return self.is_white_piece(piece)
        else:
            return self.is_black_piece(piece)
    
    def is_enemy_piece(self, piece, player):
        """Check if piece belongs to enemy"""
        if player == 'white':
            return self.is_black_piece(piece)
        else:
            return self.is_white_piece(piece)
    
    def is_within_board(self, row, col):
        """Check if position is within board"""
        return 0 <= row < 8 and 0 <= col < 8
    
    def get_possible_moves(self, from_row, from_col):
        """Get all possible moves for a piece"""
        piece = self.board[from_row][from_col]
        if not piece or not self.is_own_piece(piece, self.current_player):
            return []
        
        piece_type = piece.lower()
        moves = []
        
        if piece_type == 'p':
            moves = self.get_pawn_moves(from_row, from_col)
        elif piece_type == 'r':
            moves = self.get_rook_moves(from_row, from_col)
        elif piece_type == 'n':
            moves = self.get_knight_moves(from_row, from_col)
        elif piece_type == 'b':
            moves = self.get_bishop_moves(from_row, from_col)
        elif piece_type == 'q':
            moves = self.get_queen_moves(from_row, from_col)
        elif piece_type == 'k':
            moves = self.get_king_moves(from_row, from_col)
        
        # Filter out moves that would put own king in check
        legal_moves = []
        for to_row, to_col in moves:
            if self.is_legal_move(from_row, from_col, to_row, to_col):
                legal_moves.append([to_row, to_col])
        
        return legal_moves
    
    def get_pawn_moves(self, row, col):
        """Get possible pawn moves"""
        moves = []
        piece = self.board[row][col]
        is_white = self.is_white_piece(piece)
        direction = -1 if is_white else 1
        start_row = 6 if is_white else 1
        
        # Forward move
        new_row = row + direction
        if self.is_within_board(new_row, col) and not self.board[new_row][col]:
            moves.append((new_row, col))
            
            # Double forward move from starting position
            if row == start_row:
                new_row = row + 2 * direction
                if self.is_within_board(new_row, col) and not self.board[new_row][col]:
                    moves.append((new_row, col))
        
        # Diagonal captures
        for col_offset in [-1, 1]:
            new_row = row + direction
            new_col = col + col_offset
            if self.is_within_board(new_row, new_col):
                target = self.board[new_row][new_col]
                if target and self.is_enemy_piece(target, self.current_player):
                    moves.append((new_row, new_col))
        
        return moves
    
    def get_rook_moves(self, row, col):
        """Get possible rook moves"""
        moves = []
        directions = [(0, 1), (0, -1), (1, 0), (-1, 0)]
        
        for dr, dc in directions:
            for i in range(1, 8):
                new_row = row + dr * i
                new_col = col + dc * i
                
                if not self.is_within_board(new_row, new_col):
                    break
                
                target = self.board[new_row][new_col]
                if not target:
                    moves.append((new_row, new_col))
                elif self.is_enemy_piece(target, self.current_player):
                    moves.append((new_row, new_col))
                    break
                else:
                    break
        
        return moves
    
    def get_knight_moves(self, row, col):
        """Get possible knight moves"""
        moves = []
        knight_moves = [(-2, -1), (-2, 1), (-1, -2), (-1, 2),
                       (1, -2), (1, 2), (2, -1), (2, 1)]
        
        for dr, dc in knight_moves:
            new_row = row + dr
            new_col = col + dc
            
            if self.is_within_board(new_row, new_col):
                target = self.board[new_row][new_col]
                if not target or self.is_enemy_piece(target, self.current_player):
                    moves.append((new_row, new_col))
        
        return moves
    
    def get_bishop_moves(self, row, col):
        """Get possible bishop moves"""
        moves = []
        directions = [(1, 1), (1, -1), (-1, 1), (-1, -1)]
        
        for dr, dc in directions:
            for i in range(1, 8):
                new_row = row + dr * i
                new_col = col + dc * i
                
                if not self.is_within_board(new_row, new_col):
                    break
                
                target = self.board[new_row][new_col]
                if not target:
                    moves.append((new_row, new_col))
                elif self.is_enemy_piece(target, self.current_player):
                    moves.append((new_row, new_col))
                    break
                else:
                    break
        
        return moves
    
    def get_queen_moves(self, row, col):
        """Get possible queen moves"""
        return self.get_rook_moves(row, col) + self.get_bishop_moves(row, col)
    
    def get_king_moves(self, row, col):
        """Get possible king moves"""
        moves = []
        directions = [(0, 1), (0, -1), (1, 0), (-1, 0),
                     (1, 1), (1, -1), (-1, 1), (-1, -1)]
        
        for dr, dc in directions:
            new_row = row + dr
            new_col = col + dc
            
            if self.is_within_board(new_row, new_col):
                target = self.board[new_row][new_col]
                if not target or self.is_enemy_piece(target, self.current_player):
                    moves.append((new_row, new_col))
        
        return moves
    
    def is_valid_move(self, from_row, from_col, to_row, to_col):
        """Check if a move is valid"""
        # Basic bounds checking
        if not (self.is_within_board(from_row, from_col) and 
                self.is_within_board(to_row, to_col)):
            return False
        
        piece = self.board[from_row][from_col]
        if not piece or not self.is_own_piece(piece, self.current_player):
            return False
        
        # Check if destination is valid
        target = self.board[to_row][to_col]
        if target and self.is_own_piece(target, self.current_player):
            return False
        
        # Check if move is in possible moves
        possible_moves = self.get_possible_moves(from_row, from_col)
        return [to_row, to_col] in possible_moves
    
    def is_legal_move(self, from_row, from_col, to_row, to_col):
        """Check if move doesn't put own king in check"""
        # Make temporary move
        original_piece = self.board[to_row][to_col]
        self.board[to_row][to_col] = self.board[from_row][from_col]
        self.board[from_row][from_col] = None
        
        # Check if king is in check
        king_in_check = self.is_in_check(self.current_player)
        
        # Restore board
        self.board[from_row][from_col] = self.board[to_row][to_col]
        self.board[to_row][to_col] = original_piece
        
        return not king_in_check
    
    def find_king(self, player):
        """Find king position for given player"""
        king = 'K' if player == 'white' else 'k'
        for row in range(8):
            for col in range(8):
                if self.board[row][col] == king:
                    return row, col
        return None, None
    
    def is_in_check(self, player):
        """Check if player's king is in check"""
        king_row, king_col = self.find_king(player)
        if king_row is None:
            return False
        
        # Check if any enemy piece can attack the king
        enemy_player = 'black' if player == 'white' else 'white'
        
        for row in range(8):
            for col in range(8):
                piece = self.board[row][col]
                if piece and self.is_own_piece(piece, enemy_player):
                    # Temporarily switch player to get enemy moves
                    original_player = self.current_player
                    self.current_player = enemy_player
                    moves = self.get_possible_moves_without_check_filter(row, col)
                    self.current_player = original_player
                    
                    if (king_row, king_col) in moves:
                        return True
        
        return False
    
    def get_possible_moves_without_check_filter(self, from_row, from_col):
        """Get moves without filtering for check (used internally)"""
        piece = self.board[from_row][from_col]
        if not piece:
            return []
        
        piece_type = piece.lower()
        
        if piece_type == 'p':
            return self.get_pawn_moves(from_row, from_col)
        elif piece_type == 'r':
            return self.get_rook_moves(from_row, from_col)
        elif piece_type == 'n':
            return self.get_knight_moves(from_row, from_col)
        elif piece_type == 'b':
            return self.get_bishop_moves(from_row, from_col)
        elif piece_type == 'q':
            return self.get_queen_moves(from_row, from_col)
        elif piece_type == 'k':
            return self.get_king_moves(from_row, from_col)
        
        return []
    
    def make_move(self, from_row, from_col, to_row, to_col):
        """Make a move on the board"""
        if not self.is_valid_move(from_row, from_col, to_row, to_col):
            return False
        
        piece = self.board[from_row][from_col]
        captured_piece = self.board[to_row][to_col]
        
        # Make the move
        self.board[to_row][to_col] = piece
        self.board[from_row][from_col] = None
        
        # Handle pawn promotion
        if piece.lower() == 'p':
            if (piece.isupper() and to_row == 0) or (piece.islower() and to_row == 7):
                # Promote to queen by default
                self.board[to_row][to_col] = 'Q' if piece.isupper() else 'q'
        
        # Update game state
        self.current_player = 'black' if self.current_player == 'white' else 'white'
        self.update_game_state()
        
        return True
    
    def update_game_state(self):
        """Update game state (check, checkmate, stalemate)"""
        if self.is_in_check(self.current_player):
            if self.has_legal_moves(self.current_player):
                self.game_state = 'check'
            else:
                self.game_state = 'checkmate'
        else:
            if self.has_legal_moves(self.current_player):
                self.game_state = 'playing'
            else:
                self.game_state = 'stalemate'
    
    def has_legal_moves(self, player):
        """Check if player has any legal moves"""
        original_player = self.current_player
        self.current_player = player
        
        for row in range(8):
            for col in range(8):
                piece = self.board[row][col]
                if piece and self.is_own_piece(piece, player):
                    moves = self.get_possible_moves(row, col)
                    if moves:
                        self.current_player = original_player
                        return True
        
        self.current_player = original_player
        return False
    
    def get_move_notation(self, from_row, from_col, to_row, to_col):
        """Get algebraic notation for a move"""
        piece = self.board[from_row][from_col]
        captured = self.board[to_row][to_col] is not None
        
        # Convert to algebraic notation
        files = 'abcdefgh'
        from_square = files[from_col] + str(8 - from_row)
        to_square = files[to_col] + str(8 - to_row)
        
        piece_symbol = '' if piece.lower() == 'p' else piece.upper()
        capture_symbol = 'x' if captured else ''
        
        return f"{piece_symbol}{capture_symbol}{to_square}"


class ChessAI:
    def __init__(self, difficulty=2):
        self.difficulty = difficulty
        self.max_depth = difficulty  # 1=easy, 2=medium, 3=hard
        
        # Piece values
        self.piece_values = {
            'p': 1, 'n': 3, 'b': 3, 'r': 5, 'q': 9, 'k': 100,
            'P': 1, 'N': 3, 'B': 3, 'R': 5, 'Q': 9, 'K': 100
        }
        
        # Position value tables (simplified)
        self.pawn_table = [
            [0, 0, 0, 0, 0, 0, 0, 0],
            [50, 50, 50, 50, 50, 50, 50, 50],
            [10, 10, 20, 30, 30, 20, 10, 10],
            [5, 5, 10, 25, 25, 10, 5, 5],
            [0, 0, 0, 20, 20, 0, 0, 0],
            [5, -5, -10, 0, 0, -10, -5, 5],
            [5, 10, 10, -20, -20, 10, 10, 5],
            [0, 0, 0, 0, 0, 0, 0, 0]
        ]
        
        self.knight_table = [
            [-50, -40, -30, -30, -30, -30, -40, -50],
            [-40, -20, 0, 0, 0, 0, -20, -40],
            [-30, 0, 10, 15, 15, 10, 0, -30],
            [-30, 5, 15, 20, 20, 15, 5, -30],
            [-30, 0, 15, 20, 20, 15, 0, -30],
            [-30, 5, 10, 15, 15, 10, 5, -30],
            [-40, -20, 0, 5, 5, 0, -20, -40],
            [-50, -40, -30, -30, -30, -30, -40, -50]
        ]
    
    def get_best_move(self, game):
        """Get the best move using minimax algorithm"""
        original_player = game.current_player
        best_move = None
        best_value = float('-inf')
        
        # Get all possible moves
        moves = self.get_all_moves(game, 'black')  # AI plays as black
        
        if not moves:
            return None
        
        for move in moves:
            from_row, from_col, to_row, to_col = move
            
            # Make temporary move
            original_piece = game.board[to_row][to_col]
            game.board[to_row][to_col] = game.board[from_row][from_col]
            game.board[from_row][from_col] = None
            game.current_player = 'white'
            
            # Evaluate position
            value = self.minimax(game, self.max_depth - 1, float('-inf'), float('inf'), False)
            
            # Restore board
            game.board[from_row][from_col] = game.board[to_row][to_col]
            game.board[to_row][to_col] = original_piece
            game.current_player = original_player
            
            if value > best_value:
                best_value = value
                best_move = move
        
        return best_move
    
    def minimax(self, game, depth, alpha, beta, maximizing_player):
        """Minimax algorithm with alpha-beta pruning"""
        if depth == 0 or game.game_state in ['checkmate', 'stalemate']:
            return self.evaluate_position(game)
        
        if maximizing_player:
            max_eval = float('-inf')
            moves = self.get_all_moves(game, 'black')
            
            for move in moves:
                from_row, from_col, to_row, to_col = move
                
                # Make temporary move
                original_piece = game.board[to_row][to_col]
                original_player = game.current_player
                game.board[to_row][to_col] = game.board[from_row][from_col]
                game.board[from_row][from_col] = None
                game.current_player = 'white'
                
                eval_score = self.minimax(game, depth - 1, alpha, beta, False)
                
                # Restore board
                game.board[from_row][from_col] = game.board[to_row][to_col]
                game.board[to_row][to_col] = original_piece
                game.current_player = original_player
                
                max_eval = max(max_eval, eval_score)
                alpha = max(alpha, eval_score)
                
                if beta <= alpha:
                    break
            
            return max_eval
        else:
            min_eval = float('inf')
            moves = self.get_all_moves(game, 'white')
            
            for move in moves:
                from_row, from_col, to_row, to_col = move
                
                # Make temporary move
                original_piece = game.board[to_row][to_col]
                original_player = game.current_player
                game.board[to_row][to_col] = game.board[from_row][from_col]
                game.board[from_row][from_col] = None
                game.current_player = 'black'
                
                eval_score = self.minimax(game, depth - 1, alpha, beta, True)
                
                # Restore board
                game.board[from_row][from_col] = game.board[to_row][to_col]
                game.board[to_row][to_col] = original_piece
                game.current_player = original_player
                
                min_eval = min(min_eval, eval_score)
                beta = min(beta, eval_score)
                
                if beta <= alpha:
                    break
            
            return min_eval
    
    def get_all_moves(self, game, player):
        """Get all possible moves for a player"""
        moves = []
        original_player = game.current_player
        game.current_player = player
        
        for row in range(8):
            for col in range(8):
                piece = game.board[row][col]
                if piece and game.is_own_piece(piece, player):
                    piece_moves = game.get_possible_moves(row, col)
                    for to_row, to_col in piece_moves:
                        moves.append((row, col, to_row, to_col))
        
        game.current_player = original_player
        return moves
    
    def evaluate_position(self, game):
        """Evaluate the current position"""
        if game.game_state == 'checkmate':
            return 10000 if game.current_player == 'white' else -10000
        elif game.game_state == 'stalemate':
            return 0
        
        score = 0
        
        for row in range(8):
            for col in range(8):
                piece = game.board[row][col]
                if piece:
                    piece_value = self.piece_values.get(piece, 0)
                    position_value = self.get_position_value(piece, row, col)
                    
                    if game.is_black_piece(piece):
                        score += piece_value + position_value
                    else:
                        score -= piece_value + position_value
        
        return score
    
    def get_position_value(self, piece, row, col):
        """Get positional value for a piece"""
        piece_type = piece.lower()
        
        if piece_type == 'p':
            table = self.pawn_table
        elif piece_type == 'n':
            table = self.knight_table
        else:
            return 0  # Simplified - only pawn and knight tables
        
        # Flip table for black pieces
        if piece.islower():  # Black piece
            return table[row][col] / 100
        else:  # White piece
            return table[7-row][col] / 100
