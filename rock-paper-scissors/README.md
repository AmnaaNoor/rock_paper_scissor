# Rock Paper Scissors Game

A beginner-friendly desktop game built with Python and Tkinter. Two players take turns choosing Rock, Paper, or Scissors. The game keeps score for Player 1, Player 2, and draws.

## Features

- Two-player game mode
- Simple Tkinter GUI
- Score tracking for Player 1, Player 2, and draws
- Reset button to restart the game
- Quit button to close the application
- Ready to package into a Windows executable with PyInstaller

## Project Structure

```text
rock-paper-scissors/
├── main.py
├── logo.ico
├── window_icon.png
├── requirements.txt
├── README.md
├── .gitignore
└── .venv/   # created locally when you set up the environment
```

## Run the game

1. Open the project folder in VS Code.
2. Open the terminal.
3. Create a virtual environment:

```powershell
python -m venv .venv
```

4. Activate the environment:

```powershell
.\.venv\Scripts\Activate.ps1
```

If PowerShell blocks activation, run Python directly from the virtual environment:

```powershell
.\.venv\Scripts\python.exe main.py
```

5. Start the game:

```powershell
python main.py
```

## Build an executable with PyInstaller

1. Activate the virtual environment.
2. Install PyInstaller:

```powershell
python -m pip install pyinstaller
```

3. Build the application from the project directory. The spec bundles `window_icon.png` for the Tkinter window and uses `logo.ico` for the Windows executable:

```powershell
python -m PyInstaller --clean RockPaperScissors.spec
```

The executable is created in the `dist` folder:

```text
dist\RockPaperScissors.exe
```

## Game rules

- Rock beats Scissors
- Paper beats Rock
- Scissors beats Paper
- If both choices are the same, it is a draw
- Player 1 chooses first, then Player 2 chooses

## Notes

- The supplied `game logo.png` is JPEG-encoded, so `window_icon.png` is a PNG conversion of the same image for Tkinter. The original image remains unchanged.
- Tkinter is part of the Python standard library in a normal Windows Python install.
- You do not need to install Tkinter separately.
- The project does not require internet access after setup.
