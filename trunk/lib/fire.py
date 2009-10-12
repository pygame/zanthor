import pygame
from pygame.locals import *
import random

from pgu import timer

rr = random.randrange

class Part:
    def __init__(self,pos):
        self.pos = pygame.Rect(pos[0],pos[1],1,1)
        self._pos = pygame.Rect(self.pos)
        self.frame = 0

class Effect:
    def __init__(self,total,add):
        
        if not hasattr(Effect,'images'):
            Effect._init(self)
        
        self.total = total
        self.add = add
        
        self.parts = []
        
        self.frame = 0
        
    def _init(self):
        Effect.images = images = []
        for r in xrange(0,32):
            img = pygame.Surface((r*2,r*2)).convert()
            img.fill((255,0,255))
            img.set_colorkey((255,0,255))
            img.set_alpha(255-r*8)
            
            if r < 8: 
                rr = r-0
                c = (255,255,255-rr*8)
            elif r < 16:
                rr = r-8
                c = (255,255-rr*16,255-(rr+8)*8)
            else:
                rr = r-16
                c = (255-rr*8,128-rr*8,128-rr*8)
            #print c
            pygame.draw.circle(img,c,(r,r),r/2)
            #pygame.draw.circle(img,(255-r*8,255-r*8,255-r*8),(r,r),r)
            images.append(img)
        
    def paint(self,screen,origin):
        todo = [[] for n in xrange(0,32)]
        for part in self.parts:
            p = part.pos
            r = part.frame 
            if r >= 0 and r < 32: todo[r].append(p)
        for r in xrange(31,-1,-1):
            img = Effect.images[r]
            v = 255-r*8
            #c = (v,v,v)
            #c = (255,255,255,v)
            for p in todo[r]:
                #pygame.draw.circle(screen,c,(p.x+pos[0],p.y+pos[1]),r+3)
                screen.blit(img,(-origin[0]+p.x-r,-origin[1]+p.y-r))

            
    def loop(self,pos):
        parts = self.parts
        if len(parts) < self.total:
            for n in xrange(0,self.add):
                part = Part((pos[0]+0,pos[1]+rr(-2,0)))
                parts.append(part)
        for part in parts:
            p,_p = part.pos,part._pos

            dx,dy = p.x-_p.x,p.y-_p.y
            _p.x,_p.y = p.x,p.y
            
            p.x += dx/3 + rr(-1,2)
            p.y += dy/4 + rr(-2,1)
            
            
            part.frame += 1
            if part.frame >= 32:
                p.x,p.y = pos[0]+0,pos[1]+rr(-2,0)
                _p.x,_p.y = p.x,p.y
                part.frame = 0
                
            
            
if __name__ == '__main__':
    screen = pygame.display.set_mode((640,480))
    
    
    ss = [((rr(160,640),rr(160,480)),Effect(64,1)) for n in xrange(0,8)]
    
    t = timer.Timer(40)
    
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
        
        t.tick()
        