from flask import Flask, request, jsonify
from flask_cors import CORS
import json
from chess_ai import ChessAI, ChessGame
from checkers_ai import CheckersAI, CheckersGame

app = Flask(__name__)
CORS(app)  # Enable CORS for all routes

# Game instances storage
games = {}

@app.route('/new_game', methods=['POST'])
def new_game():
    """Initialize a new game"""
    try:
        data = request.get_json()
        game_type = data.get('game_type', 'chess')
        mode = data.get('mode', 'ai')
        difficulty = data.get('difficulty', 2)
        
        game_id = f"{game_type}_{len(games)}"
        
        if game_type == 'chess':
            game = ChessGame()
            if mode == 'ai':
                ai = ChessAI(difficulty)
                games[game_id] = {'game': game, 'ai': ai, 'type': 'chess'}
            else:
                games[game_id] = {'game': game, 'ai': None, 'type': 'chess'}
        else:  # checkers
            game = CheckersGame()
            if mode == 'ai':
                ai = CheckersAI(difficulty)
                games[game_id] = {'game': game, 'ai': ai, 'type': 'checkers'}
            else:
                games[game_id] = {'game': game, 'ai': None, 'type': 'checkers'}
        
        return jsonify({
            'success': True,
            'game_id': game_id,
            'board': game.get_board(),
            'current_player': game.current_player,
            'game_state': game.game_state
        })
    
    except Exception as e:
        return jsonify({'success': False, 'error': str(e)}), 500

@app.route('/possible_moves', methods=['POST'])
def get_possible_moves():
    """Get possible moves for a piece"""
    try:
        data = request.get_json()
        game_type = data.get('game_type', 'chess')
        board = data.get('board')
        from_row = data.get('from_row')
        from_col = data.get('from_col')
        current_player = data.get('current_player', 'white')
        
        if game_type == 'chess':
            game = ChessGame()
            game.set_board(board)
            game.current_player = current_player
            moves = game.get_possible_moves(from_row, from_col)
        else:  # checkers
            game = CheckersGame()
            game.set_board(board)
            game.current_player = current_player
            moves = game.get_possible_moves(from_row, from_col)
        
        return jsonify({
            'success': True,
            'moves': moves
        })
    
    except Exception as e:
        return jsonify({'success': False, 'error': str(e)}), 500

@app.route('/move/chess', methods=['POST'])
def make_chess_move():
    """Make a chess move"""
    try:
        data = request.get_json()
        board = data.get('board')
        from_row = data.get('from_row')
        from_col = data.get('from_col')
        to_row = data.get('to_row')
        to_col = data.get('to_col')
        current_player = data.get('current_player', 'white')
        mode = data.get('mode', 'ai')
        difficulty = data.get('difficulty', 2)
        
        # Create game instance
        game = ChessGame()
        game.set_board(board)
        game.current_player = current_player
        
        # Validate and make move
        if game.is_valid_move(from_row, from_col, to_row, to_col):
            move_notation = game.get_move_notation(from_row, from_col, to_row, to_col)
            game.make_move(from_row, from_col, to_row, to_col)
            
            response_data = {
                'valid': True,
                'board': game.get_board(),
                'game_state': game.game_state,
                'move_notation': move_notation,
                'current_player': game.current_player
            }
            
            # If AI mode and game is still playing, get AI move
            if mode == 'ai' and game.game_state == 'playing':
                ai = ChessAI(difficulty)
                ai_move = ai.get_best_move(game)
                
                if ai_move:
                    ai_from_row, ai_from_col, ai_to_row, ai_to_col = ai_move
                    ai_notation = game.get_move_notation(ai_from_row, ai_from_col, ai_to_row, ai_to_col)
                    game.make_move(ai_from_row, ai_from_col, ai_to_row, ai_to_col)
                    
                    response_data.update({
                        'ai_move': ai_move,
                        'ai_board': game.get_board(),
                        'ai_game_state': game.game_state,
                        'ai_move_notation': ai_notation
                    })
            
            return jsonify(response_data)
        else:
            return jsonify({
                'valid': False,
                'message': 'Invalid move'
            })
    
    except Exception as e:
        return jsonify({'valid': False, 'error': str(e)}), 500

@app.route('/move/checkers', methods=['POST'])
def make_checkers_move():
    """Make a checkers move"""
    try:
        data = request.get_json()
        board = data.get('board')
        from_row = data.get('from_row')
        from_col = data.get('from_col')
        to_row = data.get('to_row')
        to_col = data.get('to_col')
        current_player = data.get('current_player', 'white')
        mode = data.get('mode', 'ai')
        difficulty = data.get('difficulty', 2)
        
        # Create game instance
        game = CheckersGame()
        game.set_board(board)
        game.current_player = current_player
        
        # Validate and make move
        if game.is_valid_move(from_row, from_col, to_row, to_col):
            move_notation = f"{chr(97+from_col)}{8-from_row}-{chr(97+to_col)}{8-to_row}"
            game.make_move(from_row, from_col, to_row, to_col)
            
            response_data = {
                'valid': True,
                'board': game.get_board(),
                'game_state': game.game_state,
                'move_notation': move_notation,
                'current_player': game.current_player
            }
            
            # If AI mode and game is still playing, get AI move
            if mode == 'ai' and game.game_state == 'playing':
                ai = CheckersAI(difficulty)
                ai_move = ai.get_best_move(game)
                
                if ai_move:
                    ai_from_row, ai_from_col, ai_to_row, ai_to_col = ai_move
                    ai_notation = f"{chr(97+ai_from_col)}{8-ai_from_row}-{chr(97+ai_to_col)}{8-ai_to_row}"
                    game.make_move(ai_from_row, ai_from_col, ai_to_row, ai_to_col)
                    
                    response_data.update({
                        'ai_move': ai_move,
                        'ai_board': game.get_board(),
                        'ai_game_state': game.game_state,
                        'ai_move_notation': ai_notation
                    })
            
            return jsonify(response_data)
        else:
            return jsonify({
                'valid': False,
                'message': 'Invalid move'
            })
    
    except Exception as e:
        return jsonify({'valid': False, 'error': str(e)}), 500

@app.route('/game_state/<game_id>', methods=['GET'])
def get_game_state(game_id):
    """Get current game state"""
    try:
        if game_id not in games:
            return jsonify({'success': False, 'error': 'Game not found'}), 404
        
        game_data = games[game_id]
        game = game_data['game']
        
        return jsonify({
            'success': True,
            'board': game.get_board(),
            'current_player': game.current_player,
            'game_state': game.game_state,
            'game_type': game_data['type']
        })
    
    except Exception as e:
        return jsonify({'success': False, 'error': str(e)}), 500

@app.route('/health', methods=['GET'])
def health_check():
    """Health check endpoint"""
    return jsonify({'status': 'healthy', 'message': 'Chess & Checkers API is running'})

if __name__ == '__main__':
    print("Starting Chess & Checkers API server...")
    print("Visit http://localhost:5000/health to check if the server is running")
    app.run(debug=True, host='0.0.0.0', port=5000)
