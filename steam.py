import pygame
from pygame.locals import *
import random

from pgu import timer

rr = random.randrange

class Part:
    def __init__(self,pos,z):
        self.pos = pygame.Rect(pos[0],pos[1],1,1)
        self._pos = pygame.Rect(self.pos)
        self.frame = 0
        self.z = z


NUM_BITS = 10

class Effect:
    def __init__(self,total,add,region=1,respawn=1,color=(255,255,255)):
        
        #if not hasattr(Effect,'images'):
        #    Effect._init(self)
        
        self._init(color)
        
        self.total = total
        self.add = add
        
        self.parts = []
        self.region = region
        self.respawn = respawn
        
        self.frame = 0
        self.frames = 0
        
    def _init(self,color):
        if not hasattr(Effect,'data'):
            Effect.data = {}
        data = Effect.data
        k = 'images.%s'%str(color)
        if k not in data:
            images = data[k] = []
            for r in xrange(0,NUM_BITS):
                img = pygame.Surface((r*2,r*2)).convert()
                img.fill((255,0,255))
                img.set_colorkey((255,0,255))
                img.set_alpha(255-r*(8*32/NUM_BITS))
                pygame.draw.circle(img,color,(r,r),r)
                #pygame.draw.circle(img,(255-r*8,255-r*8,255-r*8),(r,r),r)
                images.append(img)
        self.images = data[k]

        
    def zpaint(self): #,origin):

        ret = []

        if 1 or not self.frames % 2:

            todo = [[] for n in xrange(0,NUM_BITS)]
            for part in self.parts:
                p = part.pos
                r = part.frame
                if r >= 0 and r < NUM_BITS: todo[r].append(part)
            for r in xrange(NUM_BITS-1,-1,-1):
                img = self.images[r]
                v = 255-r*8
                #c = (v,v,v)
                #c = (255,255,255,v)
                for part in todo[r]:
                    p = part.pos
                    #pygame.draw.circle(screen,c,(p.x+pos[0],p.y+pos[1]),r+3)
                    #screen.blit(img,(-origin[0]+p.x-r,-origin[1]+p.y-r))
                    ret.append((part.z,img,(p.x-r,p.y-r)))

        self.frames += 1
        
        return ret
                

            
    def zloop(self,pos,z):
        parts = self.parts
        if len(parts) < self.total:
            region = self.region
            for n in xrange(0,self.add):
                part = Part((pos[0]+rr(-region,region),pos[1]+rr(-region,region)),z)
                parts.append(part)
        for part in parts:
            p,_p = part.pos,part._pos

            dx,dy = p.x-_p.x,p.y-_p.y
            _p.x,_p.y = p.x,p.y
            
            p.x += dx/3 + rr(-4,2)
            p.y += dy/4 + rr(-6,2)
            
            #r = (abs(p.x)+abs(p.y))/8
            #if r > NUM_BITS:
            part.frame += 1
            
            if part.frame >= NUM_BITS and self.respawn:
                p.x,p.y = pos[0]+rr(-2,2),pos[1]+rr(-2,0)
                _p.x,_p.y = p.x,p.y
                part.z = z
                part.frame = 0
                
                
    def paint(self,screen,origin):
        for z,img,pos in self.zpaint():
            screen.blit(img,(-origin[0]+pos[0],-origin[1]+pos[1]))

    def loop(self,pos):
        return self.zloop(pos,0)
            
if __name__ == '__main__':
    screen = pygame.display.set_mode((640,480))
    
    
    ss = [((rr(160,640),rr(160,480)),Effect(NUM_BITS,1)) for n in xrange(0,8)]
    
    #t = timer.Timer(40)
    t = timer.Speedometer()
    pygame.time.get_ticks()
    
    _quit = False
    while not _quit:
        for e in pygame.event.get():
            if e.type is QUIT: _quit = True
            if e.type is KEYDOWN and e.key == K_ESCAPE: _quit = True
        
        screen.fill((0,0,0))
        for pos,s in ss:
            s.loop(pos)
            s.paint(screen,(0,0))
        pygame.display.flip()
        
        r = t.tick()
        if r: print r
        
