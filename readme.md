# Snake Game 🐍

A two-player arcade Snake game made using Python and Pygame.

## Files
- `snake.py` — Single player mode
- `arcade_snake.py` — Two player arcade mode

## Features
- Two player multiplayer on the same keyboard
- Grid-based snake movement
- Wall collision (death on boundary)
- Food spawning (shared between both players)
- Score tracking for both players
- Start menu screen
- Game over screen with winner announcement
- Restart option after game over

## Controls

### Player 1
- Arrow Keys → Move Snake

### Player 2
- W A S D → Move Snake

### General
- Enter → Start Game
- R → Restart after Game Over

## Requirements
- Python 3.10+
- Pygame CE

Install dependencies:
```bash
pip install -r requirements.txt
```

## Run the Game

Single player:
```bash
python snake.py
```

Two player arcade:
```bash
python arcade_snake.py
```

## Build Executable

Using PyInstaller:

```bash
pyinstaller --onefile --windowed arcade_snake.py
```

The executable will be created inside:

```text
dist/
```

## Technologies Used
- Python
- Pygame CE

## Author
Made by Lakshya Sharma