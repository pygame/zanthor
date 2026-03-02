# Asset Reference

This document describes the game assets and their organization.

## Asset Directory Structure

```
zanthor/data/
├── gfx/          # Graphics (sprites, tiles, UI)
├── sounds/       # Sound effects
├── intro/        # Intro sequence assets
├── menu/         # Menu assets (fonts)
├── levels/       # Level data files
├── themes/       # UI theme resources
└── cache/        # Runtime cache (generated)
```

## Graphics (data/gfx/)

### Tile Graphics

**tiles2.tga** (or .png)
- Main tileset for all levels
- 32x64 pixel tiles arranged in a grid
- Contains terrain, walls, items, and structures

Tile indices:
| Index | Content |
|-------|---------|
| 0 | Empty/grass |
| 1 | Coal |
| 2 | Water |
| 3-6 | Walls (various damage states) |
| 7 | Rubble |
| 8-15 | Upgrade parts |
| 23 | Wall |
| 28 | Limit tile (boundary) |
| 30 | Hole (impassable) |
| 32-35 | Cannonballs (different sizes) |

### Sprite Graphics

Castle sprites extracted from tiles2.tga:
- `castle` - Main castle sprite
- `castle.left` - Castle facing left
- `castle.right` - Castle facing right (flipped)

Other sprite names:
- `robot` - Peasant sprite
- `coal`, `water` - Resource sprites
- `factory`, `cannon`, `truck` - Enemy structures
- `cball`, `cball2`, `cball3`, `cball4` - Cannonball sizes
- `hole`, `hole2`, `hole3`, `hole4` - Ground holes

### UI Graphics

| Filename | Purpose |
|----------|---------|
| background_status_left.png | Left panel background |
| background_bottom.png | Bottom panel background |
| background_illustration.png | Castle illustration |
| background_equipment.png | Equipment panel |
| background_buttons.png | Button panel |
| background_messages.png | Message area |
| heart.png | Health meter heart |
| heart_pulse.png | Health meter pulse frame |
| health_overlay.png | Health bar overlay |
| coal_overlay.png | Coal bar overlay |
| water_overlay.png | Water bar overlay |
| steam_overlay.png | Steam bar overlay |
| hairs.tga/png | Crosshair cursor |
| caastles.png | Level select background |

### Button Graphics

Each button has three states:
- `button_*.png` - Normal state
- `button_*_rollover.png` - Hover state
- `button_*_down.png` - Pressed state

Buttons: save, load, quit, news

## Sound Effects (data/sounds/)

### Combat Sounds

| Filename | Event |
|----------|-------|
| cannon.wav/ogg | Cannon fire (low power) |
| cannon2.wav/ogg | Cannon fire (medium) |
| cannon3.wav/ogg | Cannon fire (high power) |
| hitenemy.wav/ogg | Hit enemy |
| hitwall.wav/ogg | Hit wall |
| hitwall2.wav/ogg | Hit wall (alternate) |
| hitground.wav/ogg | Cannonball hits ground |
| destroyenemy.wav/ogg | Enemy destroyed |

### Damage Sounds

| Filename | Event |
|----------|-------|
| ouch1.wav/ogg | Player hit |
| ouch2.wav/ogg | Player hit (alternate) |
| squish1.wav/ogg | Peasant crushed |
| squish2.wav/ogg | Peasant crushed (alternate) |

### Resource Sounds

| Filename | Event |
|----------|-------|
| coal.wav/ogg | Coal pickup |
| water.wav/ogg | Water pickup |
| upgrade.wav/ogg | Upgrade applied |

### Ambient Sounds

| Filename | Event |
|----------|-------|
| birds1.wav/ogg | Bird ambience |
| birds2.wav/ogg | Bird ambience |
| peasants1.wav/ogg | Peasant noise |
| peasants2.wav/ogg | Peasant noise |
| peasants3.wav/ogg | Peasant noise |

### Engine Sounds

| Filename | Event |
|----------|-------|
| engine-slow.wav/ogg | Engine idle |
| engine-fast.wav/ogg | Engine running |
| release.wav/ogg | Steam release |

## Music (data/intro/)

| Filename | Usage |
|----------|-------|
| intro1.ogg | Intro sequence |
| zanthor.ogg | Title screen |
| soundtrack1.ogg | Easy levels (1-4) |
| soundtrack2.ogg | Medium levels (5-7) |
| soundtrack3.ogg | Final level (8) |
| grass.ogg | Victory screen |

## Fonts (data/intro/, data/menu/)

| Filename | Usage |
|----------|-------|
| WALSHES.TTF | Intro text, title |
| vinque.ttf | Menu text, HUD |

## Level Files (data/levels/)

Levels are stored as TGA images where pixel colors encode tile data:

### TGA Format

- Red channel: Foreground tile index
- Green channel: Background tile index
- Blue channel: Code layer (spawn points)

### Level Files

| Filename | Level Name |
|----------|------------|
| level1.tga | Simple City |
| level2.tga | Valiant Village |
| level3.tga | Humble Hamlet |
| level4.tga | Congenial Burg |
| level5.tga | Truthful Tower |
| level6.tga | Loyal Lookout |
| level7.tga | Observatory of Honor |
| level8.tga | Comfy Castle |
| test2.tga | Test level |

### Spawn Codes (Blue Channel)

| Value | Spawns |
|-------|--------|
| 1 | Castle (player) |
| 4 | Factory |
| 5 | Truck |
| 6 | Cannon |
| 7 | Robot (peasant) |

## Themes (data/themes/)

UI theme resources for the PGU GUI system. Contains style definitions and themed widget graphics.

## Creating New Assets

### Adding New Tiles

1. Edit `tiles2.tga` to add tile graphics at an unused index
2. In `level.py`, add tile data mapping:
   ```python
   tdata = {
       NEW_INDEX: ('collision_groups', handler_function, config),
   }
   ```
3. Optionally create a handler function in `tiles.py`

### Adding New Sounds

1. Place sound file in `data/sounds/` (.wav or .ogg)
2. Add to `sound_info.py`:
   ```python
   newsound = cl(['newsound1', 'newsound2'])
   ```
3. Play in code:
   ```python
   g.level.game.sm.Play(sound_info.newsound.nextone())
   ```

### Adding New Levels

1. Create TGA image with appropriate size
2. Paint tiles using red channel
3. Paint spawn points using blue channel
4. Add to `menu.py` data array:
   ```python
   (lock_level, pygame.Rect(...), 'Name', population, 
    'filename.tga', win_percent, 'Zanthor Name', 
    'music.ogg', (row, col))
   ```

### Level Design Tips

- Ensure castle spawn point (code 1) exists
- Place coal (tile 1) and water (tile 2) for resources
- Use walls (tiles 3-6) to create obstacles
- Scatter robots (code 7) across the map
- Consider player progression with upgrade parts (tiles 8-15)

## Asset Technical Details

### Image Formats

- TGA: Preferred for tiles and levels (lossless, supports alpha)
- PNG: Alternative format (fallback in code)
- Images are loaded with `pygame.image.load()`
- Alpha transparency via `.convert_alpha()` where needed
- Color key transparency via `.set_colorkey((255, 0, 255))`

### Audio Formats

- OGG: Preferred (compressed, good quality)
- WAV: Alternative (uncompressed)
- Loaded via `pygame.mixer.Sound()`
- Music via `pygame.mixer.music`

### Font Formats

- TTF: TrueType fonts
- Various sizes rendered at runtime

## Cache System

The game caches pre-rendered level backgrounds to speed up loading:

Location: `data/cache/levels/`

Cache files:
- Named after level files (e.g., `level1.jpg`)
- Created automatically if loading takes > 1 second
- Invalidated if level or tile files are modified
- Controlled by `CACHE_USE_LEVEL_CACHE` in `const.py`

To clear cache:
```bash
rm -rf zanthor/data/cache/
```
