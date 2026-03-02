# Getting Started

This guide covers installation and running Zanthor.

## System Requirements

- **Python**: 3.6 or higher (Python 3.12+ recommended)
- **Pygame**: pygame or pygame-ce library
- **Operating System**: Windows, macOS, or Linux
- **Display**: 640x480 minimum resolution

## Installation Methods

### Method 1: Running from Source (Recommended)

1. **Extract or clone the game files**:
   ```bash
   cd path/to/zanthor
   ```

2. **Install pygame dependency**:
   ```bash
   python -m pip install pygame-ce
   ```
   
   > Note: `pygame-ce` (Pygame Community Edition) is recommended for modern Python versions as it provides pre-built wheels.

3. **Run the game**:
   ```bash
   python run_game.py
   ```

### Method 2: System-wide Installation

1. **Navigate to source folder**:
   ```bash
   cd path/to/zanthor
   ```

2. **Install using pip**:
   ```bash
   python -m pip install .
   ```

3. **Run from anywhere**:
   ```bash
   zanthor
   ```

## Command-Line Options

The game supports several command-line arguments:

| Argument | Description |
|----------|-------------|
| `fullscreen` or `full` | Launch in fullscreen mode |
| `nointro` or `no` | Skip intro sequence, go directly to menu |
| `speed` | Unlock frame rate (for testing) |
| `profile` | Run with profiling enabled |
| `l <number>` | Jump to specific level by index |
| `level<N>.tga` | Jump to specific level by filename |

### Examples

```bash
# Fullscreen mode
python run_game.py fullscreen

# Skip intro
python run_game.py nointro

# Jump to level 5
python run_game.py l 5

# Fullscreen without intro
python run_game.py full no
```

## Troubleshooting

### No Sound
- Ensure pygame.mixer is initialized properly
- Check system audio settings
- The game will run without sound if mixer fails to initialize

### Display Issues
- Default resolution is 640x480
- Try windowed mode if fullscreen causes problems
- Resolution can be modified in `const.py`

### Controller Not Working
- Ensure joystick is connected before starting the game
- The game initializes all connected joysticks on startup

### Import Errors
- Ensure pygame or pygame-ce is installed
- For pygame-ce: `pip install pygame-ce`
- For original pygame: `pip install pygame`

## Verifying Installation

After installation, you should see:
1. The intro sequence with "You are Zanthor" text
2. The title screen with animated Zanthor logo
3. The level select screen showing the Sunflower Kingdom

If any of these don't appear, check the console for error messages.

## Next Steps

- See [Gameplay Guide](gameplay_guide.md) for how to play
- See [Configuration](configuration.md) for tweaking game settings
