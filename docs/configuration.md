# Game Configuration

This document describes configurable parameters in Zanthor.

## Screen Settings

Location: `zanthor/const.py`

```python
# Base screen dimensions (for scaling calculations)
BSW, BSH = 640, 480

# Actual screen dimensions
SW, SH = 640, 480  # Default resolution

# Derived scale factors
DX = float(SW) / BSW
DY = float(SH) / BSH
```

### Changing Resolution

To change resolution, modify `SW` and `SH`:

```python
SW, SH = 800, 600   # 800x600
SW, SH = 1024, 768  # 1024x768
SW, SH = 1280, 800  # 1280x800
```

Note: UI elements scale automatically based on `DX` and `DY`.

### Fullscreen Mode

Launch with command line:
```bash
python run_game.py fullscreen
```

Or modify in `main.py`:
```python
flags = FULLSCREEN  # Instead of flags = 0
```

## Performance Settings

### Frame Rate

```python
FPS = 30  # Target frames per second
```

Higher values increase smoothness but CPU usage.

### Background Caching

```python
CACHE_USE_LEVEL_CACHE = 1  # Enable background caching
CACHE_CHECK_TILES = 1      # Check tile modification time
CACHE_CHECK_LEVEL = 1      # Check level modification time
```

When enabled, pre-rendered backgrounds are saved to `data/cache/levels/` to speed up level loading.

## Gameplay Settings

### Cannon

```python
MIN_CANNON_PRESSURE = 6  # Minimum pressure required to fire
```

### Pickup Behavior

```python
AUTO_PICKUP = 1  # 1 = auto pickup items, 0 = prompt for pickup
```

### Ground Holes

```python
HOLES_ARE_TILES = 0
# 0 = holes are visual only
# 1 = holes become solid tiles
# 2 = large holes become solid
```

### Mouse Look

```python
DISABLE_MOUSE_LOOK = 0  # 0 = enabled, 1 = disabled
```

Can be toggled in-game with `M` key.

Mouse look settings:
```python
def get_mouse_info():
    if DISABLE_MOUSE_LOOK:
        SCROLL_MOUSE = 0     # Speed of mouse scroll
        SCROLL_AUTO = 9      # Speed of auto-return
        SCROLL_BORDER = 70   # Scroll border size
    else:
        SCROLL_MOUSE = 12
        SCROLL_AUTO = 9
        SCROLL_BORDER = 160
```

### Flocking

```python
FLOCKING_FLUCT = 1  # Enable flocking fluctuation
```

Robot flocking parameters in `robot.py`:
```python
MIN = 8.0          # Minimum velocity
MIN_RAND = 4       # Min velocity randomization
MAX = 16.0         # Maximum velocity
MAX_RAND = 8       # Max velocity randomization
RADIUS = 32.0      # Separation radius
RADIUS_RAND = 12   # Radius randomization
CENTER = 4.0       # Centering strength
CENTER_RAND = 2    # Center randomization
SEARCH = 128.0     # Search radius
```

## Control Settings

### Joystick

```python
JOY_FIRE_BUTTON = 1    # Fire button index
JOY_PICKUP_BUTTON = 2  # Pickup button index
```

### Keyboard

Default controls are hardcoded in `castle.py`:
- Movement: Arrow keys, WASD
- Fire: F, Space, Ctrl
- Pause: H, P, Enter

## Unit Stats

### Castle Initial Stats

Location: `zanthor/units.py`, class `Castle`

```python
self.stats = {
    'Armour': 0.0,
    'Speed': 10.0,
    'Weight': 1.0,
    'Health': 10.0,
    'Water': 65.0,
    'Coal': 65.0,
    'Steam': 100.0,
    'EngineEfficiency': 3.0,
    'CannonPressure': 0.0,
    'MaxCannonPressure': 16.0,
    'MaxHealth': 10.0,
    'MaxWater': 70.0,
    'MaxCoal': 70.0,
    'MaxSteam': 100.0,
    'Temperature': 0.0,
    'Damage': 1.0,
    'WeaponSteam': 1.0,
    'MoveSteam': 0.05,
    'GenerateSteamCoal': 0.05,
    'GenerateSteamWater': 0.05,
}
```

### Upgrade Amounts

```python
upgrade_amounts = {}
u = upgrade_amounts
cl = cyclic_list.cyclic_list

# Each upgrade can be applied multiple times with increasing effect
u['UpEngine Efficiency'] = cl([1.0, 2.0, 2.0, 2.0, 2.0, 3.0, 3.0, ...])
u['UpEngine Speed'] = cl([1.0, 2.0, 2.0, 2.0, 2.0, 3.0, 3.0, ...])
u['UpCannon Balls'] = cl([1.0, 2.0, 2.0, 2.0, 2.0, 3.0, 3.0, ...])
u['UpArmour'] = cl([1.0, 2.0, 2.0, 2.0, 2.0, 3.0, 3.0, ...])
u['UpSteam Tank'] = cl([1.0, 2.0, 2.0, 2.0, 2.0, 3.0, 3.0, ...])
u['UpWater Tank'] = cl([1.0, 2.0, 2.0, 2.0, 2.0, 3.0, 3.0, ...])
u['UpCoal Tank'] = cl([1.0, 2.0, 2.0, 2.0, 2.0, 3.0, 3.0, ...])
u['UpCannon Power'] = cl([1.0, 2.0, 2.0, 2.0, 2.0, 3.0, 3.0, ...])
```

## Level Configuration

### Level Data

Location: `zanthor/menu.py`

```python
data = [
    # (lock, rect, title, population, filename, percent, ztitle, music, grid_pos)
    (7, pygame.Rect(...), 'Comfy Castle', 4397, 'level8.tga', 70, ...),
    (4, pygame.Rect(...), 'Truthful Tower', 1232, 'level5.tga', 70, ...),
    # ...
]
```

Fields:
- `lock` - Number of levels required to unlock (0 = always available)
- `rect` - Clickable area on map
- `title` - Display name
- `population` - Number of citizens (peasants)
- `filename` - Level file in `data/levels/`
- `percent` - Kill percentage required to win (70-80)
- `ztitle` - Zanthor's name for the location
- `music` - Background music file
- `grid_pos` - Selection grid position

### Tile Data

Location: `zanthor/level.py`

```python
tdata = {
    0x01: ('castle', tiles.tile_coal, None),
    0x02: ('castle', tiles.tile_water, None),
    0x04: ('cball', tiles.tile_wall, None),
    0x05: ('cball', tiles.tile_wall, None),
    0x06: ('cball', tiles.tile_wall, None),
    0x07: ('castle', tiles.tile_rubble, None),
    8: ('castle', tiles.tile_part, None),   # Engine Efficiency
    9: ('castle', tiles.tile_part, None),   # Engine Speed
    10: ('castle', tiles.tile_part, None),  # Cannon Balls
    11: ('castle', tiles.tile_part, None),  # Armour
    12: ('castle', tiles.tile_part, None),  # Steam Tank
    13: ('castle', tiles.tile_part, None),  # Water Tank
    14: ('castle', tiles.tile_part, None),  # Coal Tank
    15: ('castle', tiles.tile_part, None),  # Cannon Power
    0x1C: ('castle,cball,robot', tiles.tile_limit, None),  # Out of bounds
}
```

### Spawn Codes

```python
cdata = {
    1: (castle.castle_new, None),      # Castle spawn
    4: (factory.factory_new, None),    # Factory spawn
    5: (truck.truck_new, None),        # Truck spawn
    6: (cannon.cannon_new, None),      # Cannon spawn
    7: (robot.robot_new, None),        # Robot spawn
}
```

## Sound Configuration

### Sound Mappings

Location: `zanthor/sound_info.py`

```python
cannon = cl(['cannon', 'cannon2', 'cannon3', 'cannon', 'cannon'])
hitenemy = cl(['hitenemy'])
hitwall = cl(['hitwall2'])
hitground = cl(['hitground'])
destroyenemy = cl(['destroyenemy'])
ushit = cl(['ouch1', 'ouch2'])
coal = cl(['coal'])
water = cl(['water'])
birds = cl(['birds1', 'birds2', 'birds2'])
peasants = cl(['peasants1', 'peasants2', 'peasants3'])
squish = cl(['squish1', 'squish2'])
```

Sounds are located in `data/sounds/` as `.wav` or `.ogg` files.

### Audio Settings

Location: `zanthor/main.py`

```python
pygame.mixer.pre_init(22050, -16, 2, 1024)
# Sample rate: 22050
# Bit depth: -16 (16-bit signed)
# Channels: 2 (stereo)
# Buffer: 1024
```

## UI Rectangles

All UI positions are defined as rectangles in `const.py`:

```python
# Game view area
S_VIEW = multr(dxdy, (76, 0, 380, 340))

# Left status panel
S_STATUS = multr(dxdy, (0, 0, 76, 340))

# Stat bars
S_HEALTH = multr(dxdy, (10, 4, 60, 96))
S_COAL = multr(dxdy, (10, 100, 60, 70))
S_WATER = multr(dxdy, (10, 190, 60, 70))
S_STEAM = multr(dxdy, (10, 260, 60, 70))

# Cannon pressure
S_CANNON_PRESSURE = multr(dxdy, (76, 0, 5, 340))

# Peasants remaining
S_PEASANTS_REMAINING = multr(dxdy, (487, 24, 122, 114))

# Robot illustration
S_ROBOT = multr(dxdy, (456, 0, 184, 163))

# Equipment area
S_ITEMS = multr(dxdy, (456, 163, 184, 177))

# Button area
S_BUTTONS = pygame.Rect(470, 340, 170, 140)

# Message area
S_MESSAGES = multr(dxdy, (95, 365, 355, 110))
```

## Message Generator

Location: `zanthor/messages.py`

The message generator uses a context-free grammar:

```python
data = {
    'SENTENCE': ['[_SENTENCE]'],
    '_SENTENCE': [
        '[NAME] [WILL] [KILL] [HUMANS].',
        '[FEAR] [NAME].',
        # ... more patterns
    ],
    'NAME': ['[_NAME]', '[_NAME] the [GREAT]', ...],
    'GREAT': ['awesome', 'great', 'magnificent', ...],
    'KILL': ['kill', 'maim', 'destroy', ...],
    # ... more vocabulary
}
```

Add new patterns or vocabulary to customize messages.

## Debug Settings

### Upgrade Fun Mode

```python
UPGRADE_FUN = 1  # Enable number keys 1-8 for instant upgrades
```

### Tile Debug

In `tiles.py`:
```python
PRINTDEBUG = 0  # Set to 1 for tile interaction messages
```

### Profiling

Run with profiling:
```bash
python run_game.py profile
```

This uses Python's `hotshot` profiler to identify performance bottlenecks.
