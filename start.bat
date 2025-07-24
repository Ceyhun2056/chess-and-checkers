@echo off
echo Starting Chess & Checkers Game...
echo.

echo Installing Python dependencies...
cd backend
pip install -r requirements.txt

echo.
echo Starting Flask server...
echo The game will be available at:
echo Frontend: Open frontend/index.html in your browser
echo Backend API: http://localhost:5000
echo.

python app.py
