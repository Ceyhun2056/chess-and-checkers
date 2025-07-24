import random
import copy

class CheckersGame:
    def __init__(self):
        self.board = self.get_initial_board()
        self.current_player = 'white'
        self.game_state = 'playing'  # 'playing', 'win'
        self.move_history = []
        self.must_capture = False  # Force capture if available
        
    def get_initial_board(self):
        """Get the initial checkers board setup"""
        board = [[None for _ in range(8)] for _ in range(8)]
        
        # Place black pieces (lowercase 'b')
        for row in range(3):
            for col in range(8):
                if (row + col) % 2 == 1:  # Dark squares only
                    board[row][col] = 'b'
        
        # Place white pieces (lowercase 'w')
        for row in range(5, 8):
            for col in range(8):
                if (row + col) % 2 == 1:  # Dark squares only
                    board[row][col] = 'w'
        
        return board
    
    def get_board(self):
        """Get current board state"""
        return copy.deepcopy(self.board)
    
    def set_board(self, board):
        """Set board state"""
        self.board = copy.deepcopy(board)
    
    def is_white_piece(self, piece):
        """Check if piece belongs to white"""
        return piece and piece.lower() == 'w'
    
    def is_black_piece(self, piece):
        """Check if piece belongs to black"""
        return piece and piece.lower() == 'b'
    
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
    
    def is_king(self, piece):
        """Check if piece is a king"""
        return piece and piece.isupper()
    
    def is_within_board(self, row, col):
        """Check if position is within board"""
        return 0 <= row < 8 and 0 <= col < 8
    
    def is_dark_square(self, row, col):
        """Check if square is dark (playable in checkers)"""
        return (row + col) % 2 == 1
    
    def get_possible_moves(self, from_row, from_col):
        """Get all possible moves for a piece"""
        piece = self.board[from_row][from_col]
        if not piece or not self.is_own_piece(piece, self.current_player):
            return []
        
        # Check for forced captures first
        capture_moves = self.get_capture_moves(from_row, from_col)
        if capture_moves:
            return [[move[0], move[1]] for move in capture_moves]
        
        # If no captures, get regular moves
        regular_moves = self.get_regular_moves(from_row, from_col)
        return [[move[0], move[1]] for move in regular_moves]
    
    def get_regular_moves(self, from_row, from_col):
        """Get regular (non-capture) moves"""
        moves = []
        piece = self.board[from_row][from_col]
        
        if not piece:
            return moves
        
        is_king = self.is_king(piece)
        is_white = self.is_white_piece(piece)
        
        # Determine directions
        if is_king:
            directions = [(-1, -1), (-1, 1), (1, -1), (1, 1)]
        else:
            if is_white:
                directions = [(-1, -1), (-1, 1)]  # White moves up
            else:
                directions = [(1, -1), (1, 1)]    # Black moves down
        
        # Check each direction
        for dr, dc in directions:
            new_row = from_row + dr
            new_col = from_col + dc
            
            if (self.is_within_board(new_row, new_col) and 
                self.is_dark_square(new_row, new_col) and 
                not self.board[new_row][new_col]):
                moves.append((new_row, new_col))
        
        return moves
    
    def get_capture_moves(self, from_row, from_col):
        """Get capture moves for a piece"""
        captures = []
        piece = self.board[from_row][from_col]
        
        if not piece:
            return captures
        
        is_king = self.is_king(piece)
        is_white = self.is_white_piece(piece)
        
        # Determine directions
        if is_king:
            directions = [(-1, -1), (-1, 1), (1, -1), (1, 1)]
        else:
            if is_white:
                directions = [(-1, -1), (-1, 1)]  # White moves up
            else:
                directions = [(1, -1), (1, 1)]    # Black moves down
        
        # Check each direction for captures
        for dr, dc in directions:
            enemy_row = from_row + dr
            enemy_col = from_col + dc
            landing_row = from_row + 2 * dr
            landing_col = from_col + 2 * dc
            
            if (self.is_within_board(enemy_row, enemy_col) and
                self.is_within_board(landing_row, landing_col) and
                self.is_dark_square(landing_row, landing_col)):
                
                enemy_piece = self.board[enemy_row][enemy_col]
                landing_piece = self.board[landing_row][landing_col]
                
                if (enemy_piece and 
                    self.is_enemy_piece(enemy_piece, self.current_player) and
                    not landing_piece):
                    captures.append((landing_row, landing_col, enemy_row, enemy_col))
        
        return captures
    
    def has_captures_available(self, player):
        """Check if player has any capture moves available"""
        for row in range(8):
            for col in range(8):
                piece = self.board[row][col]
                if piece and self.is_own_piece(piece, player):
                    if self.get_capture_moves(row, col):
                        return True
        return False
    
    def is_valid_move(self, from_row, from_col, to_row, to_col):
        """Check if a move is valid"""
        # Basic bounds checking
        if not (self.is_within_board(from_row, from_col) and 
                self.is_within_board(to_row, to_col)):
            return False
        
        # Check if destination is dark square
        if not self.is_dark_square(to_row, to_col):
            return False
        
        piece = self.board[from_row][from_col]
        if not piece or not self.is_own_piece(piece, self.current_player):
            return False
        
        # Check if destination is empty
        if self.board[to_row][to_col]:
            return False
        
        # Check if move is in possible moves
        possible_moves = self.get_possible_moves(from_row, from_col)
        return [to_row, to_col] in possible_moves
    
    def make_move(self, from_row, from_col, to_row, to_col):
        """Make a move on the board"""
        if not self.is_valid_move(from_row, from_col, to_row, to_col):
            return False
        
        piece = self.board[from_row][from_col]
        
        # Check if it's a capture move
        capture_moves = self.get_capture_moves(from_row, from_col)
        captured_piece_pos = None
        
        for capture in capture_moves:
            if capture[0] == to_row and capture[1] == to_col:
                captured_piece_pos = (capture[2], capture[3])
                break
        
        # Make the move
        self.board[to_row][to_col] = piece
        self.board[from_row][from_col] = None
        
        # Remove captured piece
        if captured_piece_pos:
            self.board[captured_piece_pos[0]][captured_piece_pos[1]] = None
        
        # Check for king promotion
        if piece.lower() == 'w' and to_row == 0:  # White reaches top
            self.board[to_row][to_col] = 'W'
        elif piece.lower() == 'b' and to_row == 7:  # Black reaches bottom
            self.board[to_row][to_col] = 'B'
        
        # Check for additional captures (multiple jumps)
        additional_captures = self.get_capture_moves(to_row, to_col)
        if not additional_captures:
            # Switch players only if no more captures available
            self.current_player = 'black' if self.current_player == 'white' else 'white'
        
        # Update game state
        self.update_game_state()
        
        return True
    
    def update_game_state(self):
        """Update game state"""
        white_pieces = 0
        black_pieces = 0
        
        # Count pieces
        for row in range(8):
            for col in range(8):
                piece = self.board[row][col]
                if piece:
                    if self.is_white_piece(piece):
                        white_pieces += 1
                    elif self.is_black_piece(piece):
                        black_pieces += 1
        
        # Check for win conditions
        if white_pieces == 0:
            self.game_state = 'win'  # Black wins
        elif black_pieces == 0:
            self.game_state = 'win'  # White wins
        elif not self.has_legal_moves(self.current_player):
            self.game_state = 'win'  # Current player has no moves
        else:
            self.game_state = 'playing'
    
    def has_legal_moves(self, player):
        """Check if player has any legal moves"""
        for row in range(8):
            for col in range(8):
                piece = self.board[row][col]
                if piece and self.is_own_piece(piece, player):
                    moves = self.get_possible_moves(row, col)
                    if moves:
                        return True
        return False


class CheckersAI:
    def __init__(self, difficulty=2):
        self.difficulty = difficulty
        self.max_depth = difficulty * 2  # 2=easy, 4=medium, 6=hard
        
        # Piece values
        self.piece_values = {
            'w': 1, 'W': 3,  # White piece, White king
            'b': 1, 'B': 3   # Black piece, Black king
        }
        
        # Position values - favor center and advanced positions
        self.position_values = [
            [0, 1, 0, 1, 0, 1, 0, 1],
            [1, 0, 2, 0, 2, 0, 2, 0],
            [0, 2, 0, 3, 0, 3, 0, 2],
            [2, 0, 3, 0, 4, 0, 3, 0],
            [0, 3, 0, 4, 0, 3, 0, 2],
            [2, 0, 3, 0, 3, 0, 2, 0],
            [0, 2, 0, 2, 0, 2, 0, 1],
            [1, 0, 1, 0, 1, 0, 1, 0]
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
        
        # Prioritize capture moves
        capture_moves = []
        regular_moves = []
        
        for move in moves:
            from_row, from_col, to_row, to_col = move
            captures = game.get_capture_moves(from_row, from_col)
            if any(c[0] == to_row and c[1] == to_col for c in captures):
                capture_moves.append(move)
            else:
                regular_moves.append(move)
        
        # Evaluate captures first
        moves_to_evaluate = capture_moves if capture_moves else regular_moves
        
        for move in moves_to_evaluate:
            from_row, from_col, to_row, to_col = move
            
            # Make temporary move
            original_board = copy.deepcopy(game.board)
            original_game_state = game.game_state
            
            game.make_move(from_row, from_col, to_row, to_col)
            
            # Evaluate position
            if self.difficulty == 1:
                # Easy: Random with slight preference for captures
                value = random.random()
                if capture_moves and move in capture_moves:
                    value += 0.5
            else:
                # Medium/Hard: Use minimax
                value = self.minimax(game, self.max_depth - 1, float('-inf'), float('inf'), False)
            
            # Restore board
            game.board = original_board
            game.current_player = original_player
            game.game_state = original_game_state
            
            if value > best_value:
                best_value = value
                best_move = move
        
        return best_move
    
    def minimax(self, game, depth, alpha, beta, maximizing_player):
        """Minimax algorithm with alpha-beta pruning"""
        if depth == 0 or game.game_state == 'win':
            return self.evaluate_position(game)
        
        if maximizing_player:
            max_eval = float('-inf')
            moves = self.get_all_moves(game, 'black')
            
            for move in moves:
                from_row, from_col, to_row, to_col = move
                
                # Make temporary move
                original_board = copy.deepcopy(game.board)
                original_player = game.current_player
                original_state = game.game_state
                
                game.make_move(from_row, from_col, to_row, to_col)
                
                eval_score = self.minimax(game, depth - 1, alpha, beta, False)
                
                # Restore board
                game.board = original_board
                game.current_player = original_player
                game.game_state = original_state
                
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
                original_board = copy.deepcopy(game.board)
                original_player = game.current_player
                original_state = game.game_state
                
                game.make_move(from_row, from_col, to_row, to_col)
                
                eval_score = self.minimax(game, depth - 1, alpha, beta, True)
                
                # Restore board
                game.board = original_board
                game.current_player = original_player
                game.game_state = original_state
                
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
        if game.game_state == 'win':
            # Determine winner
            white_pieces = sum(1 for row in game.board for piece in row if piece and game.is_white_piece(piece))
            black_pieces = sum(1 for row in game.board for piece in row if piece and game.is_black_piece(piece))
            
            if black_pieces == 0:
                return -10000  # White wins (bad for AI)
            elif white_pieces == 0:
                return 10000   # Black wins (good for AI)
            elif not game.has_legal_moves('black'):
                return -10000  # Black has no moves (bad for AI)
            else:
                return 10000   # White has no moves (good for AI)
        
        score = 0
        
        for row in range(8):
            for col in range(8):
                piece = game.board[row][col]
                if piece:
                    piece_value = self.piece_values.get(piece, 0)
                    position_value = self.position_values[row][col] * 0.1
                    
                    total_value = piece_value + position_value
                    
                    if game.is_black_piece(piece):
                        score += total_value
                        # Bonus for advanced pieces
                        if row > 4:
                            score += 0.5
                    else:
                        score -= total_value
                        # Bonus for advanced pieces
                        if row < 3:
                            score -= 0.5
        
        # Bonus for piece advantage
        white_count = sum(1 for row in game.board for piece in row if piece and game.is_white_piece(piece))
        black_count = sum(1 for row in game.board for piece in row if piece and game.is_black_piece(piece))
        score += (black_count - white_count) * 2
        
        # Bonus for mobility (number of available moves)
        black_moves = len(self.get_all_moves(game, 'black'))
        white_moves = len(self.get_all_moves(game, 'white'))
        score += (black_moves - white_moves) * 0.1
        
        return score
