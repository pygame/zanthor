import pygame
from pygame.locals import *
import random

from pgu import timer

rr = random.randrange

class Part:
    def __init__(self,x,y):
        x,y = float(x),float(y)
        self.x,self.y = x,y
        self._x,self._y = x,y
        self.min = 4.0
        self.max = 16.0
        self.radius = 16.0
        self.center = 2.0
        self.search = 64.0
        self._flock_frame = 0
        self.near = []
        
class Flock:
    def __init__(self,rect,spacing):
        self.rect,self.spacing = rect,spacing
        self.grid = [[[] for tx in xrange(rect.left,rect.right,spacing)] for ty in xrange(rect.top,rect.bottom,spacing)]
        self.parts = []
    
    def append(self,p):
        rect,spacing,grid,parts = self.rect,self.spacing,self.grid,self.parts
        self.parts.append(p)
        tx,ty = p._tx,p._ty = int((p.x-rect.left)/spacing),int((p.y-rect.top)/spacing)
        p.vx,p.vy = 0,0
        grid[ty][tx].append(p)
        
    def remove(self,p):
        rect,spacing,grid,parts = self.rect,self.spacing,self.grid,self.parts
        tx,ty = p._tx,p._ty
        grid[ty][tx].remove(p)
        parts.remove(p)
        
        
    def __len__(self):
        return self.parts.__len__()
    
    def __iter__(self):
        return self.parts.__iter__()
        
    def loop(self):
        rect,spacing,grid,parts = self.rect,self.spacing,self.grid,self.parts
        gw,gh = len(grid[0]),len(grid)
        
        #update grid
        for p in parts:
            tx,ty = p._tx,p._ty
            grid[ty][tx].remove(p)
            tx,ty = p._tx,p._ty = int((p.x-rect.left)/spacing),int((p.y-rect.top)/spacing)
            grid[ty][tx].append(p)

        #calculate velocities
        for p in parts:
            p.vx,p.vy = p.x-p._x,p.y-p._y
            p._x,p._y = p.x,p.y
            
        #calculate neighbors
        for p in parts:
            tx,ty = p._tx,p._ty
            
            p.near = []
            for dy in (-1,0,1):
                for dx in (-1,0,1):
                    xx,yy = tx+dx,ty+dy
                    if xx < 0 or yy < 0 or xx >= gw or yy >= gh: continue
                    p.near.extend(grid[yy][xx])
            p.near.remove(p)
            
            p.ax,p.ay = p.x,p.y
            p.avx,p.avy = p.vx,p.vy
    
            for _p in p.near:
                p.ax += _p.x
                p.ay += _p.y
                p.avx += _p.vx
                p.avy += _p.vy
                
            total = len(p.near)+1
            p.ax /= total
            p.ay /= total
            p.avx /= total
            p.avy /= total
                    
        #add average velocity to item
        for p in parts:
            p.x,p.y = p.x+p.avx,p.y+p.avy
            
        #move towards the center
        for p in parts:
            step = p.center
            ax,ay = p.ax,p.ay
            dx,dy = ax-p.x,ay-p.y
            dist = (dx*dx+dy*dy)**0.5
            if dist > step:
                p.x,p.y = p.x+step*dx/dist,p.y+step*dy/dist

        #check min velocity
        for p in parts:
            step = p.min
            dx,dy = p.x-p._x,p.y-p._y
            dist = (dx*dx+dy*dy)**0.5
            while dist < 0.5:
                dx,dy = random.randrange(-1,2),random.randrange(-1,2)
                dist = (dx*dx+dy*dy)**0.5
            if dist < step:
                p.x,p.y = p._x+dx*step/dist,p._y+dy*step/dist
    
        #keep away from neighbords
        for p in parts:
            for _p in p.near:
                dx,dy = _p.x-p.x,_p.y-p.y
                dist = (dx*dx+dy*dy)**0.5
                r = p.radius+_p.radius
                if dist < r:
                    if dist == 0: dist,dx = 1,1
                    inc = r/2.0
                    mx,my = (p.x+_p.x)/2,(p.y+_p.y)/2
                    p.x,p.y = mx - (inc*dx/dist), my - (inc*dy/dist)
                    _p.x,_p.y = mx + (inc*dx/dist), my + (inc*dy/dist)
                            
        #check max velocity
        for p in parts:
            step = p.max
            dx,dy = p.x-p._x,p.y-p._y
            dist = (dx*dx+dy*dy)**0.5
            if dist > step:
                p.x,p.y = p._x+dx*step/dist,p._y+dy*step/dist

if __name__ == '__main__':
    try:
        #0/0 #HACK: so i can CTRL-c out
        import psyco
        psyco.profile()
        print 'psyco installed'
    except:
        print 'psyco not installed'


    SW,SH = 640,480
    screen = pygame.display.set_mode((SW,SH))
    
    num = 256
    rad = 12
    spacing = rad*3/2
    border = spacing*2
    myflock = Flock(pygame.Rect(-border,-border,SW+border*2,SH+border*2),spacing)
    for n in xrange(0,num):
        p = Part(rr(0,SW),rr(0,SH))
        p.radius = rad
        myflock.append(p)
    
    t = timer.Speedometer()
    pygame.time.get_ticks()
    
    us = [(0,0,SW,SH)]
    
    _quit = False
    frames = 0
    while not _quit:
        for e in pygame.event.get():
            if e.type is QUIT: _quit = True
            if e.type is KEYDOWN and e.key == K_ESCAPE: _quit = True
        
        for r in us:
            screen.fill((0,0,0),r)
        _us,us = us,[]
        us = []

        p = myflock.parts[0] #HACK!!
        p.x,p.y = pygame.mouse.get_pos()
        p.radius = 64
        x,y,r = int(p.x),int(p.y),int(p.radius)
        pygame.draw.circle(screen,(0,0,128),(x,y),r)
        us.append((x-r,y-r,r*2,r*2))
        
        myflock.loop()
        
        for p in myflock: #HACK!!
            p.x = max(0,min(SW,p.x))
            p.y = max(0,min(SH,p.y))
            rect = int(p.x),int(p.y),4,4
            screen.fill((255,255,255),rect)
            us.append(rect)
        pygame.display.update(_us)
        pygame.display.update(us)
        
        r = t.tick()
        if r: print r
        frames += 1
        
