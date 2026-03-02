"""
zanthor.settings
================

A simple, modular configuration system for Zanthor.

Design goals
------------
*   **Single source of truth** – one `Settings` object, imported as
    ``from zanthor import settings`` anywhere in the code base.
*   **Human‑editable** – persisted as pretty‑printed JSON in the user's
    config directory (``~/.zanthor/settings.json`` or the platform
    equivalent).  Users may hand‑edit the file; unknown keys are ignored
    and missing keys fall back to schema defaults.
*   **Schema‑driven validation** – every option is described by a
    :class:`Spec` which provides the default value, an optional
    ``choices`` list or ``(min, max)`` range, a widget hint and a
    human‑readable label / description.  The Options UI is generated
    directly from the schema so adding a new setting is a one‑line change.
*   **Key‑binding support** – actions are stored as lists of *pygame
    key names* (``"w"``, ``"left ctrl"`` …) so the JSON stays portable
    across pygame / SDL versions.  Helper :func:`Settings.keys` returns
    the resolved key‑codes for fast event comparison.
*   **Live apply** – whenever a value changes, registered listeners are
    notified.  Audio‑volume changes for example take effect immediately
    while the user is still dragging the slider.

Usage
-----
>>> from zanthor import settings
>>> settings.get("display.resolution")          # -> (640, 480)
>>> settings.get("audio.music_volume")          # -> 0.8
>>> settings.keys("move_up")                    # -> [K_UP, K_w]
>>> settings.set("audio.music_volume", 0.5)
>>> settings.save()

Adding a new option is literally one entry in :data:`SCHEMA`; the
Options screen picks it up automatically.
"""

from __future__ import annotations

import copy
import json
import os
import sys
import traceback

# NOTE: pygame is imported lazily inside the methods that need it so that
#       importing ``zanthor.settings`` never triggers a pygame.init().
#       This keeps start‑up fast and allows the module to be used in
#       headless tools (e.g. a future CLI settings dump).


# ---------------------------------------------------------------------------
#  Schema description
# ---------------------------------------------------------------------------

class Spec:
    """Describes a single configurable value.

    Parameters
    ----------
    default : Any
        Fallback value when the key is absent or invalid.
    label : str
        Human‑friendly name shown in the Options screen.
    kind : str
        Widget hint.  One of:
        ``"toggle"``, ``"choice"``, ``"slider"``, ``"int"``, ``"key"``.
    choices : list, optional
        Permitted values for ``"choice"`` kind (also used to cycle
        resolutions).
    vmin, vmax : number, optional
        Inclusive range for ``"slider"`` / ``"int"`` kinds.
    step : number, optional
        Increment used by the UI when adjusting via keyboard.
    desc : str, optional
        Longer description / tooltip text.
    restart : bool, optional
        When True the UI displays a *"requires restart"* badge.
    """

    __slots__ = (
        "default",
        "label",
        "kind",
        "choices",
        "vmin",
        "vmax",
        "step",
        "desc",
        "restart",
    )

    def __init__(
        self,
        default,
        label,
        kind,
        choices=None,
        vmin=None,
        vmax=None,
        step=None,
        desc="",
        restart=False,
    ):
        self.default = default
        self.label = label
        self.kind = kind
        self.choices = choices
        self.vmin = vmin
        self.vmax = vmax
        self.step = step
        self.desc = desc
        self.restart = restart

    # -- validation -----------------------------------------------------
    def coerce(self, value):
        """Return *value* coerced / clamped to this spec.

        Invalid input silently falls back to ``self.default`` – we never
        want a corrupt settings file to crash the game.
        """
        try:
            if self.kind == "toggle":
                return bool(value)

            if self.kind == "choice":
                # Choices may be scalars (ints / strings) OR sequences
                # like resolution tuples.  Sequence values are stored
                # as JSON lists so we compare against both list and
                # tuple forms.  Scalar choices just use plain ==.
                if self.choices:
                    for c in self.choices:
                        if value == c:
                            return c
                        if isinstance(c, (list, tuple)):
                            try:
                                if list(value) == list(c):
                                    return tuple(c)
                            except TypeError:
                                pass
                return copy.deepcopy(self.default)

            if self.kind == "slider":
                v = float(value)
                if self.vmin is not None:
                    v = max(self.vmin, v)
                if self.vmax is not None:
                    v = min(self.vmax, v)
                return round(v, 3)

            if self.kind == "int":
                v = int(value)
                if self.vmin is not None:
                    v = max(self.vmin, v)
                if self.vmax is not None:
                    v = min(self.vmax, v)
                return v

            if self.kind == "key":
                # Expect a list of pygame *key names* (strings).
                if isinstance(value, (list, tuple)):
                    out = [str(x) for x in value if isinstance(x, (str, int))]
                    return out or list(self.default)
                return list(self.default)

            return value  # unknown kind – pass through
        except Exception:
            return copy.deepcopy(self.default)


# ---------------------------------------------------------------------------
#  The Schema
# ---------------------------------------------------------------------------
# The schema is a dict‑of‑dicts: section -> option -> Spec.
# Sections map naturally to tabs in the Options UI.

_RESOLUTIONS = [
    (640, 480),
    (800, 600),
    (1024, 768),
    (1280, 720),
    (1280, 800),
    (1366, 768),
    (1600, 900),
    (1920, 1080),
]

SCHEMA = {
    # ----------------------------------------------------------------- #
    "display": {
        "resolution": Spec(
            (640, 480),
            "Resolution",
            "choice",
            choices=_RESOLUTIONS,
            desc="Window size. The game scales its layout automatically.",
            restart=True,
        ),
        "fullscreen": Spec(
            False,
            "Fullscreen",
            "toggle",
            desc="Run the game in fullscreen mode.",
            restart=True,
        ),
        "fps_cap": Spec(
            30,
            "FPS Cap",
            "int",
            vmin=20,
            vmax=120,
            step=5,
            desc="Maximum frames per second.",
            restart=True,
        ),
        "skip_intro": Spec(
            False,
            "Skip Intro",
            "toggle",
            desc="Skip the opening cutscene and jump straight to the title.",
        ),
    },
    # ----------------------------------------------------------------- #
    "audio": {
        "music_volume": Spec(
            0.8,
            "Music Volume",
            "slider",
            vmin=0.0,
            vmax=1.0,
            step=0.05,
            desc="Background music loudness.",
        ),
        "sfx_volume": Spec(
            1.0,
            "Effects Volume",
            "slider",
            vmin=0.0,
            vmax=1.0,
            step=0.05,
            desc="Sound‑effect loudness.",
        ),
        "mute": Spec(
            False,
            "Mute All",
            "toggle",
            desc="Silence every channel.",
        ),
    },
    # ----------------------------------------------------------------- #
    "controls": {
        # Key bindings are stored as *key‑name* lists so the JSON stays
        # readable and portable across SDL versions.
        "move_up": Spec(["up", "w"], "Move Up", "key"),
        "move_down": Spec(["down", "s"], "Move Down", "key"),
        "move_left": Spec(["left", "a"], "Move Left", "key"),
        "move_right": Spec(["right", "d"], "Move Right", "key"),
        "fire": Spec(["space", "f", "left ctrl", "right ctrl"], "Fire", "key"),
        "pause": Spec(["p", "return", "h"], "Pause / Help", "key"),
        "toggle_mouselook": Spec(["m"], "Toggle Look", "key"),
        "mouse_look": Spec(
            True,
            "Mouse-Look",
            "toggle",
            desc="Scroll the view when the cursor approaches the edge.",
        ),
        "joy_fire_button": Spec(
            1,
            "Joy Fire Btn",
            "int",
            vmin=0,
            vmax=15,
            step=1,
            desc="Joystick button index used to fire.",
        ),
        "joy_pickup_button": Spec(
            2,
            "Joy Pickup Btn",
            "int",
            vmin=0,
            vmax=15,
            step=1,
            desc="Joystick button index used to pick items up.",
        ),
    },
    # ----------------------------------------------------------------- #
    "gameplay": {
        "auto_pickup": Spec(
            True,
            "Auto-Pickup",
            "toggle",
            desc="Automatically collect coal, water and parts on contact.",
        ),
        "holes_are_tiles": Spec(
            0,
            "Cannon Craters",
            "choice",
            choices=[0, 1, 2],
            desc="0 = cosmetic, 1 = solid, 2 = big solid craters.",
        ),
        "debug_upgrades": Spec(
            False,
            "Debug Upgrades",
            "toggle",
            desc="Allow the 1-8 number keys to grant free upgrades.",
        ),
    },
}


# Flat look‑up of "section.option" -> Spec for convenience.
_FLAT = {
    "{}.{}".format(sec, key): spec
    for sec, opts in SCHEMA.items()
    for key, spec in opts.items()
}


# ---------------------------------------------------------------------------
#  Storage location helpers
# ---------------------------------------------------------------------------

def _user_config_dir(app_name="zanthor"):
    """Return a per‑user, per‑platform directory for config files.

    Creates the directory if it does not yet exist.  If that fails
    (read‑only home, sandboxed env …) we silently fall back to the
    *current working directory* so the game still runs.
    """
    # Allow packagers / power users to override the location completely.
    override = os.environ.get("ZANTHOR_CONFIG_DIR")
    if override:
        path = os.path.expanduser(override)
    elif sys.platform.startswith("win"):
        base = os.environ.get("APPDATA") or os.path.expanduser("~")
        path = os.path.join(base, app_name)
    elif sys.platform == "darwin":
        path = os.path.expanduser(
            os.path.join("~", "Library", "Application Support", app_name)
        )
    else:
        base = os.environ.get("XDG_CONFIG_HOME") or os.path.expanduser("~/.config")
        path = os.path.join(base, app_name)

    try:
        os.makedirs(path, exist_ok=True)
    except Exception:
        path = os.getcwd()
    return path


_CONFIG_FILE = os.path.join(_user_config_dir(), "settings.json")


# ---------------------------------------------------------------------------
#  The Settings object
# ---------------------------------------------------------------------------

class Settings:
    """In‑memory view of the user's configuration.

    The object behaves like a small dict keyed by dotted paths
    (``"display.resolution"``).  Change listeners can be registered with
    :meth:`subscribe` – this is how the Options UI makes audio sliders
    feel *live*.
    """

    def __init__(self):
        self._data = self._defaults()
        self._listeners = []          # list of callables(key, value)
        self._key_cache = {}          # action -> [key_codes]
        self._dirty_restart = False   # True once any restart‑only value changed
        self._loaded_snapshot = None  # values as last saved/loaded for dirty‑check
        self.config_path = _CONFIG_FILE

    # ------------------------------------------------------------------
    #  construction helpers
    # ------------------------------------------------------------------
    @staticmethod
    def _defaults():
        out = {}
        for sec, opts in SCHEMA.items():
            out[sec] = {}
            for key, spec in opts.items():
                out[sec][key] = copy.deepcopy(spec.default)
        return out

    # ------------------------------------------------------------------
    #  persistence
    # ------------------------------------------------------------------
    def load(self, path=None):
        """Load from *path* (defaults to the standard config file).

        Never raises – any error simply leaves the defaults in place and
        is logged to stderr.  A fresh file is written on first run so
        users can discover where the config lives.
        """
        path = path or self.config_path
        self.config_path = path

        if os.path.exists(path):
            try:
                with open(path, "r", encoding="utf-8") as fh:
                    raw = json.load(fh)
                self._merge(raw)
                print("[settings] loaded {}".format(path))
            except Exception:
                print("[settings] failed to parse {} – using defaults".format(path))
                traceback.print_exc()
        else:
            # Seed the file so users can find it & tweak by hand.
            self.save()
            print("[settings] created default config at {}".format(path))

        self._loaded_snapshot = json.dumps(self._data, sort_keys=True)
        self._key_cache.clear()
        self._apply_live_audio()
        return self

    def save(self, path=None):
        path = path or self.config_path
        try:
            tmp = path + ".tmp"
            with open(tmp, "w", encoding="utf-8") as fh:
                json.dump(self._data, fh, indent=2, sort_keys=True)
            os.replace(tmp, path)  # atomic on POSIX, best‑effort on Windows
            self._loaded_snapshot = json.dumps(self._data, sort_keys=True)
            print("[settings] saved {}".format(path))
        except Exception:
            print("[settings] could not write {}".format(path))
            traceback.print_exc()
        return self

    def _merge(self, raw):
        """Merge a raw dict (from JSON) into ``self._data`` with coercion."""
        if not isinstance(raw, dict):
            return
        for sec, opts in SCHEMA.items():
            src = raw.get(sec, {})
            if not isinstance(src, dict):
                continue
            for key, spec in opts.items():
                if key in src:
                    self._data[sec][key] = spec.coerce(src[key])

    # ------------------------------------------------------------------
    #  basic accessors
    # ------------------------------------------------------------------
    def get(self, dotted, default=None):
        sec, _, key = dotted.partition(".")
        try:
            return self._data[sec][key]
        except KeyError:
            return default

    def set(self, dotted, value, notify=True):
        spec = _FLAT.get(dotted)
        sec, _, key = dotted.partition(".")
        if spec is None or sec not in self._data:
            raise KeyError(dotted)

        old = self._data[sec].get(key)
        new = spec.coerce(value)
        self._data[sec][key] = new

        if old != new:
            if spec.restart:
                self._dirty_restart = True
            self._key_cache.clear()
            if notify:
                for cb in list(self._listeners):
                    try:
                        cb(dotted, new)
                    except Exception:
                        traceback.print_exc()
            self._on_change(dotted, new)

        return new

    def spec(self, dotted):
        return _FLAT.get(dotted)

    def sections(self):
        return list(SCHEMA.keys())

    def options(self, section):
        return list(SCHEMA.get(section, {}).keys())

    def reset_all(self):
        self._data = self._defaults()
        self._key_cache.clear()
        self._dirty_restart = True
        for cb in list(self._listeners):
            try:
                cb("*", None)
            except Exception:
                traceback.print_exc()
        self._apply_live_audio()

    def reset_section(self, section):
        if section not in SCHEMA:
            return
        for key, spec in SCHEMA[section].items():
            self.set("{}.{}".format(section, key), copy.deepcopy(spec.default))

    # ------------------------------------------------------------------
    #  dirty / restart tracking
    # ------------------------------------------------------------------
    @property
    def dirty(self):
        """True when in‑memory values differ from the on‑disk snapshot."""
        return json.dumps(self._data, sort_keys=True) != self._loaded_snapshot

    @property
    def restart_required(self):
        return self._dirty_restart

    def clear_restart_flag(self):
        self._dirty_restart = False

    # ------------------------------------------------------------------
    #  listeners
    # ------------------------------------------------------------------
    def subscribe(self, fn):
        """Register *fn(key, value)* to be called whenever a value changes."""
        self._listeners.append(fn)
        return fn

    def unsubscribe(self, fn):
        try:
            self._listeners.remove(fn)
        except ValueError:
            pass

    # ------------------------------------------------------------------
    #  key‑binding helpers
    # ------------------------------------------------------------------
    def keys(self, action):
        """Return the pygame key‑codes bound to *action* (e.g. ``"move_up"``).

        The result is cached until any binding changes.  Unknown key
        names are silently skipped so a hand‑edited config with a typo
        never crashes event handling.
        """
        if action in self._key_cache:
            return self._key_cache[action]

        import pygame  # local import keeps settings importable w/o pygame init

        names = self._data.get("controls", {}).get(action, [])
        codes = []
        for n in names:
            try:
                if isinstance(n, int):
                    codes.append(int(n))
                else:
                    codes.append(pygame.key.key_code(str(n)))
            except Exception:
                pass
        self._key_cache[action] = codes
        return codes

    def bind_key(self, action, key_code, replace_primary=True):
        """Bind *key_code* (pygame int) to *action*.

        When *replace_primary* is True the new key becomes the single
        primary binding; otherwise it is appended as a secondary one.
        The storage format stays key‑*names* so the JSON stays readable.
        """
        import pygame

        try:
            name = pygame.key.name(int(key_code))
        except Exception:
            name = str(key_code)

        dotted = "controls.{}".format(action)
        spec = _FLAT.get(dotted)
        if spec is None or spec.kind != "key":
            raise KeyError("{} is not a key binding".format(action))

        current = list(self._data["controls"].get(action, []))
        if replace_primary:
            current = [name]
        elif name not in current:
            current.append(name)

        self.set(dotted, current)

    def key_label(self, action):
        """Human‑readable string for a binding (``"W / Up"``)."""
        names = self._data.get("controls", {}).get(action, [])
        pretty = [str(n).replace("_", " ").title() for n in names]
        return " / ".join(pretty) if pretty else "— unbound —"

    # ------------------------------------------------------------------
    #  live‑apply hooks
    # ------------------------------------------------------------------
    def _on_change(self, dotted, value):
        """Immediate side‑effects for settings that support live update."""
        if dotted.startswith("audio.") or dotted == "*":
            self._apply_live_audio()
        if dotted == "controls.mouse_look":
            try:
                from . import const
                const.DISABLE_MOUSE_LOOK = 0 if value else 1
            except Exception:
                pass

    def _apply_live_audio(self):
        """Push current audio levels to pygame's mixer if it's alive."""
        try:
            import pygame
            if not pygame.mixer or not pygame.mixer.get_init():
                return
            mute = bool(self.get("audio.mute", False))
            music = 0.0 if mute else float(self.get("audio.music_volume", 0.8))
            try:
                pygame.mixer.music.set_volume(music)
            except Exception:
                pass
        except Exception:
            pass

    # ------------------------------------------------------------------
    #  convenience high‑level getters  (used by const.py / main.py)
    # ------------------------------------------------------------------
    def resolution(self):
        r = self.get("display.resolution", (640, 480))
        try:
            w, h = int(r[0]), int(r[1])
            return max(320, w), max(240, h)
        except Exception:
            return 640, 480

    def fps_cap(self):
        return int(self.get("display.fps_cap", 30) or 30)

    def fullscreen(self):
        return bool(self.get("display.fullscreen", False))

    def skip_intro(self):
        return bool(self.get("display.skip_intro", False))

    def music_volume(self):
        if self.get("audio.mute", False):
            return 0.0
        return float(self.get("audio.music_volume", 0.8))

    def sfx_volume(self):
        if self.get("audio.mute", False):
            return 0.0
        return float(self.get("audio.sfx_volume", 1.0))

    # ------------------------------------------------------------------
    #  export / import
    # ------------------------------------------------------------------
    def export_copy(self):
        """Deep‑copy the current values (useful for a *Cancel* button)."""
        return copy.deepcopy(self._data)

    def import_copy(self, data):
        """Restore values from a previous :meth:`export_copy` result."""
        self._merge(data)
        self._key_cache.clear()
        self._apply_live_audio()


# ---------------------------------------------------------------------------
#  module‑level singleton  +  thin module‑function façade
# ---------------------------------------------------------------------------

_instance = Settings().load()


def get(dotted, default=None):
    return _instance.get(dotted, default)


def set(dotted, value):              # noqa: A001  (intentional shadow of builtin)
    return _instance.set(dotted, value)


def save():
    return _instance.save()


def load():
    return _instance.load()


def reset_all():
    return _instance.reset_all()


def keys(action):
    return _instance.keys(action)


def bind_key(action, key_code, replace_primary=True):
    return _instance.bind_key(action, key_code, replace_primary)


def key_label(action):
    return _instance.key_label(action)


def spec(dotted):
    return _instance.spec(dotted)


def sections():
    return _instance.sections()


def options(section):
    return _instance.options(section)


def subscribe(fn):
    return _instance.subscribe(fn)


def unsubscribe(fn):
    return _instance.unsubscribe(fn)


def resolution():
    return _instance.resolution()


def fps_cap():
    return _instance.fps_cap()


def fullscreen():
    return _instance.fullscreen()


def skip_intro():
    return _instance.skip_intro()


def music_volume():
    return _instance.music_volume()


def sfx_volume():
    return _instance.sfx_volume()


def export_copy():
    return _instance.export_copy()


def import_copy(data):
    return _instance.import_copy(data)


def restart_required():
    return _instance.restart_required


def clear_restart_flag():
    return _instance.clear_restart_flag()


def dirty():
    return _instance.dirty
