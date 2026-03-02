# Module Reference

Detailed documentation for each module in Zanthor.

## Core Modules

### main.py

Entry point and game initialization.

**Classes:**

```python
class Game(engine.Game):
    """Main game controller."""
    
    def init(self):
        """Initialize timer, sound manager, and game data."""
        
    def tick(self):
        """Called each frame. Updates timers and sound."""
        
    def data_reset(self):
        """Reset game data for new game."""
        
    def event(self, e):
        """Handle global events (quit, Android pause)."""
```

**Functions:**

```python
def main():
    """Parse command-line args and start game."""
    
def do_main(no_intro=0, the_level=0):
    """Initialize pygame and run game loop."""
```

---

### const.py

Game constants and configuration.

**Screen Configuration:**
- `SW, SH` - Screen width/height (default 640x480)
- `FPS` - Target frame rate (default 30)
- `BSW, BSH` - Base size for scaling (640x480)
- `DX, DY` - Scale factors

**UI Rectangles:**
- `S_VIEW` - Game view area
- `S_STATUS` - Left status panel
- `S_HEALTH`, `S_COAL`, `S_WATER`, `S_STEAM` - Stat bar positions
- `S_ROBOT` - Castle illustration area
- `S_ITEMS` - Equipment display area
- `S_BUTTONS` - Button area
- `S_MESSAGES` - Message display area

**Gameplay Constants:**
- `MIN_CANNON_PRESSURE` - Minimum pressure to fire
- `JOY_FIRE_BUTTON`, `JOY_PICKUP_BUTTON` - Joystick button mappings
- `AUTO_PICKUP` - Auto-pickup items (default 1)
- `HOLES_ARE_TILES` - Ground holes become solid (0/1/2)
- `DISABLE_MOUSE_LOOK` - Disable mouse viewport control
- `FLOCKING_FLUCT` - Flocking fluctuation

**Functions:**
```python
def data_dir(*args):
    """Get path to data directory."""
    
def multr(dx_dy, r):
    """Scale rectangle by display ratio."""
    
def get_mouse_info():
    """Get mouse scroll configuration."""
```

---

### level.py

Level loading and main gameplay state.

**Class: Level**

```python
class Level:
    def __init__(self, game, _round, perc, music):
        """
        Initialize level.
        
        Args:
            game: Game instance
            _round: Level filename or index
            perc: Percentage of peasants to kill
            music: Background music filename
        """
        
    def init(self):
        """Called when level becomes active."""
        
    def paint(self, screen):
        """Render the level."""
        
    def update(self, screen):
        """Update and render."""
        
    def loop(self):
        """Game logic. Returns next state if level complete."""
        
    def event(self, e):
        """Handle input events."""
```

**Key Attributes:**
- `tv` - Isovid renderer instance
- `interface` - Interface instance
- `round` - Current level
- `percent` - Win percentage

---

### castle.py

Player castle entity.

**Class: CastleSprite(isovid.Sprite)**

```python
class CastleSprite(isovid.Sprite):
    """Player-controlled castle."""
    
    def __init__(self, *args, **kwargs):
        """Initialize castle with unit stats."""
        
    def no_move(self):
        """Disable movement."""
        
    def yes_move(self):
        """Enable movement."""
        
    def yes_pickup(self, e):
        """Accept item pickup."""
        
    def no_pickup(self, e):
        """Decline item pickup."""
        
    def check_for_pickup(self, g, t):
        """Check if tile has item to pickup."""
        
    def upgrade_something(self, upgrade_what):
        """Apply upgrade to castle."""
        
    def event(self, g, e):
        """Handle castle-specific input."""
        
    def reset_castle(self):
        """Reset stats from backup."""
        
    def backup_castle(self):
        """Save current stats."""
```

**Functions:**

```python
def castle_new(g, t, value):
    """Spawn castle at tile."""
    
def castle_hit(g, s, a):
    """Handle castle hitting something."""
    
def castle_loop(g, s):
    """Per-frame castle update."""
    
def cball_new(g, pos, dest, damage=1.0, pressure=16):
    """Create cannonball projectile."""
    
def cball_loop(g, s):
    """Per-frame cannonball update."""
    
def cball_hit(g, a, b):
    """Handle cannonball collision."""
```

---

### units.py

Unit stats and behavior.

**Upgrade Configuration:**

```python
upgrade_amounts = {
    'UpEngine Efficiency': cyclic_list([1.0, 2.0, ...]),
    'UpEngine Speed': cyclic_list([...]),
    'UpCannon Balls': cyclic_list([...]),
    'UpArmour': cyclic_list([...]),
    'UpSteam Tank': cyclic_list([...]),
    'UpWater Tank': cyclic_list([...]),
    'UpCoal Tank': cyclic_list([...]),
    'UpCannon Power': cyclic_list([...]),
}

upgrade_words = [
    'UpEngine Efficiency',
    'UpEngine Speed',
    'UpCannon Balls',
    'UpCannon Power',
    'UpArmour',
    'UpSteam Tank',
    'UpWater Tank',
    'UpCoal Tank',
]
```

**Class: BaseUnit**

```python
class BaseUnit:
    """Base class for all units."""
    
    def __init__(self):
        """Initialize with default stats."""
        
    def pickup_item(self, item):
        """Add item to inventory. Returns 1 if successful."""
        
    def hit(self, damage_amount):
        """Take damage. Returns 1 if dead."""
        
    def try_move(self):
        """Attempt movement. Returns 1 if enough steam."""
        
    def try_fire(self):
        """Attempt to fire. Returns 1 if enough steam."""
        
    def prep_fire(self):
        """Start charging cannon."""
        
    def try_do_fire(self):
        """Fire cannon. Returns pressure used."""
        
    def try_use_steam(self, amount):
        """Use steam. Returns 1 if successful."""
        
    def loop(self):
        """Per-frame update (generate steam)."""
        
    def generate_steam(self):
        """Convert coal+water to steam."""
        
    def upgrade_part(self, part_up, amount):
        """Apply upgrade to unit stats."""
```

**Unit Classes:**
- `Castle(BaseUnit)` - Player castle
- `Robot(BaseUnit)` - Peasant enemy
- `CannonTower(BaseUnit)` - Enemy turret
- `CoalTruck(BaseUnit)` - Resource transport
- `Factory(BaseUnit)` - Enemy building

---

### items.py

Collectible items.

**Item Types (bitmask):**
```python
ITEM_COAL = 0x0001
ITEM_WATER = 0x0002
ITEM_PART = 0x0010
ITEM_CANNON = 0x0020
ITEM_ENGINE = 0x0030
ITEM_WATERTANK = 0x0040
ITEM_COALSTORAGEROOM = 0x0050
ITEM_ARMOUR = 0x0060
ITEM_RUBBLE = 0x0100
```

**Item Classes:**

```python
class Coal:
    type = ITEM_COAL
    def __init__(self, amount=1.0)
    
class Water:
    type = ITEM_WATER
    def __init__(self, amount=1.0)
    
class Part:
    type = ITEM_PART
    def __init__(self, name, pickup_string)
    
class Rubble:
    type = ITEM_RUBBLE
    
class Cannon, Engine, WaterTank, CoalStorageRoom, Armour:
    # Additional item types
```

---

### robot.py

Peasant AI.

**Configuration:**
```python
MIN = 8.0       # Minimum velocity
MAX = 16.0      # Maximum velocity
RADIUS = 32.0   # Separation radius
CENTER = 4.0    # Centering strength
SEARCH = 128.0  # Search radius
```

**Functions:**

```python
def robot_new(g, t, v):
    """Spawn peasant at tile."""
    
def robot_loop(g, s):
    """Per-frame peasant update."""
    
def robot_shove(g, s, (x, y)):
    """Push peasant to position."""
    
def robot_hit(g, a, b):
    """Handle peasant collision."""
```

---

### flock.py

Flocking behavior system.

**Class: Part**
```python
class Part:
    """Individual flocking entity."""
    x, y      # Position
    _x, _y    # Previous position
    min       # Minimum velocity
    max       # Maximum velocity
    radius    # Separation radius
    center    # Centering strength
    near      # List of nearby parts
```

**Class: Flock**
```python
class Flock:
    def __init__(self, rect, spacing):
        """
        Create flock with spatial grid.
        
        Args:
            rect: Bounding rectangle
            spacing: Grid cell size
        """
        
    def append(self, p):
        """Add entity to flock."""
        
    def remove(self, p):
        """Remove entity from flock."""
        
    def loop(self):
        """Update all entities each frame."""
```

**Flocking Algorithm:**
1. Update spatial grid positions
2. Calculate velocities from previous frame
3. Find neighbors using spatial grid
4. Add average velocity (alignment)
5. Move toward center (cohesion)
6. Enforce minimum velocity (random movement if stuck)
7. Separate from neighbors (separation)
8. Enforce maximum velocity

---

## State Modules

### states.py

Game state classes.

```python
class SPause(engine.State):
    """Simple pause state."""
    
class GameOver(engine.State):
    """Game over screen."""
    
class NextLevel(engine.State):
    """Level complete - upgrade screen."""
    
class GameWon(engine.State):
    """Victory screen."""
    
class News(engine.State):
    """News popup."""
    
class Pause(engine.State):
    """Pause with help text."""
    
class Prompt(engine.State):
    """Yes/no prompt."""
```

---

### intro.py

Intro sequence.

```python
class Intro(engine.State):
    """Animated intro sequence."""
    
    # Timing data for text display
    data = [
        (0, "you", 0, 64),
        (8, "are", 90, 64),
        (16, "Zanthor", 128, 144),
        ...
    ]
```

---

### title.py

Title screen and menus.

```python
class Title(engine.State):
    """Main title screen with menu."""
    
class Help(engine.State):
    """Help screen."""
    
class Credits(engine.State):
    """Credits screen."""
```

---

### menu.py

Level selection screen.

```python
# Level data: (lock, rect, title, pop, filename, percent, ztitle, music, selected)
data = [
    (7, pygame.Rect(...), "Comfy Castle", 4397, "level8.tga", 70, ...),
    ...
]

class Menu(engine.State):
    """Level selection map."""
    
    def find_select_place(self, tobe):
        """Check if position is valid level."""
        
    def set_selected_parts(self, tobe):
        """Update selection with bounds checking."""
```

---

## Effect Modules

### effect.py

Effect system.

```python
def effect_new(g, rect, e, f):
    """
    Create sprite with effect.
    
    Args:
        g: Game instance
        rect: Position
        e: Effect object
        f: Frame count (< 1 for infinite)
    """
    
def effect_loop(g, s):
    """Per-frame effect update."""
```

---

### steam.py

Steam particle effect.

```python
class Part:
    """Single steam particle."""
    pos     # Current position
    _pos    # Previous position
    frame   # Age in frames
    z       # Z-order

class Effect:
    def __init__(self, total, add, region=1, respawn=1, color=(255,255,255)):
        """
        Args:
            total: Maximum particles
            add: Particles to add per frame
            region: Spawn radius
            respawn: Whether particles respawn
            color: Particle color
        """
        
    def loop(self, pos):
        """Update particles."""
        
    def paint(self, screen, origin):
        """Render particles."""
        
    def zloop(self, pos, z):
        """Update with z-ordering."""
        
    def zpaint(self):
        """Return z-sorted render data."""
```

---

### explode.py

Explosion particle effect. Similar structure to steam.py with different particle behavior.

---

## UI Modules

### interface.py

HUD and status display.

```python
class StatsDraw:
    """Draws stat bars (health, coal, water, steam)."""
    
    def draw_img(self, screen, min, max, current, color, where_rect, astat):
        """Draw stat as image (for health)."""
        
    def draw_rect(self, screen, min, max, current, color, where_rect):
        """Draw stat as filled rectangle."""
        
    def update_stats(self, screen, stats, robots, max_robots):
        """Update all stat displays."""

class Interface:
    """Main HUD controller."""
    
    def __init__(self):
        """Initialize fonts and message system."""
        
    def load(self):
        """Load UI graphics."""
        
    def event(self, g, e):
        """Handle UI events."""
        
    def new_random_message(self):
        """Generate new Zanthor message."""
        
    def new_upgrade_message(self, upgrade_what):
        """Show upgrade confirmation."""
        
    def new_equipment(self, stats):
        """Update equipment display."""
        
    def update(self, tv, screen):
        """Render all UI elements. Returns dirty rects."""
```

---

### messages.py

Procedural message generator.

```python
# Grammar definition
data = {
    'SENTENCE': ['[_SENTENCE]'],
    '_SENTENCE': ['[NAME] [WILL] [KILL] [HUMANS].', ...],
    'NAME': ['[_NAME]', '[_NAME] the [GREAT]', ...],
    # ... more grammar rules
}

def generate():
    """Generate random message using grammar."""
    
def generate_upgrade_message(upgrade_what):
    """Generate upgrade confirmation message."""
```

---

## Audio Modules

### sounds.py

Sound management.

```python
class SoundManager:
    def __init__(self, sound_list, sound_path, extensions):
        """Initialize sound system."""
        
    def Load(self, sound_list=[]):
        """Load sounds into memory."""
        
    def GetSound(self, name):
        """Get Sound object by name."""
        
    def Play(self, name, volume=[1.0, 1.0], wait=0, loop=0):
        """
        Play sound.
        
        wait modes:
            0 - Play immediately
            1 - Queue if playing
            2 - Skip if playing
            3 - No queue
        """
        
    def Stop(self, name):
        """Stop sound."""
        
    def StopAll(self):
        """Stop all sounds."""
        
    def Update(self, elapsed_time):
        """Process queued sounds."""
        
    def PlayMusic(self, musicname):
        """Play background music."""
        
    def PauseMusic(self):
    def UnPauseMusic(self):

class ChannelFader:
    """Fade audio channel in/out."""
    
    def fade_in(self, seconds, volume_to):
    def fade_out(self, seconds, volume_to):
    def Update(self, elapsed_time):
```

---

### sound_info.py

Sound definitions.

```python
cannon = cl(['cannon', 'cannon2', 'cannon3', ...])
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

def get_upgrade_sound(upgrade_what):
    """Get sound for upgrade type."""
```

---

## Engine Modules

### isovid.py

Isometric renderer.

```python
class Isovid(Vid):
    """Isometric tile engine."""
    
    def paint(self, screen):
        """Render isometric view."""
        
    def bkgr_blit(self, img, pos):
        """Blit to background at iso position."""
        
    def iso_to_view(self, pos):
        """Convert iso to view coordinates."""
        
    def view_to_iso(self, pos):
        """Convert view to iso coordinates."""
        
    def tile_to_view(self, pos):
        """Convert tile to view coordinates."""
        
    def screen_to_tile(self, pos):
        """Convert screen to tile coordinates."""
        
    def tga_load_tiles(self, fname, size, tdata={}):
        """Load tiles from TGA image."""
        
    def tga_load_level(self, fname, bg=0):
        """Load level from TGA image."""
        
    def set(self, pos, v):
        """Set tile and update pathfinding layers."""
```

---

### algo.py

A* pathfinding.

```python
def astar(start, end, layer, dist_func):
    """
    Find path from start to end.
    
    Args:
        start: (x, y) start position
        end: (x, y) end position
        layer: 2D array (0=walkable, 1=blocked)
        dist_func: Heuristic function
        
    Returns:
        List of (x, y) positions or empty list
    """
```

---

### cyclic_list.py

Utility data structure.

```python
class cyclic_list:
    """List that cycles through elements."""
    
    def __init__(self, items):
        """Initialize with item list."""
        
    def cur(self):
        """Get current item."""
        
    def nextone(self):
        """Get next item and advance."""
        
    def __next__(self):
        """Advance to next item."""
```

---

### tiles.py

Tile interaction handlers.

```python
def tile_block(g, t, s):
    """Handle solid tile collision."""
    
def tile_wall(g, t, s):
    """Handle wall hit (destructible)."""
    
def tile_coal(g, t, s):
    """Handle coal pickup."""
    
def tile_water(g, t, s):
    """Handle water pickup."""
    
def tile_rubble(g, t, s):
    """Handle rubble pickup."""
    
def tile_part(g, t, s):
    """Handle upgrade part pickup."""
    
def tile_limit(g, t, s):
    """Handle out-of-bounds (remove sprite)."""
```

---

## PGU Library (pgu/)

Phil's Game Utilities - embedded game framework.

### pgu/engine.py

State machine engine.

```python
class State:
    """Base state class."""
    
    def init(self): pass
    def paint(self, screen): pass
    def update(self, screen): pass
    def loop(self): pass
    def event(self, e): pass

class Game:
    """Game controller."""
    
    def run(self, state, screen):
        """Run game loop with initial state."""

class Quit(State):
    """Quit signal state."""
```

### pgu/vid.py

Base tile video engine.

```python
class Tile:
    """Single tile type."""
    image, image_h
    agroups, hit
    config
    
class Sprite:
    """Game entity."""
    image, rect, shape
    groups, agroups
    loop, hit

class Vid:
    """Tile-based video engine."""
    
    tiles       # List of Tile objects
    sprites     # List of Sprite objects
    tlayer      # Foreground tile layer
    blayer      # Background tile layer
    clayer      # Code layer
    
    def resize(self, size, bg=0)
    def set(self, pos, v)
    def get(self, pos)
    def paint(self, screen)
    def loop(self)
```

### pgu/timer.py

Timing utilities.

```python
class Timer:
    """Frame rate limiter."""
    
    def tick(self):
        """Limit frame rate."""

class Speedometer:
    """FPS counter."""
    
    def tick(self):
        """Returns FPS every second."""
```

### pgu/gui/

GUI widget system (tables, buttons, input, etc.).
