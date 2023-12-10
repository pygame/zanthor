import pygame
import math


def scale_rect(r, orig_size, size):
    width, height = size
    owidth, oheight = orig_size
    sw = width / float(owidth)
    sh = height / float(oheight)
    return pygame.Rect(
        list(
            map(int, list(map(math.ceil, [r[0] * sw, r[1] * sh, r[2] * sw, r[3] * sh])))
        )
    )
