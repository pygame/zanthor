"""
zanthor.options
===============

The in‑game **Options** screen.

Visual design
-------------
The screen deliberately echoes Zanthor's existing title / menu look & feel:

* The parchment‑and‑brass colour palette (cream, gold, black outlines)
  matches the ``mybkgr.png`` art, which is reused as a dimmed backdrop.
* All text is rendered with the game's ``vinque.ttf`` fantasy font and the
  same black‑halo outline helper (:func:`pgu.text.write`) used everywhere
  else.
* Tabs are laid out along the top, options in a brass‑trimmed card on the
  left, and a live description / value panel on the right.

Interaction design
------------------
* **Mouse** – click tabs to switch section, click an option to select
  it, click **again** (or click the value column) to edit / toggle.
  Dragging on a slider live‑updates the value.  Bottom buttons for
  *Save*, *Reset Section*, *Defaults* and *Back*.
* **Keyboard** – ``Tab / Shift+Tab`` cycles tabs, ``↑ / ↓`` moves the
  selection, ``← / →`` adjusts, ``Enter`` toggles / starts a key‑rebind,
  ``Esc`` goes back (also cancels an in‑progress rebind).

All widgets are hand‑drawn – no external GUI toolkit – so the module is
drop‑in with zero extra dependencies.
"""

import math

import pygame
from pygame.locals import (
    KEYDOWN,
    KEYUP,
    K_DOWN,
    K_ESCAPE,
    K_LEFT,
    K_RETURN,
    K_RIGHT,
    K_SPACE,
    K_TAB,
    K_UP,
    K_BACKSPACE,
    K_DELETE,
    KMOD_SHIFT,
    MOUSEBUTTONDOWN,
    MOUSEBUTTONUP,
    MOUSEMOTION,
)

from .pgu import engine
from .pgu import text as pgu_text
from .const import data_dir, SW, SH
from . import settings


# ---------------------------------------------------------------------------
#  Colour palette  (steampunk parchment / brass)
# ---------------------------------------------------------------------------

C_BG_OVERLAY = (0, 0, 0, 130)      # dim overlay on top of parchment

C_TITLE = (255, 232, 170)          # warm gold
C_TEXT = (240, 230, 210)           # cream
C_TEXT_DIM = (150, 140, 120)       # inactive label

C_ACCENT = (255, 175, 64)          # brass highlight
C_ACCENT_DARK = (170, 110, 40)     # brass shadow
C_PANEL = (26, 22, 18, 215)        # dark brown semi‑opaque card
C_PANEL_BORDER = (90, 68, 38)

C_SLIDER_TRACK = (70, 55, 40)
C_SLIDER_FILL = (200, 145, 60)
C_SLIDER_KNOB = (255, 220, 170)

C_TOGGLE_ON = (92, 190, 80)
C_TOGGLE_OFF = (120, 60, 50)

C_BUTTON = (50, 40, 30)
C_BUTTON_HOVER = (80, 60, 40)
C_RESTART = (255, 96, 96)          # small restart badge


# ---------------------------------------------------------------------------
#  Tiny drawing helpers
# ---------------------------------------------------------------------------

def _round_rect(surface, color, rect, radius=8, width=0):
    """Anti‑aliased rounded rectangle (filled when *width* == 0)."""
    try:
        pygame.draw.rect(surface, color, rect, width=width, border_radius=radius)
    except TypeError:  # pygame <2 fallback
        pygame.draw.rect(surface, color, rect, width)


def _panel(surface, rect, radius=10):
    """Draw a dark semi‑transparent card with a brass border."""
    panel = pygame.Surface(rect.size, pygame.SRCALPHA)
    _round_rect(panel, C_PANEL, panel.get_rect(), radius)
    surface.blit(panel, rect.topleft)
    _round_rect(surface, C_PANEL_BORDER, rect, radius, width=2)


def _outline_text(surface, font, pos, color, txt, border=2):
    pgu_text.write(surface, font, pos, color, txt, border)


def _text_size(font, txt):
    return font.size(txt)


# ---------------------------------------------------------------------------
#  The Options State
# ---------------------------------------------------------------------------

class Options(engine.State):
    """Full‑screen configuration editor, reachable from the title menu."""

    # ------------------------------------------------------------------ #
    #  life‑cycle
    # ------------------------------------------------------------------ #
    def init(self):
        # ---- fonts
        self.font_title = pygame.font.Font(data_dir("menu", "vinque.ttf"), 42)
        self.font_tab = pygame.font.Font(data_dir("menu", "vinque.ttf"), 26)
        self.font_opt = pygame.font.Font(data_dir("menu", "vinque.ttf"), 22)
        self.font_small = pygame.font.Font(data_dir("menu", "vinque.ttf"), 16)

        # ---- background: parchment dimmed with a dark overlay
        try:
            bg = pygame.image.load(data_dir("intro", "mybkgr.png")).convert()
            bg = pygame.transform.scale(bg, (SW, SH))
        except Exception:
            bg = pygame.Surface((SW, SH))
            bg.fill((28, 22, 18))
        overlay = pygame.Surface((SW, SH), pygame.SRCALPHA)
        overlay.fill(C_BG_OVERLAY)
        bg.blit(overlay, (0, 0))
        self.bkgr = bg

        # ---- state
        self.tabs = settings.sections()          # e.g. ['display', 'audio', ...]
        self.tab_idx = 0
        self.sel_idx = 0
        self.hover_idx = None
        self.scroll = 0                          # first visible row index

        self.rebinding = None                    # action name while waiting for key
        self.slider_drag = None                  # (dotted, rect) while dragging
        self.flash = ""                          # transient status line
        self.flash_timer = 0

        # Snapshot so the user can *Cancel* (leave via Esc with unsaved changes
        # and optionally revert – we revert only on explicit *Back w/o Save*
        # prompt; currently we simply auto‑save on *Save* and leave values
        # in memory on *Back*).
        self._snapshot = settings.export_copy()

        # Geometry --------------------------------------------------------
        pad = int(SW * 0.03)
        self.r_title = pygame.Rect(pad, pad, SW - 2 * pad, 50)
        self.r_tabs = pygame.Rect(pad, self.r_title.bottom + 4, SW - 2 * pad, 42)
        body_top = self.r_tabs.bottom + 12
        body_h = SH - body_top - 72
        opt_w = int((SW - 2 * pad) * 0.58)
        self.r_opts = pygame.Rect(pad, body_top, opt_w, body_h)
        self.r_desc = pygame.Rect(
            self.r_opts.right + 12, body_top, SW - pad - self.r_opts.right - 12, body_h
        )
        self.r_buttons = pygame.Rect(pad, SH - 64, SW - 2 * pad, 56)

        # Per‑frame layout caches (rebuilt each paint)
        self._tab_rects = []
        self._opt_rects = []     # list of (dotted, label_rect, value_rect, spec)
        self._btn_rects = {}     # name -> rect

        self.frame = 0
        pygame.mouse.set_visible(True)
        pygame.key.set_repeat(350, 40)

    # ------------------------------------------------------------------ #
    #  drawing
    # ------------------------------------------------------------------ #
    def paint(self, screen):
        screen.blit(self.bkgr, (0, 0))

        # --- Title --------------------------------------------------------
        _outline_text(
            screen,
            self.font_title,
            (self.r_title.x, self.r_title.y),
            C_TITLE,
            "Options",
            border=2,
        )

        # --- Tabs ---------------------------------------------------------
        self._draw_tabs(screen)

        # --- Option panel -------------------------------------------------
        _panel(screen, self.r_opts)
        self._draw_options(screen)

        # --- Description panel -------------------------------------------
        _panel(screen, self.r_desc)
        self._draw_description(screen)

        # --- Buttons ------------------------------------------------------
        self._draw_buttons(screen)

        # --- Flash / status ----------------------------------------------
        if self.flash and self.flash_timer > 0:
            _outline_text(
                screen,
                self.font_small,
                (self.r_buttons.x + 8, self.r_buttons.y - 22),
                C_ACCENT,
                self.flash,
            )

        # --- Key‑rebind overlay ------------------------------------------
        if self.rebinding:
            self._draw_rebind_overlay(screen)

        pygame.display.flip()

    def update(self, screen):
        self.paint(screen)

    def loop(self):
        self.frame += 1
        if self.flash_timer > 0:
            self.flash_timer -= 1

    # .................................................................. #
    #  sub‑drawers
    # .................................................................. #
    def _draw_tabs(self, screen):
        self._tab_rects = []
        x = self.r_tabs.x
        y = self.r_tabs.y
        gap = 14
        for i, sec in enumerate(self.tabs):
            label = sec.title()
            w, h = _text_size(self.font_tab, label)
            pad = 14
            r = pygame.Rect(x, y, w + pad * 2, h + 10)
            active = i == self.tab_idx

            # tab background
            fill = C_ACCENT_DARK if active else C_BUTTON
            _round_rect(screen, fill, r, radius=8)
            if active:
                _round_rect(screen, C_ACCENT, r, radius=8, width=2)
                # little brass underline pointing to the panel
                pygame.draw.line(
                    screen,
                    C_ACCENT,
                    (r.x + 6, r.bottom),
                    (r.right - 6, r.bottom),
                    3,
                )

            col = C_TITLE if active else C_TEXT_DIM
            _outline_text(
                screen, self.font_tab, (r.x + pad, r.y + 4), col, label, border=1
            )

            self._tab_rects.append((i, r))
            x = r.right + gap

    def _draw_options(self, screen):
        """Render visible options in the active section (scrolling)."""
        sec = self.tabs[self.tab_idx]
        opts = settings.options(sec)

        self._opt_rects = []
        x0 = self.r_opts.x + 16
        top = self.r_opts.y + 14
        row_h = max(32, self.font_opt.get_height() + 10)
        label_w = int(self.r_opts.w * 0.50)
        visible = max(1, (self.r_opts.h - 28) // row_h)

        # Clamp / auto-scroll so the selected row is always on screen.
        self.scroll = max(0, min(self.scroll, max(0, len(opts) - visible)))
        if self.sel_idx < self.scroll:
            self.scroll = self.sel_idx
        elif self.sel_idx >= self.scroll + visible:
            self.scroll = self.sel_idx - visible + 1

        # Clip to the panel so overflowing text never bleeds.
        old_clip = screen.get_clip()
        clip = pygame.Rect(
            self.r_opts.x + 4, self.r_opts.y + 4,
            self.r_opts.w - 8, self.r_opts.h - 8,
        )
        screen.set_clip(clip)

        y = top
        first, last = self.scroll, min(len(opts), self.scroll + visible)
        for i in range(first, last):
            key = opts[i]
            dotted = "{}.{}".format(sec, key)
            spec = settings.spec(dotted)
            val = settings.get(dotted)

            sel = i == self.sel_idx
            hov = i == self.hover_idx

            r_row = pygame.Rect(x0 - 6, y - 4, self.r_opts.w - 20, row_h)
            if sel:
                hl = pygame.Surface(r_row.size, pygame.SRCALPHA)
                hl.fill((255, 200, 120, 36))
                screen.blit(hl, r_row.topleft)
                _round_rect(screen, C_ACCENT, r_row, radius=6, width=1)
            elif hov:
                hl = pygame.Surface(r_row.size, pygame.SRCALPHA)
                hl.fill((255, 255, 255, 14))
                screen.blit(hl, r_row.topleft)

            # label --------------------------------------------------
            label_col = C_TEXT if (sel or hov) else C_TEXT_DIM
            lab = self._ellipsize(spec.label, self.font_opt, label_w - 10)
            _outline_text(
                screen, self.font_opt, (x0, y), label_col, lab, border=1
            )
            if spec.restart:
                _outline_text(
                    screen,
                    self.font_small,
                    (x0 + _text_size(self.font_opt, lab)[0] + 6, y),
                    C_RESTART,
                    "*",
                    border=1,
                )

            # value widget ------------------------------------------
            r_val = pygame.Rect(
                x0 + label_w, y - 2,
                self.r_opts.w - label_w - 30, row_h - 6,
            )
            self._draw_value(screen, dotted, spec, val, r_val, sel)

            self._opt_rects.append((dotted, r_row, r_val, spec, i))
            y += row_h

        screen.set_clip(old_clip)

        # Scroll arrows ---------------------------------------------
        if first > 0:
            self._draw_scroll_hint(screen, self.r_opts.centerx, self.r_opts.y + 6, up=True)
        if last < len(opts):
            self._draw_scroll_hint(screen, self.r_opts.centerx, self.r_opts.bottom - 6, up=False)

    @staticmethod
    def _ellipsize(text, font, max_w):
        """Truncate *text* with a trailing ellipsis until it fits in *max_w*."""
        if font.size(text)[0] <= max_w:
            return text
        ell = ".."
        out = text
        while out and font.size(out + ell)[0] > max_w:
            out = out[:-1]
        return (out + ell) if out else ell

    @staticmethod
    def _draw_scroll_hint(screen, cx, cy, up):
        """Tiny chevron indicating more content above/below."""
        d = -1 if up else 1
        pts = [(cx - 7, cy - 4 * d), (cx + 7, cy - 4 * d), (cx, cy + 4 * d)]
        pygame.draw.polygon(screen, C_ACCENT, pts)
        pygame.draw.polygon(screen, (0, 0, 0), pts, 1)


    def _draw_value(self, screen, dotted, spec, val, rect, selected):
        """Render the right‑hand side widget for one option."""
        kind = spec.kind

        if kind == "toggle":
            # pill‑style switch
            pill = pygame.Rect(rect.x, rect.y + rect.h // 2 - 10, 46, 20)
            col = C_TOGGLE_ON if val else C_TOGGLE_OFF
            _round_rect(screen, col, pill, radius=10)
            knob_x = pill.right - 12 if val else pill.x + 12
            pygame.draw.circle(screen, C_SLIDER_KNOB, (knob_x, pill.centery), 9)
            txt = "On" if val else "Off"
            _outline_text(
                screen,
                self.font_small,
                (pill.right + 10, pill.y),
                C_TEXT,
                txt,
                border=1,
            )

        elif kind == "slider":
            track = pygame.Rect(rect.x, rect.centery - 4, rect.w - 60, 8)
            _round_rect(screen, C_SLIDER_TRACK, track, radius=4)
            rng = (spec.vmax - spec.vmin) or 1.0
            pct = (float(val) - spec.vmin) / rng
            pct = max(0.0, min(1.0, pct))
            fill = pygame.Rect(track.x, track.y, int(track.w * pct), track.h)
            _round_rect(screen, C_SLIDER_FILL, fill, radius=4)
            knob_x = track.x + int(track.w * pct)
            pygame.draw.circle(screen, C_SLIDER_KNOB, (knob_x, track.centery), 8)
            pygame.draw.circle(screen, C_ACCENT_DARK, (knob_x, track.centery), 8, 1)
            txt = "{:.0%}".format(pct) if spec.vmax == 1.0 else str(val)
            _outline_text(
                screen,
                self.font_small,
                (track.right + 10, track.y - 4),
                C_TEXT,
                txt,
                border=1,
            )
            # stash track for drag handling
            rect.w = track.w  # shrink hit‑rect to the track itself
            rect.x = track.x
            rect.h = 18
            rect.y = track.y - 5

        elif kind == "choice":
            # < Value > stepper with arrow markers on each side when selected
            s_val = self._fmt_choice(val)
            if selected:
                s_val = "<  {}  >".format(s_val)
            _outline_text(
                screen, self.font_opt, (rect.x, rect.y), C_ACCENT, s_val, border=1
            )

        elif kind == "int":
            s_val = str(val)
            if selected:
                s_val = "<  {}  >".format(s_val)
            _outline_text(
                screen, self.font_opt, (rect.x, rect.y), C_ACCENT, s_val, border=1
            )

        elif kind == "key":
            action = dotted.split(".", 1)[1]
            s_val = settings.key_label(action)
            # Long multi-bindings ("Space / F / Left Ctrl / Right Ctrl")
            # would spill past the panel – trim with an ellipsis.
            s_val = self._ellipsize(s_val, self.font_opt, rect.w)
            col = C_ACCENT if selected else C_TEXT
            _outline_text(screen, self.font_opt, (rect.x, rect.y), col, s_val, border=1)

        else:
            _outline_text(
                screen, self.font_opt, (rect.x, rect.y), C_TEXT, str(val), border=1
            )

    @staticmethod
    def _fmt_choice(val):
        if isinstance(val, (list, tuple)) and len(val) == 2:
            return "{} x {}".format(val[0], val[1])
        return str(val)

    def _draw_description(self, screen):
        sec = self.tabs[self.tab_idx]
        opts = settings.options(sec)
        if not opts:
            return
        idx = max(0, min(self.sel_idx, len(opts) - 1))
        dotted = "{}.{}".format(sec, opts[idx])
        spec = settings.spec(dotted)

        x = self.r_desc.x + 14
        y = self.r_desc.y + 12
        _outline_text(screen, self.font_opt, (x, y), C_TITLE, spec.label, border=1)
        y += self.font_opt.get_height() + 8

        # word‑wrapped description
        desc = spec.desc or ""
        max_w = self.r_desc.w - 28
        for line in self._wrap(desc, self.font_small, max_w):
            _outline_text(screen, self.font_small, (x, y), C_TEXT, line, border=1)
            y += self.font_small.get_height() + 2

        if spec.restart:
            y += 10
            _outline_text(
                screen,
                self.font_small,
                (x, y),
                C_RESTART,
                "* restart required",
                border=1,
            )

        # -- footer: config file location
        y = self.r_desc.bottom - 60
        _outline_text(
            screen,
            self.font_small,
            (x, y),
            C_TEXT_DIM,
            "Config file:",
            border=1,
        )
        # cut off long paths gracefully
        path = settings._instance.config_path
        short = path
        if len(short) > 48:
            short = "…" + short[-46:]
        _outline_text(
            screen,
            self.font_small,
            (x, y + self.font_small.get_height() + 2),
            C_TEXT_DIM,
            short,
            border=1,
        )

    @staticmethod
    def _wrap(text, font, max_w):
        if not text:
            return []
        words = text.split(" ")
        out, line = [], ""
        for w in words:
            test = (line + " " + w).strip()
            if font.size(test)[0] <= max_w:
                line = test
            else:
                if line:
                    out.append(line)
                line = w
        if line:
            out.append(line)
        return out

    def _draw_buttons(self, screen):
        self._btn_rects = {}
        labels = [
            ("save", "Save"),
            ("reset_sec", "Reset Tab"),
            ("defaults", "Defaults"),
            ("back", "Back"),
        ]
        n = len(labels)
        gap = 12
        bw = (self.r_buttons.w - gap * (n - 1)) // n
        bh = self.r_buttons.h - 12
        x = self.r_buttons.x
        y = self.r_buttons.y + 6

        mouse = pygame.mouse.get_pos()
        for key, text in labels:
            r = pygame.Rect(x, y, bw, bh)
            hov = r.collidepoint(mouse)
            fill = C_BUTTON_HOVER if hov else C_BUTTON
            _round_rect(screen, fill, r, radius=8)
            border_col = C_ACCENT if hov else C_PANEL_BORDER
            _round_rect(screen, border_col, r, radius=8, width=2)
            tw, th = _text_size(self.font_opt, text)
            _outline_text(
                screen,
                self.font_opt,
                (r.centerx - tw // 2, r.centery - th // 2),
                C_TEXT,
                text,
                border=1,
            )
            self._btn_rects[key] = r
            x += bw + gap

        # Restart‑required badge
        if settings.restart_required():
            msg = "Some changes take effect after restart"
            tw, th = self.font_small.size(msg)
            _outline_text(
                screen,
                self.font_small,
                (self.r_buttons.right - tw - 4, self.r_buttons.y - th - 4),
                C_RESTART,
                msg,
                border=1,
            )

    def _draw_rebind_overlay(self, screen):
        overlay = pygame.Surface((SW, SH), pygame.SRCALPHA)
        overlay.fill((0, 0, 0, 170))
        screen.blit(overlay, (0, 0))

        box_w, box_h = int(SW * 0.6), 120
        r = pygame.Rect((SW - box_w) // 2, (SH - box_h) // 2, box_w, box_h)
        _panel(screen, r, radius=12)

        action = self.rebinding
        spec = settings.spec("controls.{}".format(action))
        title = "Rebind: {}".format(spec.label if spec else action)
        tw, _ = self.font_opt.size(title)
        _outline_text(
            screen,
            self.font_opt,
            (r.centerx - tw // 2, r.y + 16),
            C_TITLE,
            title,
            border=1,
        )
        sub = "Press any key…  (Esc to cancel · Backspace to clear)"
        sw, _ = self.font_small.size(sub)
        _outline_text(
            screen,
            self.font_small,
            (r.centerx - sw // 2, r.y + 56),
            C_TEXT,
            sub,
            border=1,
        )
        pygame.display.flip()

    # ------------------------------------------------------------------ #
    #  events
    # ------------------------------------------------------------------ #
    def event(self, e):
        # ------------------------------------------------ rebind capture
        if self.rebinding:
            if e.type == KEYDOWN:
                if e.key == K_ESCAPE:
                    self.rebinding = None
                elif e.key in (K_BACKSPACE, K_DELETE):
                    settings.set("controls.{}".format(self.rebinding), [])
                    self._flash("Cleared binding for {}".format(self.rebinding))
                    self.rebinding = None
                else:
                    settings.bind_key(self.rebinding, e.key, replace_primary=True)
                    self._flash(
                        "Bound {} → {}".format(
                            self.rebinding, pygame.key.name(e.key)
                        )
                    )
                    self.rebinding = None
            return  # eat everything else while rebinding

        # ------------------------------------------------ mouse
        if e.type == MOUSEMOTION:
            self._update_hover(e.pos)
            if self.slider_drag:
                self._drag_slider(e.pos)

        elif e.type == MOUSEBUTTONDOWN and e.button == 1:
            return self._handle_click(e.pos)

        elif e.type == MOUSEBUTTONDOWN and e.button == 4:
            # mouse wheel up – scroll the options list
            self.scroll = max(0, self.scroll - 1)

        elif e.type == MOUSEBUTTONDOWN and e.button == 5:
            # mouse wheel down
            self.scroll += 1  # clamped in _draw_options

        elif e.type == MOUSEBUTTONUP and e.button == 1:
            self.slider_drag = None

        # ------------------------------------------------ keyboard
        elif e.type == KEYDOWN:
            if e.key == K_ESCAPE:
                return self._go_back()

            if e.key == K_TAB:
                delta = -1 if (e.mod & KMOD_SHIFT) else 1
                self._switch_tab(delta)

            elif e.key == K_UP:
                self._move_selection(-1)

            elif e.key == K_DOWN:
                self._move_selection(+1)

            elif e.key == K_LEFT:
                self._adjust(-1)

            elif e.key == K_RIGHT:
                self._adjust(+1)

            elif e.key in (K_RETURN, K_SPACE):
                self._activate()

    # .................................................................. #
    #  event helpers
    # .................................................................. #
    def _update_hover(self, pos):
        self.hover_idx = None
        for (dotted, row, rv, spec, idx) in self._opt_rects:
            if row.collidepoint(pos):
                self.hover_idx = idx
                break

    def _handle_click(self, pos):
        # tabs
        for i, r in self._tab_rects:
            if r.collidepoint(pos):
                self.tab_idx = i
                self.sel_idx = 0
                self.hover_idx = None
                self.scroll = 0
                return

        # option rows
        for (dotted, row, rv, spec, idx) in self._opt_rects:
            if row.collidepoint(pos):
                was_sel = self.sel_idx == idx
                self.sel_idx = idx
                if spec.kind == "slider" and rv.collidepoint(pos):
                    self.slider_drag = (dotted, rv)
                    self._drag_slider(pos)
                    return
                if was_sel or rv.collidepoint(pos):
                    self._activate()
                return

        # buttons
        for name, r in self._btn_rects.items():
            if r.collidepoint(pos):
                return self._button_action(name)

    def _drag_slider(self, pos):
        dotted, rv = self.slider_drag
        spec = settings.spec(dotted)
        rng = (spec.vmax - spec.vmin) or 1.0
        pct = (pos[0] - rv.x) / max(1, rv.w)
        pct = max(0.0, min(1.0, pct))
        val = spec.vmin + pct * rng
        if spec.step:
            val = round(val / spec.step) * spec.step
        settings.set(dotted, val)

    def _button_action(self, name):
        if name == "save":
            settings.save()
            self._snapshot = settings.export_copy()
            self._flash("Settings saved.")
        elif name == "reset_sec":
            settings.reset_section(self.tabs[self.tab_idx])
            self._flash("Tab reset to defaults.")
        elif name == "defaults":
            settings.reset_all()
            self._flash("All settings reset to defaults.")
        elif name == "back":
            return self._go_back()

    def _go_back(self):
        pygame.key.set_repeat()        # turn off key repeat outside the menu
        # Auto‑save on exit so players aren't surprised by lost changes.
        if settings.dirty():
            settings.save()
            self._flash("Settings saved.")
        from . import title
        return title.Title(self.game)

    def _switch_tab(self, delta):
        self.tab_idx = (self.tab_idx + delta) % len(self.tabs)
        self.sel_idx = 0
        self.hover_idx = None
        self.scroll = 0

    def _move_selection(self, delta):
        n = len(settings.options(self.tabs[self.tab_idx]))
        if n:
            self.sel_idx = (self.sel_idx + delta) % n

    # .................................................................. #
    #  value editing
    # .................................................................. #
    def _current(self):
        sec = self.tabs[self.tab_idx]
        opts = settings.options(sec)
        if not opts:
            return None, None
        key = opts[max(0, min(self.sel_idx, len(opts) - 1))]
        dotted = "{}.{}".format(sec, key)
        return dotted, settings.spec(dotted)

    def _adjust(self, delta):
        dotted, spec = self._current()
        if spec is None:
            return
        val = settings.get(dotted)

        if spec.kind == "toggle":
            settings.set(dotted, not val)

        elif spec.kind == "slider":
            step = spec.step or 0.05
            settings.set(dotted, val + step * delta)

        elif spec.kind == "int":
            step = spec.step or 1
            settings.set(dotted, val + step * delta)

        elif spec.kind == "choice":
            choices = spec.choices or [val]
            try:
                idx = 0
                for n, c in enumerate(choices):
                    if (
                        val == c
                        or list(val) == list(c)
                        or tuple(val) == tuple(c)
                    ):
                        idx = n
                        break
            except Exception:
                idx = 0
            idx = (idx + delta) % len(choices)
            settings.set(dotted, choices[idx])

        elif spec.kind == "key":
            # keys are edited via Enter → rebind overlay
            pass

    def _activate(self):
        """Primary action on Enter / Space / mouse click."""
        dotted, spec = self._current()
        if spec is None:
            return
        if spec.kind == "toggle":
            settings.set(dotted, not settings.get(dotted))
        elif spec.kind == "key":
            self.rebinding = dotted.split(".", 1)[1]
        elif spec.kind in ("choice", "int", "slider"):
            self._adjust(+1)

    def _flash(self, msg):
        self.flash = msg
        self.flash_timer = 90  # ~3 s at 30 fps
