"""
"""
import pygame
from pygame.locals import *

from .const import *
from . import widget


class Input(widget.Widget):
    """A single line text input.

    <pre>Input(value="",size=20)</pre>

    <dl>
    <dt>value<dd>initial text
    <dt>size<dd>size for the text box, in characters
    </dl>

    <strong>Example</strong>
    <code>
    w = Input(value="Cuzco the Goat",size=20)

    w = Input("Marbles")
    </code>

    """

    def __init__(self, value="", size=20, **params):
        params.setdefault("cls", "input")
        widget.Widget.__init__(self, **params)
        self.value = value
        self.pos = len(str(value))
        self.vpos = 0
        self.font = self.style.font
        w, h = self.font.size("e" * size)
        self.style.width, self.style.height = w, h
        # self.rect.w=w+self.style.padding_left+self.style.padding_right;
        # self.rect.h=h+self.style.padding_top+self.style.padding_bottom;

    def paint(self, s):
        r = pygame.Rect(0, 0, self.rect.w, self.rect.h)

        cs = 2  # NOTE: should be in a style

        w, h = self.font.size(self.value[0 : self.pos])
        x = w - self.vpos
        if x < 0:
            self.vpos -= -x
        if x + cs > s.get_width():
            self.vpos += x + cs - s.get_width()

        s.blit(self.font.render(self.value, 1, self.style.color), (-self.vpos, 0))

        if self.container.myfocus is self:
            w, h = self.font.size(self.value[0 : self.pos])
            r.x = w - self.vpos
            r.w = cs
            r.h = h
            s.fill(self.style.color, r)

    def _setvalue(self, v):
        self.__dict__["value"] = v
        self.send(CHANGE)

    def event(self, e):
        if e.type == KEYDOWN:
            if e.key == K_BACKSPACE:
                if self.pos:
                    self._setvalue(self.value[: self.pos - 1] + self.value[self.pos :])
                    self.pos -= 1
            elif e.key == K_DELETE:
                if len(self.value) > self.pos:
                    self._setvalue(self.value[: self.pos] + self.value[self.pos + 1 :])
            elif e.key == K_HOME:
                self.pos = 0
            elif e.key == K_END:
                self.pos = len(self.value)
            elif e.key == K_LEFT:
                if self.pos > 0:
                    self.pos -= 1
            elif e.key == K_RIGHT:
                if self.pos < len(self.value):
                    self.pos += 1
            elif e.key == K_RETURN:
                next(self)
            elif e.key == K_TAB:
                next(self)
            else:
                # c = str(e.unicode)
                c = (e.str).encode("latin-1")
                if c:
                    self._setvalue(self.value[: self.pos] + c + self.value[self.pos :])
                    self.pos += 1
            self.repaint()
        elif e.type == FOCUS:
            self.repaint()
        elif e.type == BLUR:
            self.repaint()

        self.pcls = ""
        if self.container.myfocus is self:
            self.pcls = "focus"

    def __setattr__(self, k, v):
        if k == "value":
            if v == None:
                v = ""
            v = str(v)
            self.pos = len(v)
        _v = self.__dict__.get(k, NOATTR)
        self.__dict__[k] = v
        if k == "value" and _v != NOATTR and _v != v:
            self.send(CHANGE)
            self.repaint()


class Password(Input):
    """A password input, text is *-ed out.

    <pre>Password(value="",size=20)</pre>

    <dl>
    <dt>value<dd>initial text
    <dt>size<dd>size for the text box, in characters
    </dl>

    <strong>Example</strong>
    <code>
    w = Password(value="password",size=20)

    w = Password("53[r3+")
    </code>

    """

    def paint(self, s):
        hidden = "*"
        show = len(self.value) * hidden

        # print "self.value:",self.value

        if self.pos == None:
            self.pos = len(self.value)

        r = pygame.Rect(0, 0, self.rect.w, self.rect.h)

        cs = 2  # NOTE: should be in a style

        w, h = self.font.size(show)
        x = w - self.vpos
        if x < 0:
            self.vpos -= -x
        if x + cs > s.get_width():
            self.vpos += x + cs - s.get_width()

        s.blit(self.font.render(show, 1, self.style.color), (-self.vpos, 0))

        if self.container.myfocus is self:
            # w,h = self.font.size(self.value[0:self.pos])
            w, h = self.font.size(show[0 : self.pos])
            r.x = w - self.vpos
            r.w = cs
            r.h = h
            s.fill(self.style.color, r)
