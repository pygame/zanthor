""" this file has lots of tweaky things in it.

Historically every value here was hard‑coded.  The module now pulls the
values that *should* be user‑configurable from :mod:`zanthor.settings`
(resolution, FPS, control keys, audio levels, …).  Anything not in the
schema stays a plain constant so existing ``from .const import *``
imports keep working unchanged.

Tweakable files (other) :
    sound_info.py - tweaking sounds.
    units.py - tweaking unit stats.

"""


import pygame

import os

# --------------------------------------------------------------------- #
#  User settings – loaded once at import time.
# --------------------------------------------------------------------- #
# The settings module is intentionally import‑safe: importing it never
# initialises pygame, and any I/O error simply yields defaults.  This
# means ``const.py`` (which is imported from nearly every file in the
# game) can still be used as a source of module‑level "constants"
# while really reading from a JSON config the user can edit.
from . import settings as _settings


_DATA_DIR = None


def data_dir(*args):
    global _DATA_DIR
    if _DATA_DIR is None:
        # _DATA_DIR = os.path.join(*(['zanthor', 'data'] + list(args)))
        _DATA_DIR = os.path.join("zanthor", "data")
        if not os.path.exists(_DATA_DIR):
            _DATA_DIR = os.path.join(os.path.split(__file__)[0], "data")
    return os.path.join(*([_DATA_DIR] + list(args)))


# --------------------------------------------------------------------- #
#  Display
# --------------------------------------------------------------------- #
# The base size every layout rect was authored against.  All the S_* rects
# below are multiplied by (DX, DY) so the UI scales to whatever resolution
# the user picks.
BSW, BSH = 640, 480

# Previous code did:
#     SW, SH = 640, 480      # <-- hard-coded!
# Now we ask the settings module.  Users can change this either in the
# in-game Options screen or by editing ~/.config/zanthor/settings.json.
SW, SH = _settings.resolution()

DX = float(SW) / BSW
DY = float(SH) / BSH

dxdy = (DX, DY)

# Likewise FPS is now configurable ("display.fps_cap" in settings.json).
FPS = _settings.fps_cap()

MIN_CANNON_PRESSURE = 6


def multr(dx_dy, r):
    a, b, c, d = tuple(r)
    dx, dy = dxdy
    return pygame.Rect(a * dx, b * dy, c * dx, d * dy)


# S_VIEW = pygame.Rect(0,0,480,480)


S_STATUS = multr(dxdy, (480, 320, 400, 160))

S_ITEMS = multr(dxdy, (480, 160, 160, 200))
S_STATUS = multr(dxdy, (480, 360, 160, 120))


# game view area.
S_VIEW = multr(dxdy, (76, 0, 380, 340))


# left side, full status area.
S_STATUS = multr(dxdy, (0, 0, 76, 340))


# left side status boxes.
# S_HEALTH = pygame.Rect(10,30,60,70)
S_HEALTH = multr(dxdy, (10, 4, 60, 96))
S_COAL = multr(dxdy, (10, 100, 60, 70))
S_WATER = multr(dxdy, (10, 190, 60, 70))
S_STEAM = multr(dxdy, (10, 260, 60, 70))

S_PEASANTS_REMAINING = multr(dxdy, (487, 24, 122, 114))
S_CANNON_PRESSURE = multr(dxdy, (76, 0, 5, 340))


# top right,  castle robot illustration area.
S_ROBOT = multr(dxdy, (456, 0, 184, 163))


# middle right, items area.
S_ITEMS = multr(dxdy, (456, 163, 184, 177))


S_ITEMS_ENGINE = multr(dxdy, (480, 160, 160, 160))
S_ITEMS_COALSTORAGEROOM = multr(dxdy, (480, 160, 160, 160))
S_ITEMS_WATERTANK = multr(dxdy, (480, 160, 160, 160))
S_ITEMS_CANNON = multr(dxdy, (480, 160, 160, 160))
S_ITEMS_ARMOUR = multr(dxdy, (480, 160, 160, 160))


# bottom right,  button area.
S_BUTTONS = pygame.Rect(470, 340, 170, 140)

S_BUTTONS_SAVE = pygame.Rect(490, 360, 60, 40)
S_BUTTONS_LOAD = pygame.Rect(490, 420, 60, 40)
S_BUTTONS_QUIT = pygame.Rect(560, 360, 60, 40)
S_BUTTONS_NEWS = pygame.Rect(560, 420, 60, 40)

S_BOTTOM = pygame.Rect(0, 340, 640, 140)

(
    S_BUTTONS,
    S_BUTTONS_SAVE,
    S_BUTTONS_LOAD,
    S_BUTTONS_QUIT,
    S_BUTTONS_NEWS,
    S_BOTTOM,
) = [
    multr(dxdy, x)
    for x in [
        S_BUTTONS,
        S_BUTTONS_SAVE,
        S_BUTTONS_LOAD,
        S_BUTTONS_QUIT,
        S_BUTTONS_NEWS,
        S_BOTTOM,
    ]
]


S_BOTTOM_BUTTONS = multr(dxdy, (470, 0, 170, 140))
S_BOTTOM_MESSAGES = multr(dxdy, (95, 25, 355, 110))
# bottom middle message area.
S_MESSAGES = multr(dxdy, (95, 365, 355, 110))

# S_NEXT_LEVEL_MESSAGES = pygame.Rect(20,165,380,410)
S_NEXT_LEVEL_MESSAGES = multr(dxdy, (20, 20, 500, 410))


S_ = pygame.Rect(480, 360, 160, 120)


# --------------------------------------------------------------------- #
#  Gameplay toggles – now sourced from settings (with sane fallbacks).
# --------------------------------------------------------------------- #
# Debug: pressing 1-8 in-game grants free upgrades.  Disabled by default
# for regular players; power users can flip it in the Options screen.
UPGRADE_FUN = 1 if _settings.get("gameplay.debug_upgrades", False) else 0

CACHE_USE_LEVEL_CACHE = 1

# if you are modifying just the tiles or just the levels set one of these to 0.
#  These only check the levels,
#    or the tiles to see if its older than the cache.
CACHE_CHECK_TILES = 1
CACHE_CHECK_LEVEL = 1


# --------------------------------------------------------------------- #
#  Controls
# --------------------------------------------------------------------- #
# joystick buttons (indices, not pygame constants)
JOY_FIRE_BUTTON = int(_settings.get("controls.joy_fire_button", 1))
JOY_PICKUP_BUTTON = int(_settings.get("controls.joy_pickup_button", 2))

# should things be auto picked up or not?
AUTO_PICKUP = 1 if _settings.get("gameplay.auto_pickup", True) else 0

# should holes that the castle hits the ground be
# solid tiles
# 0 = no, 1 = yes, 2= big holes
HOLES_ARE_TILES = int(_settings.get("gameplay.holes_are_tiles", 0) or 0)


# NOTE: mouselook seems to not work well on some systems...
#       can toggle it with the m key in game.
# 1 disables mouse-look, 0 enables it – we derive it from the *positive*
# "mouse_look" boolean in settings so the JSON stays intuitive.
DISABLE_MOUSE_LOOK = 0 if _settings.get("controls.mouse_look", True) else 1


FLOCKING_FLUCT = 1


def get_mouse_info():
    if DISABLE_MOUSE_LOOK:
        SCROLL_MOUSE = 0  # speed of mouse scroll
        SCROLL_AUTO = 9  # speed of auto-return scroll
        SCROLL_BORDER = 70  # size of scrolling border during auto-scroll
    else:
        SCROLL_MOUSE = 12  # speed of mouse scroll
        SCROLL_AUTO = 9  # speed of auto-return scroll
        SCROLL_BORDER = 160  # size of scrolling border during auto-scroll

    return [SCROLL_MOUSE, SCROLL_AUTO, SCROLL_BORDER]


# --------------------------------------------------------------------- #
#  Key-binding helpers
# --------------------------------------------------------------------- #
# Historically the castle/level/menu modules compared against hard-coded
# pygame K_* constants.  They now call these helpers, which resolve the
# user's bindings on the fly.  Calling settings.keys(...) is cheap – the
# settings module caches the resolved key-codes until a rebind happens.

def KEYS_UP():
    """Pygame key-codes bound to 'move up'."""
    return _settings.keys("move_up")


def KEYS_DOWN():
    return _settings.keys("move_down")


def KEYS_LEFT():
    return _settings.keys("move_left")


def KEYS_RIGHT():
    return _settings.keys("move_right")


def KEYS_FIRE():
    return _settings.keys("fire")


def KEYS_PAUSE():
    return _settings.keys("pause")


def KEYS_TOGGLE_MOUSELOOK():
    return _settings.keys("toggle_mouselook")
