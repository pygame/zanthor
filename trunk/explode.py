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

SIZE = 16 #32 is original

class Effect:
    def __init__(self,total,add):
        
        if not hasattr(Effect,'init'):
            Effect._init(self)
        
        self.total = total
        self._total = 0
        self.add = add
        
        self.parts = []
        
        self.frame = 0
        
    def _init(self):
        Effect.init = True
        Effect.colors = colors = []
        for r in xrange(0,32):
            if r < 8: 
                rr = r-0
                c = (255,255,255-rr*8)
            elif r < 16:
                rr = r-8
                c = (255,255-rr*16,255-(rr+8)*8)
            else:
                rr = r-16
                c = (255-rr*8,128-rr*8,128-rr*8)
                
            colors.append(c)
            
        Effect.images = images = []
        for v in xrange(0,32):
            r = max(1,v*SIZE/32)
            img = pygame.Surface((r*2,r*2)).convert()
            img.fill((255,0,255))
            img.set_colorkey((255,0,255))
            img.set_alpha(255-v*8)
            
            if v < 8: 
                rr = v-0
                c = (255,255,255-rr*8)
            elif v < 16:
                rr = v-8
                c = (255,255-rr*16,255-(rr+8)*8)
            else:
                rr = v-16
                c = (255-rr*8,128-rr*8,128-rr*8)
            #print c
            pygame.draw.circle(img,c,(r,r),max(1,r/2))
            #pygame.draw.circle(img,(255-r*8,255-r*8,255-r*8),(r,r),r)
            images.append(img)

        
    def paint(self,screen,origin):
        if self.frame > 16: return
        
        _screen = screen
        
        center = self.center
        sz = 240*SIZE/32
        screen = pygame.Surface((sz,sz)).convert() 
        screen.fill((80,0,0))
        screen.set_colorkey((80,0,0))
        f = max(0,self.frame-8)
        screen.set_alpha(255-f*32)
        adj = (sz/2-center[0],sz/2-center[1])
        
        center = self.center

        todo = [[] for n in xrange(0,32)]
        
        for part in self.parts:
            p,_p = part.pos,part._pos
            xx,yy = abs(center[0]-p.x),abs(center[1]-p.y)
            #f = self.frame*2
            #r = ( abs((xx*xx+yy*yy) - (f*f)))/256
            r =  (xx*xx+yy*yy) / (256*SIZE/32)
            #dx,dy = p.x-_p.x,p.y-_p.y
            #r = ((xx*xx+yy*yy)*(dx*dx+dy*dy))/16384
            if r >= 0 and r < 32: todo[r].append((_p,p))
            
        ox,oy = adj
        for v in xrange(31,-1,-1):
            img = Effect.images[v]
            c = Effect.colors[v]
            #v = 255-r*8
            #c = (v,v,v)
            #c = (255,255,255,v)
            r = img.get_width()/2 #max(1,v*SIZE/32)
            sz = max(1,((32-v)/3+1)*SIZE/32)
            for _p,p in todo[v]:
                #pygame.draw.circle(screen,c,(p.x+pos[0],p.y+pos[1]),r+3)
                #screen.blit(img,(p.x-r+pos[0],p.y-r+pos[1]))
                
                dx,dy = p.x-_p.x,p.y-_p.y
                
                #sz = self.frame
                pygame.draw.line(screen,c,(ox+_p.x-dx*1,oy+_p.y-dy*1),(ox+p.x,oy+p.y),sz)
                screen.blit(img,(p.x-r+adj[0],p.y-r+adj[1]))

        _screen.blit(screen,(-origin[0]+center[0]-screen.get_width()/2,-origin[1]+center[1]-screen.get_height()/2))
            
    def loop(self,pos):
        if self.frame > 20: return
        self.frame += 1
        
        self.center = pos
            
            
        parts = self.parts
        if self._total < self.total:
            for n in xrange(0,self.add):
                part = Part((pos[0]+rr(-12*SIZE/32,13*SIZE/32),pos[1]+rr(-12*SIZE/32,13*SIZE/32)))
                part._pos.x,part._pos.y = pos[0],pos[1]
                parts.append(part)
                self._total += 1
        l = len(parts)
        rm = []
        for part in self.parts:
            p,_p = part.pos,part._pos

            dx,dy = p.x-_p.x,p.y-_p.y
            _p.x,_p.y = p.x,p.y
            
            p.x += dx 
            p.y += dy 
            
            
            
if __name__ == '__main__':
    screen = pygame.display.set_mode((640,480))
    
    
    #ss = [((rr(160,640),rr(160,480)),Effect(256,64)) for n in xrange(0,1)]
    
    ss = []
    
    t = timer.Timer(40)
    
    f = 0
    
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
        
        if f%20 == 0:
            ss = [((rr(160,480),rr(160,320)),Effect(512,128))]
        f += 1
        
        t.tick()
        