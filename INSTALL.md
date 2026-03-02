# Zanthor Installation Guide

Zanthor is a game built with Python and Pygame where you play an evil robot castle. 

## Requirements
- **Python 3.6 or higher** (Python 3.12+ recommended)
- **Pygame** (or `pygame-ce`, which is recommended for modern Python versions)

---

## 🚀 Running from Source (Recommended)

Follow these steps to run the game directly from the downloaded source code without installing it permanently to your system.

### 1. Extract the Game Files
If you downloaded a `.zip` file, extract it to a folder of your choice. Open your terminal or command prompt and navigate to that folder:
```bash
cd path/to/zanthor
```

### 2. Install Dependencies
The game requires the `pygame` library. On modern versions of Python, it is highly recommended to install Pygame Community Edition (`pygame-ce`), as it provides pre-built wheels and avoids compilation errors.

```bash
python -m pip install pygame-ce
```
*(Note: If you are on Linux/macOS and `python` defaults to Python 2, use `python3 -m pip install pygame-ce` instead).*

### 3. Run the Game
Once the installation finishes, you can start the game right away:

```bash
python run_game.py
```

---

## 📦 System-wide Installation (Optional)

If you prefer to install Zanthor so you can launch it from anywhere on your computer using the `zanthor` command:

### 1. Navigate to the Source Folder
```bash
cd path/to/zanthor
```

### 2. Install using pip
Run the following command to install the project and its dependencies:

```bash
python -m pip install .
```

*Troubleshooting note:* The `setup.py` explicitly demands `pygame`. If this fails on your system due to missing build tools for older pygame versions, install `pygame-ce` first (`pip install pygame-ce`) and try again, or just use the **Running from Source** method above.

### 3. Launch from Anywhere
After a successful installation, you can launch the game from any terminal window simply by typing:
```bash
zanthor
```

---

## 🎮 Controls

### Keyboard
- **Move**: Arrow keys or `W`, `A`, `S`, `D`
- **Fire**: `F`, `Space`, or `Ctrl`
- **Pause**: `F10`

### Mouse
- **Fire**: Left Button (Button 1)
- **Move**: Right Button (Button 2)

### Gamepad / Joystick
- **Move**: D-Pad or Analog Stick
- **Fire**: Button 1
