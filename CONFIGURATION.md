# Zanthor – Configuration System

Zanthor ships with a simple, modular configuration system that lets
players tweak **display, audio, controls and gameplay** settings either
from the in‑game **Options** screen or by hand‑editing a JSON file.

---

## In‑game Options Screen

Open the game → **Options** on the title menu.

| Input | Action |
|---|---|
| Mouse click | Select tab / row / button; drag a slider; click again to edit |
| `Tab` / `Shift+Tab` | Cycle tabs |
| `↑` / `↓` | Move selection |
| `←` / `→` | Adjust current value (slider / choice / toggle) |
| `Enter` / `Space` | Toggle / cycle / start key‑rebind |
| Mouse wheel | Scroll the options list |
| `Esc` | Back (auto‑saves on exit) |

Key‑rebind: select a key‑binding row → `Enter` → press any key, or
`Backspace` to clear the binding, or `Esc` to cancel.

Settings marked with a red `*` require restarting the game.

---

## Configuration file

The file lives at a platform‑appropriate location:

| Platform | Path |
|---|---|
| Linux / BSD | `~/.config/zanthor/settings.json` |
| macOS | `~/Library/Application Support/zanthor/settings.json` |
| Windows | `%APPDATA%\zanthor\settings.json` |
| Override | set `$ZANTHOR_CONFIG_DIR` |

It is **safe to hand‑edit** – the loader validates and clamps every
value.  Missing keys fall back to defaults; unknown keys are ignored;
a corrupt file simply yields the defaults (and is logged, not thrown).

Example:
```json
{
  "display": {
    "resolution": [1024, 768],
    "fullscreen": true,
    "fps_cap": 60,
    "skip_intro": true
  },
  "audio": {
    "music_volume": 0.5,
    "sfx_volume": 0.8,
    "mute": false
  },
  "controls": {
    "move_up":    ["i"],
    "move_down":  ["k"],
    "move_left":  ["j"],
    "move_right": ["l"],
    "fire":       ["e"],
    "mouse_look": false
  },
  "gameplay": {
    "auto_pickup": false,
    "holes_are_tiles": 1
  }
}
```

Key names are the human‑readable names returned by
`pygame.key.name()` (`"space"`, `"left ctrl"`, `"return"` …).

---

## For developers

The two new modules are drop‑in:

* **`zanthor/settings.py`** – schema‑driven `Settings` singleton.
  Adding a new option is one line in the `SCHEMA` dict and it shows up
  in the UI automatically.  `settings.get("section.key")`,
  `settings.keys("move_up")`, `settings.save()` … that's the whole API.

* **`zanthor/options.py`** – a `pgu.engine.State` that renders the
  Options screen purely with pygame primitives (no extra deps).

`const.py` now sources its previously hard‑coded values from
`settings`, and `KEYS_UP()`, `KEYS_FIRE()` etc. helpers are used by
`castle.py`, `menu.py` and `level.py` instead of literal `K_*`
constants, so rebinds take effect immediately.
