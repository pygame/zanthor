import isovid
import algo

from const import *
from units import CoalTruck



def truck_new(g,t,v):
    print 'trucks disabled'
    return
    g.clayer[t.ty][t.tx] = 0
    s = isovid.Sprite(g.images['truck'],t.rect)
    
    s.frame = 0

    g.sprites.append(s)
    s.loop = truck_loop
    s.hit = truck_hit
    s.groups = g.string2groups("truck")
    s.agroups= g.string2groups("castle")
    
    s.origin = t.tx,t.ty
    s.state = 'init'
    s.unit = CoalTruck()


def dist(a,b):
    return abs(a[0]-b[0])+abs(a[1]-b[1])

def sign(v):
    if v == 0: return v
    return v/abs(v)
    
def truck_loop(g,s):
    s.unit.loop()

    s.frame += 1
    
    tw,th = g.iso_w,g.iso_h
    ww,hh = g.size
    sx,sy = s.rect.centerx/tw,s.rect.centery/th
    if s.state == 'init':
        best_s,best_d = None,65535
        for ss in g.sprites:
            if hasattr(ss,'type') and ss.type == 'factory':
                fx,fy = ss.rect.centerx/tw,ss.rect.centery/th
                dst = dist((sx,sy),(fx,fy))
                if dst < best_d:
                    best_s,best_d = ss,dst
        s.factory = best_s
        s.state = 'search'
        return
                
    
                
    if s.state == 'search':
        coals = []
        for y in xrange(0,ww):
            for x in xrange(0,hh):
                if g.tlayer[y][x] == 1: #HACK: if is coal
                    coals.append((x,y))
        if len(coals) == 0:
            s.state = 'wait'
            return
        
        best,best_d = None,65535
        fx,fy = s.factory.rect.centerx/tw,s.factory.rect.centery/th
        for cx,cy in coals:
            dst = dist((cx,cy),(fx,fy))
            if dst < best_d:
                best,best_d = (cx,cy),dst
            
        cx,cy = best
        s.target = cx,cy
        s.path = algo.astar((sx,sy),(cx,cy),g.truck_layer,dist)
        s.state = 'coal'
                    
    #once a second check if some coal has appeared...
    if s.state == 'wait':
        if s.frame%FPS == 0:
            s.state = 'search'
        return
        
        
    if s.state == 'coal':
        fx,fy = s.target
        n = g.tlayer[fy][fx] 
        if n != 1: #HACK: coal?
            s.state = 'search'
            return
        if (sx,sy) == s.target:
            s.coal = 1
            g.set((sx,sy),0)
            
            fx,fy = s.factory.rect.centerx/tw,s.factory.rect.centery/th
            s.target = fx,fy
            s.path = algo.astar((sx,sy),(fx,fy),g.truck_layer,dist)
            s.state = 'factory'
        
    if s.state == 'factory':
        if (sx,sy) == s.target:
            s.coal = 0
            #NOTE: give the coal to the factory here....
            s.state = 'search'
            return
    
    path = s.path
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
        

        
            
    
 

def truck_hit(g,a,b):
    pass
