import isovid
import random

from const import *

from units import CannonTower

import states
import sound_info


def cannon_new(g,t,v):
    g.clayer[t.ty][t.tx] = 0
    s = isovid.Sprite(g.images['cannon'],t.rect)
    
    s.frame = random.randrange(0,FPS*3) 

    g.sprites.append(s)
    s.loop = cannon_loop
    s.hit = cannon_hit
    s.groups = g.string2groups("cannon")
    #s.agroups =g.string2groups("castle")

    s.unit = CannonTower()



def cannon_loop(g,s):
    s.unit.loop()

    tw,th = g.iso_w,g.iso_h
    if s.frame%(FPS*3) == 0:
        sx,sy = s.rect.centerx/tw,s.rect.centery/th
        p = g.castle
        px,py = p.rect.centerx/tw,p.rect.centery/th
        dx,dy = px-sx,py-sy
        if (dx*dx+dy*dy)**0.5 < 12: #only shoot if they are reachable
           # try and use some steam to fire.
            if s.unit.try_fire():
                cball_new(g,(s.rect.centerx,s.rect.centery), s.unit.stats['Damage'])
        

    s.frame += 1


def cannon_hit(g,a,b):
    pass


def cball_new(g,pos, damage = 1.0):
    g.level.game.sm.Play("cannon")

    s = isovid.Sprite(g.images['cball'],pos)
    
    s.frame = 0

    g.sprites.append(s)
    s.loop = cball_loop
    s.hit = cball_hit
    #s.groups = g.string2groups("cball")
    s.agroups =g.string2groups("castle")
    
    #s.rect, s._rect
    
    dx,dy = g.castle.rect.x-s.rect.x,g.castle.rect.y-s.rect.y
    dist = (dx*dx+dy*dy)**0.5
    v = 16
    s.vx, s.vy = dx*v/dist,dy*v/dist
    s.vz = -8
    s.z = 0
    s.damage = damage
    


def cball_loop(g,s):
    
    s.rect.x += s.vx
    s.rect.y += s.vy
    s.z += s.vz
    s.vz += 1
    if s.vz == 8:
        g.sprites.remove(s)
    #print s.rect
    s.frame += 1
    
    
def cball_hit(g,a,b):
    print "BANG!"
    g.level.game.sm.Play(sound_info.ushit.nextone())

    if b.unit.hit(a.damage):
        #raise "game over, you got killed!"
        #b.reset_castle()
        g.level.game.state = states.GameOver(g.level.game) #, g.level.game.state)




    pass
    
