# Architecture Overview

This document describes the technical architecture of Zanthor.

## High-Level Architecture

```
┌─────────────────────────────────────────────────────────────┐
│                        main.py                               │
│                    (Entry Point & Game Loop)                 │
├─────────────────────────────────────────────────────────────┤
│                                                              │
│  ┌─────────────┐  ┌─────────────┐  ┌─────────────────────┐  │
│  │   States    │  │    Level    │  │     Interface       │  │
│  │  (title,    │  │ (gameplay   │  │  (HUD, status bars, │  │
│  │   menu,     │  │  logic)     │  │   messages)         │  │
│  │   intro)    │  │             │  │                     │  │
│  └─────────────┘  └─────────────┘  └─────────────────────┘  │
│                                                              │
│  ┌─────────────┐  ┌─────────────┐  ┌─────────────────────┐  │
│  │   Castle    │  │   Units     │  │      Items          │  │
│  │ (player     │  │ (stats &    │  │  (coal, water,      │  │
│  │  entity)    │  │  behavior)  │  │   upgrades)         │  │
│  └─────────────┘  └─────────────┘  └─────────────────────┘  │
│                                                              │
├─────────────────────────────────────────────────────────────┤
│                        PGU Engine                            │
│        (isovid, engine, timer, gui, vid)                    │
├─────────────────────────────────────────────────────────────┤
│                         Pygame                               │
└─────────────────────────────────────────────────────────────┘
```

## Directory Structure

```
zanthor/
├── main.py              # Package entry point (main.main)
├── run_game.py          # Alternative entry point
├── setup.py             # Package installation
├── zanthor/
│   ├── __init__.py
│   ├── __main__.py      # Module entry point
│   ├── main.py          # Game initialization & main loop
│   ├── const.py         # Constants & configuration
│   │
│   ├── # Core Game Modules
│   ├── level.py         # Level loading & game state
│   ├── castle.py        # Player castle entity
│   ├── units.py         # Unit stats & behavior
│   ├── items.py         # Collectible items
│   ├── tiles.py         # Tile interaction handlers
│   │
│   ├── # Game States
│   ├── states.py        # Game state classes
│   ├── intro.py         # Intro sequence
│   ├── title.py         # Title screen
│   ├── menu.py          # Level select menu
│   │
│   ├── # Enemy Entities
│   ├── robot.py         # Peasant AI
│   ├── flock.py         # Flocking behavior
│   ├── cannon.py        # Enemy cannons
│   ├── truck.py         # Coal trucks
│   ├── factory.py       # Factory buildings
│   │
│   ├── # Visual Effects
│   ├── effect.py        # Effect system
│   ├── steam.py         # Steam particle effects
│   ├── explode.py       # Explosion effects
│   ├── fire.py          # Fire effects
│   │
│   ├── # UI & Interface
│   ├── interface.py     # HUD & status display
│   ├── messages.py      # Procedural message generator
│   ├── html.py          # HTML text rendering
│   │
│   ├── # Audio
│   ├── sounds.py        # Sound manager
│   ├── sound_info.py    # Sound definitions
│   │
│   ├── # Engine Components
│   ├── isovid.py        # Isometric renderer
│   ├── algo.py          # A* pathfinding
│   ├── cyclic_list.py   # Utility data structure
│   ├── util.py          # Utility functions
│   │
│   ├── pgu/             # Phil's Game Utilities library
│   │   ├── engine.py    # State machine engine
│   │   ├── vid.py       # Video/tile engine base
│   │   ├── isovid.py    # Isometric extension
│   │   ├── timer.py     # Timer utilities
│   │   ├── gui/         # GUI components
│   │   └── ...
│   │
│   └── data/            # Game assets
│       ├── gfx/         # Graphics (tiles, sprites)
│       ├── sounds/      # Sound effects
│       ├── intro/       # Intro assets & music
│       ├── menu/        # Menu assets
│       ├── levels/      # Level data (TGA files)
│       └── themes/      # UI themes
```

## Core Systems

### State Machine (pgu.engine)

The game uses a state machine pattern for managing screens:

```python
class Game(engine.Game):
    def init(self):
        # Initialize game
        
    def tick(self):
        # Called each frame
        
    def event(self, e):
        # Handle global events

# State transitions
Intro → Title → Menu → Level → (NextLevel | GameOver | GameWon) → Menu/Title
```

State classes implement:
- `init()` - Initialize state
- `paint(screen)` - Initial render
- `update(screen)` - Per-frame update
- `loop()` - Game logic (may return new state)
- `event(e)` - Event handling (may return new state)

### Isometric Engine (isovid.py)

Extends the PGU vid system for isometric rendering:

```
Coordinate Systems:
- Screen coords (pixels on display)
- View coords (world pixels, offset by view position)  
- Iso coords (isometric world coordinates)
- Tile coords (grid cell coordinates)

Conversion Functions:
- iso_to_view(pos) - Convert iso to view coords
- view_to_iso(pos) - Convert view to iso coords
- tile_to_view(pos) - Convert tile to view coords
- screen_to_tile(pos) - Convert screen to tile coords
```

Tile layers:
- `tlayer` - Foreground tiles (interactive)
- `blayer` - Background tiles (decoration)
- `clayer` - Code layer (spawn points)
- `zlayer` - Z-height layer
- `robot_layer` - Pathfinding for robots
- `castle_layer` - Pathfinding for castle

### Entity System

Entities are sprites with attached behavior:

```python
class Sprite:
    rect        # Position & size
    image       # Current image
    groups      # Collision groups (bitmask)
    agroups     # Groups to collide against
    loop        # Per-frame callback: loop(g, sprite)
    hit         # Collision callback: hit(g, self, other)
```

Entity types:
- Castle (player)
- Robot (peasant)
- Cannon (enemy turret)
- Truck (resource transport)
- Factory (enemy building)
- Cball (cannonball projectile)

### Unit System (units.py)

Units have stats dictionaries:

```python
stats = {
    'Health': 10.0,
    'MaxHealth': 10.0,
    'Coal': 65.0,
    'MaxCoal': 70.0,
    'Water': 65.0,
    'MaxWater': 70.0,
    'Steam': 100.0,
    'MaxSteam': 100.0,
    'Speed': 10.0,
    'Armour': 0.0,
    'Damage': 1.0,
    'EngineEfficiency': 3.0,
    'CannonPressure': 0.0,
    'MaxCannonPressure': 16.0,
    # ... more stats
}
```

Unit classes: Castle, Robot, CannonTower, CoalTruck, Factory

### Flocking System (flock.py)

Implements Boids-like flocking for peasants:

```python
class Flock:
    def __init__(self, rect, spacing):
        # Spatial grid for neighbor lookup
        
    def loop(self):
        # Per-frame update:
        # 1. Update spatial grid
        # 2. Calculate velocities
        # 3. Find neighbors
        # 4. Apply flocking rules:
        #    - Cohesion (move toward center)
        #    - Separation (avoid neighbors)
        #    - Alignment (match velocity)
        # 5. Enforce min/max velocity
```

### Sound System (sounds.py)

```python
class SoundManager:
    def Load(self, sound_list)    # Load sounds
    def Play(self, name, ...)     # Play sound
    def Stop(self, name)          # Stop sound
    def PlayMusic(self, name)     # Play background music
    def Update(self, elapsed)     # Process queued sounds
```

Sound queuing modes:
- 0: Play immediately (overlap)
- 1: Queue if already playing
- 2: Skip if already playing
- 3: Play immediately, no queue

### Interface System (interface.py)

```python
class Interface:
    def load(self)                # Load UI graphics
    def update(self, tv, screen)  # Render HUD
    def event(self, g, e)         # Handle UI events
    
class StatsDraw:
    def update_stats(self, screen, stats, ...)  # Render stat bars
```

Dirty flag system for efficient updates:
- Only redraws changed UI elements
- Tracks: messages, backgrounds, equipment, etc.

## Data Flow

### Frame Update Cycle

```
1. Game.tick()
   - Update timers
   - Update sound manager
   
2. State.loop()
   - Game logic
   - Entity updates
   - Flock calculations
   - Collision detection
   - Win/lose checks
   
3. State.update(screen) / State.paint(screen)
   - Render background
   - Render tiles
   - Render entities (z-sorted)
   - Render effects
   - Render UI
   
4. Event Processing
   - Handle pygame events
   - Pass to state.event()
   - Pass to entity event handlers
```

### Level Loading

```
1. Load tile graphics (tga_load_tiles)
2. Load level map (tga_load_level)
3. Initialize pathfinding layers
4. Run spawn codes (run_codes)
5. Initialize flocking system
6. Load interface
```

### Collision System

Collision groups (bitmask):
- `castle` - Player castle
- `robot` - Peasants
- `cball` - Cannonballs
- `cannon` - Enemy cannons
- `factory` - Factory buildings
- `truck` - Coal trucks

Collision checking:
- `sprite.groups` - What groups sprite belongs to
- `sprite.agroups` - What groups to check collisions against
- On collision: calls `sprite.hit(g, self, other)`

## Configuration

Key configuration in `const.py`:
- Screen dimensions (SW, SH)
- Frame rate (FPS)
- UI rectangles (S_VIEW, S_STATUS, etc.)
- Gameplay constants (MIN_CANNON_PRESSURE, etc.)
- Debug flags (CACHE_USE_LEVEL_CACHE, etc.)

## Performance Considerations

1. **Background Caching**: Pre-rendered background cached to disk
2. **Spatial Grid**: Flocking uses grid for O(1) neighbor lookup
3. **Dirty Rectangles**: UI only redraws changed elements
4. **Pathfinding Layers**: Pre-computed walkability grids

## Extension Points

To add new features:

1. **New Entity Type**: Create sprite with loop/hit callbacks, add to level.py cdata
2. **New Upgrade**: Add to units.upgrade_amounts, update upgrade_part()
3. **New Level**: Create TGA file in data/levels/, add to menu.data
4. **New Effect**: Create Effect class with loop/paint methods
5. **New State**: Extend engine.State, wire into state transitions
