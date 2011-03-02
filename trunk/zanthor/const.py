""" this file has lots of tweaky things in it.

Tweakable files (other) :
    sound_info.py - tweaking sounds.
    units.py - tweaking unit stats.

"""


import pygame

import os
_DATA_DIR = None
def data_dir(*args):
    global _DATA_DIR
    if _DATA_DIR is None:
        #_DATA_DIR = os.path.join(*(['zanthor', 'data'] + list(args)))
        _DATA_DIR = os.path.join('zanthor', 'data')
        if not os.path.exists(_DATA_DIR):
            _DATA_DIR = os.path.join(os.path.split(__file__)[0], 'data')
    return os.path.join(*([_DATA_DIR] + list(args)))

# the base size.
BSW,BSH = 640,480
SW,SH = 640,480
SW,SH = 320,200
SW,SH = 800,600
SW,SH = 1280,800
SW,SH = 1024,768

DX = float(SW) / BSW
DY = float(SH) / BSH

dxdy = (DX, DY)

FPS = 30

MIN_CANNON_PRESSURE = 6

def multr(dx_dy, r):
    a,b,c,d = tuple(r)
    dx,dy = dxdy
    return pygame.Rect(a*dx, b*dy, c*dx, d*dy)
    

#S_VIEW = pygame.Rect(0,0,480,480)


S_STATUS = multr( dxdy, (480,320,400,160))

S_ITEMS = multr( dxdy, (480,160,160,200))
S_STATUS = multr( dxdy, (480,360,160,120))




# game view area.
S_VIEW = multr( dxdy, (76,0,380,340))


# left side, full status area.
S_STATUS = multr( dxdy, (0,0,76,340) )


# left side status boxes.
#S_HEALTH = pygame.Rect(10,30,60,70)
S_HEALTH = multr( dxdy, (10,4,60,96) )
S_COAL   = multr( dxdy, (10,100,60,70) )
S_WATER  = multr( dxdy, (10,190,60,70) )
S_STEAM  = multr( dxdy, (10,260,60,70) )

S_PEASANTS_REMAINING = multr( dxdy, (487,24,122,114) )
S_CANNON_PRESSURE = multr( dxdy, (76,0,5,340) )





# top right,  castle robot illustration area.
S_ROBOT = multr( dxdy, (456,0,184,163) )


# middle right, items area.
S_ITEMS = multr( dxdy, (456,163,184,177) )


S_ITEMS_ENGINE = multr( dxdy, (480,160,160,160) )
S_ITEMS_COALSTORAGEROOM = multr( dxdy, (480,160,160,160) )
S_ITEMS_WATERTANK = multr( dxdy, (480,160,160,160) )
S_ITEMS_CANNON = multr( dxdy, (480,160,160,160) )
S_ITEMS_ARMOUR = multr( dxdy, (480,160,160,160) )




# bottom right,  button area.
S_BUTTONS = pygame.Rect(470,340,170,140)

S_BUTTONS_SAVE = pygame.Rect(490,360,60,40)
S_BUTTONS_LOAD = pygame.Rect(490,420,60,40)
S_BUTTONS_QUIT = pygame.Rect(560,360,60,40)
S_BUTTONS_NEWS = pygame.Rect(560,420,60,40)

S_BOTTOM = pygame.Rect(0,340,640,140)

S_BUTTONS, S_BUTTONS_SAVE, S_BUTTONS_LOAD, S_BUTTONS_QUIT, S_BUTTONS_NEWS, S_BOTTOM, = map(lambda x:multr(dxdy, x), [S_BUTTONS, S_BUTTONS_SAVE, S_BUTTONS_LOAD, S_BUTTONS_QUIT, S_BUTTONS_NEWS, S_BOTTOM])






S_BOTTOM_BUTTONS = multr(dxdy, (470,0,170,140))
S_BOTTOM_MESSAGES = multr(dxdy, (95,25,355,110))
# bottom middle message area.
S_MESSAGES = multr(dxdy, (95,365,355,110))

#S_NEXT_LEVEL_MESSAGES = pygame.Rect(20,165,380,410)
S_NEXT_LEVEL_MESSAGES = multr( dxdy, (20,20,500,410))



S_= pygame.Rect(480,360,160,120)



UPGRADE_FUN = 1

CACHE_USE_LEVEL_CACHE = 1

# if you are modifying just the tiles or just the levels set one of these to 0.
#  These only check the levels, 
#    or the tiles to see if its older than the cache.
CACHE_CHECK_TILES = 1
CACHE_CHECK_LEVEL = 1


# joystick buttons
JOY_FIRE_BUTTON = 1
JOY_PICKUP_BUTTON = 2

# should things be auto picked up or not?
AUTO_PICKUP = 1

#should holes that the castle hits the ground be
#solid tiles
#0 = no, 1 = yes, 2= big holes
HOLES_ARE_TILES = 0


#NOTE: mouselook seems to not work well on some systems...
#       can toggle it with the m key in game.
DISABLE_MOUSE_LOOK =0


FLOCKING_FLUCT = 1

def get_mouse_info():

    if DISABLE_MOUSE_LOOK:
        SCROLL_MOUSE = 0 #speed of mouse scroll
        SCROLL_AUTO = 9 #speed of auto-return scroll
        SCROLL_BORDER = 70 #size of scrolling border during auto-scroll
    else:
        SCROLL_MOUSE = 12 #speed of mouse scroll
        SCROLL_AUTO = 9 #speed of auto-return scroll
        SCROLL_BORDER = 160 #size of scrolling border during auto-scroll

    return [SCROLL_MOUSE, SCROLL_AUTO, SCROLL_BORDER]
