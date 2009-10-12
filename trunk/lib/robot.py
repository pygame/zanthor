import isovid

from const import *
#from pgu import algo
import algo

from units import Robot

import sound_info


import random


MIN = 8.0
MIN_RAND = 4
MAX = 16.0
MAX_RAND = 8.0
RADIUS = 32.0
RADIUS_RAND = 12
CENTER = 4.0 
CENTER_RAND = 2
SEARCH = 128.0

def robot_new(g,t,v):
    g.clayer[t.ty][t.tx] = 0
    s = isovid.Sprite(g.images['robot'],t.rect)
    
    s.frame = 0
    s.origin = t.tx,t.ty

    g.sprites.append(s)
    s.loop = robot_loop
    #if random.randrange(0,20) == 0:
    #    s.loop = robot_loop_2
    s.hit = robot_hit
    s.groups = g.string2groups("robot")
    s.agroups =0 #g.string2groups("castle")
    s.path = []
    s.state = 'alive'
    s.type = 'robot'

    s.unit = Robot()
    
    s.x,s.y = float(s.rect.x),float(s.rect.y)
    s._x,s._y = s.x,s.y
    s._min = s.min = MIN + random.randrange(-MIN_RAND,MIN_RAND)
    s.max = MAX + random.randrange(-MAX_RAND,MAX_RAND)
    s.radius = RADIUS + random.randrange(-RADIUS_RAND,RADIUS_RAND)
    s.center = CENTER + random.randrange(-CENTER_RAND,CENTER_RAND)
    s.search = SEARCH 
    s._flock_frame = 0
    s.near = []
    s.avx = 0
    s.avy = 0
    s.ax = 0
    s.ay = 0


    g.robots.append(s)
    
    ty,tx = t.ty,t.tx
    g.robot_list_layer[ty][tx].append(s)
    


def dist(a,b):
    return abs(a[0]-b[0])+abs(a[1]-b[1])
def sign(v):
    if v == 0: return v
    return v/abs(v)
    
    
    
def sdist(a,b):
    return abs(a.rect.x-b.rect.x)+abs(a.rect.y-b.rect.y)

def robot_shove(g,s,(x,y)):
    tw,th = g.iso_w,g.iso_h
    r = pygame.Rect(s.rect)
    dx,dy = x-r.x,y-r.y
    dist = (dx*dx+dy*dy)**0.5
    dx,dy = dx/dist,dy/dist
    n = 0
    inc = 8.0
    xx,yy = r.x,r.y
    while n < dist:
        # play them in order.  if there is one already playing, don't play it.
        g.level.game.sm.Play(sound_info.peasants.nextone(), wait=2)
        p = pygame.Rect(r)
        n += inc #sure, why not 8!
        xx += dx*inc
        yy += dy*inc
        r.x,r.y = xx,yy
        tx,ty = r.centerx/tw,r.centery/th
        if g.robot_layer[ty][tx]:
            s.x,s.y = p.x,p.y
            return
    s.x,s.y = x,y
    
    
        
    
    
    

def robot_loop(g,s):
    
    if s.state == 'dead':
        if s in g.sprites: g.sprites.remove(s)
        if s in g.robots: g.robots.remove(s)
        return
    
    tw,th = g.iso_w,g.iso_h
    s.min = max(s._min,min(s.max,s.min-0.5))
    
    s.rect.x,s.rect.y = s.x,s.y
    tx,ty = s.rect.centerx/tw,s.rect.centery/th
    
    if g.robot_layer[ty][tx]:
        s.rect.x,s.rect.y = s._x,s._y
        tx,ty = s.rect.centerx/tw,s.rect.centery/th
        if g.robot_layer[ty][tx]:
            x,y = s.px,s.py
            s.rect.x,s.rect.y = x,y
        s.x,s.y = s.rect.x,s.rect.y
    
    tx,ty = s.rect.centerx/tw,s.rect.centery/th
    if g.robot_layer[ty][tx]:
        if s in g.sprites:
            g.sprites.remove(s)
        if s in g.robots:
            g.robots.remove(s)
            

    
def robot_init(g,s):
    rdist = []
    for r in g.robots:
        rdist.append((sdist(r,s),r))
    rdist.sort()
    s.robots = []
    for d,r in rdist[0:3]:
        s.robots.append(r)
        

def robot_loop_bilge(g,s):
    print len(g.robots)
    return
    #s.unit.loop()
    
    #if random.randrange(0,30) == 0:
    #    s.init = True
    
    #if s.init:
    #    robot_init(g,s)
    #    s.init = False

    
    tw,th = g.iso_w,g.iso_h
    tx,ty = s.rect.centerx/tw,s.rect.centery/th
    
    g.robot_list_layer[ty][tx].remove(s)
    
    xx,yy = 0,0
    total = 0.0
#     for r in s.robots:
    for _ty in xrange(ty-1,ty+2):
        for _tx in xrange(tx-1,tx+2):
    #for _tx,_ty in [(tx-1,ty),(tx+1,ty),(tx,ty-1),(tx,ty+1)]:
            for r in g.robot_list_layer[_ty][_tx]:
                sx,sy = s.frect.x,s.frect.y
                rx,ry = r.frect.x,r.frect.y
                px,py = r._frect.x,r._frect.y
                
                #go towards neighbor
                f = 1.0
                xx,yy,total = xx+rx*f,yy+ry*f,total+f
                
                #stear away from neighbor
                dx,dy = sx-rx,sy-ry 
                while dx == 0 and dy == 0:
                    dx,dy = random.randrange(-1,2),random.randrange(-1,2)
                dist = abs(dx)+abs(dy)
                sep = 32
                x,y = rx+(sep*dx/dist),ry+(sep*dy/dist)
                f = 1.0
                xx,yy,total = xx+x*f,yy+y*f,total+f
        
                #stear towards you + neighbors vector
                dx,dy = rx-px,ry-py 
                x,y = sx+dx,sy+dy
                f = 1.0
                xx,yy,total = xx+x*f,yy+y*f,total+f

    if total != 0:
        xx = int(xx/total)
        yy = int(yy/total)
    else: xx,yy = s.rect.x,s.rect.y
    
    
    px,py = s.rect.x,s.rect.y
    
    dx,dy = xx-px,yy-py
    mx = 16
    val = (abs(dx)+abs(dy))
    if val > mx:
        xx = px + dx*mx/val
        yy = py + dy*mx/val
        
    if val == 0:
        dx,dy = s.frect.x-s._frect.x,s.frect.y-s._frect.y
        xx,yy = px+dx,py+dy
        
    ty,tx = xx/tw,yy/th
    if g.robot_layer[ty][tx]:
        xx,yy = s.rect.x,s.rect.y
    
    s.rect.x,s.rect.y = xx,yy
    
    tx,ty = s.rect.centerx/tw,s.rect.centery/th
    g.robot_list_layer[ty][tx].append(s)
    
def robot_loop_2(g,s):
    
    tw,th = g.iso_w,g.iso_h
    sx,sy = s.rect.centerx/tw,s.rect.centery/th
        
    if s.frame%FPS in (0,10,20,30): #HACK, uh oh!
        #rint g.slayer#
        
        #sx,sy = s.rect.centerx/tw,s.rect.centery/th
        p = g.castle
        px,py = p.rect.centerx/tw,p.rect.centery/th
        ox,oy = s.origin[0],s.origin[1]
        dx,dy = px-ox,py-oy #px-sx,py-sy
        
        if (dx*dx+dy*dy)**0.5 < 12: #follow if near by origin
            sx,sy = s.rect.centerx/tw,s.rect.centery/th
            p = g.castle
            px,py = p.rect.centerx/tw,p.rect.centery/th
            s.path = algo.astar((sx,sy),(px,py),g.robot_layer,dist)
        else: #else return to origin
            s.path = algo.astar((sx,sy),(ox,oy),g.robot_layer,dist)
            
        
    path = s.path
    if 1: # or len(path) < 12:
        while len(path) > 1:
            bx,by = path[1]
            if (bx,by) == (sx,sy): 
                path.pop(0)
                continue
            dx,dy = bx-sx,by-sy
            v = 4
            s.rect.x += sign(dx)*v
            s.rect.y += sign(dy)*v
            break
        

        
            
    
    s.frame += 1


def robot_hit(g,a,b):
    pass
