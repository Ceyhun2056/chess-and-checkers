# Chess & Checkers

A complete web-based implementation of two classic board games - Chess and Checkers - with AI opponents and multiplayer support.

## 🎮 Features

- **Two Classic Games**: Play both Chess and Checkers in one application
- **Multiple Game Modes**: 
  - Player vs AI (with adjustable difficulty)
  - Player vs Player (local multiplayer)
- **Smart AI Opponents**:
  - Chess AI using Minimax algorithm with position evaluation
  - Checkers AI with capture prioritization and strategic positioning
- **Professional UI**: Clean, responsive design with smooth animations
- **Move Validation**: Complete rule enforcement for both games
- **Game Features**:
  - Move history tracking
  - Score keeping
  - Game state detection (check, checkmate, stalemate)
  - Possible move highlighting
  - Piece promotion (Chess)
  - King promotion (Checkers)

## 🏗️ Architecture

### Frontend (HTML/CSS/JavaScript)
- Responsive grid-based board layout
- Interactive piece movement with drag-and-drop feel
- Real-time game state updates
- Modern CSS with animations and transitions

### Backend (Python/Flask)
- RESTful API for game logic
- Separate AI engines for Chess and Checkers
- Move validation and game state management
- CORS enabled for cross-origin requests

## 📁 Project Structure

```
chess-and-checkers/
├── frontend/
│   ├── index.html          # Main game interface
│   ├── style.css           # Responsive styling
│   └── script.js           # Game logic and API communication
├── backend/
│   ├── app.py              # Flask API server
│   ├── chess_ai.py         # Chess game logic and AI
│   ├── checkers_ai.py      # Checkers game logic and AI
│   └── requirements.txt    # Python dependencies
└── README.md
```

## 🚀 Getting Started

### Prerequisites
- Python 3.7+
- Modern web browser
- Internet connection for initial setup

### Installation

1. **Clone the repository**
   ```bash
   git clone https://github.com/Ceyhun2056/chess-and-checkers.git
   cd chess-and-checkers
   ```

2. **Set up the backend**
   ```bash
   cd backend
   pip install -r requirements.txt
   ```

3. **Start the Flask server**
   ```bash
   python app.py
   ```
   The API will be available at `http://localhost:5000`

4. **Open the frontend**
   - Open `frontend/index.html` in your web browser
   - Or serve it using a local web server:
     ```bash
     cd frontend
     python -m http.server 8080
     ```
   - Then visit `http://localhost:8080`

## 🎯 How to Play

### Chess
- Click on a piece to select it and see possible moves
- Click on a highlighted square to move
- The AI will respond automatically in AI mode
- Special rules implemented: castling, en passant, pawn promotion

### Checkers
- Click on a checker to select it
- Move diagonally to adjacent dark squares
- Jump over enemy pieces to capture them
- Reach the opposite end to promote to a king
- Multiple jumps are enforced when available

## 🤖 AI Difficulty Levels

### Easy (Level 1)
- Random moves with slight preference for captures
- Suitable for beginners

### Medium (Level 2)
- Minimax algorithm with 2-depth search (Chess) / 4-depth (Checkers)
- Basic position evaluation
- Good challenge for intermediate players

### Hard (Level 3)
- Deeper search with 3-depth (Chess) / 6-depth (Checkers)
- Advanced position evaluation
- Challenging for experienced players

## 🔧 API Endpoints

- `POST /new_game` - Initialize a new game
- `POST /possible_moves` - Get possible moves for a piece
- `POST /move/chess` - Make a chess move
- `POST /move/checkers` - Make a checkers move
- `GET /health` - Health check

## 🎨 Customization

The game supports easy customization:

- **Styling**: Modify `frontend/style.css` for visual changes
- **AI Behavior**: Adjust evaluation functions in `chess_ai.py` and `checkers_ai.py`
- **Game Rules**: Extend game logic in the respective AI files
- **UI Features**: Add new functionality in `frontend/script.js`

## 🔄 Game Flow

1. **Game Selection**: Choose between Chess and Checkers
2. **Mode Selection**: Pick Player vs AI or Player vs Player
3. **Difficulty**: Set AI difficulty (if applicable)
4. **Gameplay**: Make moves by clicking pieces and destinations
5. **AI Response**: AI calculates and makes its move (if in AI mode)
6. **Game End**: Detect and announce win/draw conditions

## 🧠 Technical Details

### Chess AI Implementation
- Material evaluation (piece values)
- Positional evaluation (piece-square tables)
- Minimax with alpha-beta pruning
- Check/checkmate detection
- Special move handling

### Checkers AI Implementation
- Piece counting and positioning
- Capture prioritization
- King promotion bonuses
- Mobility evaluation
- Forced capture rules

## 🐛 Troubleshooting

### Common Issues

1. **CORS Errors**: Ensure the Flask server is running and CORS is enabled
2. **API Connection**: Check that the backend is accessible at `http://localhost:5000`
3. **Move Validation**: The game enforces strict rules - invalid moves will be rejected
4. **Browser Compatibility**: Use a modern browser with JavaScript enabled

### Performance Tips

- The AI may take a few seconds to calculate moves on higher difficulties
- Reduce AI difficulty for faster gameplay
- Ensure stable internet connection for API calls

## 🤝 Contributing

1. Fork the repository
2. Create a feature branch (`git checkout -b feature/amazing-feature`)
3. Commit your changes (`git commit -m 'Add some amazing feature'`)
4. Push to the branch (`git push origin feature/amazing-feature`)
5. Open a Pull Request

## 📝 License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## 🙏 Acknowledgments

- Chess piece symbols from Unicode standard
- Minimax algorithm implementation inspired by classic game AI literature
- Responsive design principles for modern web development

## 📧 Contact

For questions, suggestions, or bug reports, please open an issue on GitHub.

---

**Enjoy playing Chess and Checkers!** 🎯♟️