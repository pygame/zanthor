
import time
import pygame
from pygame.locals import *
from const import *

import os
from pgu import engine

#tempo = 125
#speed = 6

data = [
    (0,'you',0,64),
    (8,'are',90,64),
    (16,'Zanthor',128,144),
    (28,'and',160,64),
    (32,'you',190,64),
    (48,'are',210,64),
    (64+0,'MAD',255,320),
    ]

#     (0,'you',0,32),
#     (8,'are',90,32),
#     (16,'Zanthor',128,72),
#     (28,'and',160,32),
#     (32,'you',190,32),
#     (48,'are',210,32),
#     (64+0,'MAD',255,160),

# uncomment this to test it without a mixer.
#pygame.mixer = None

class Intro(engine.State):
    
    def init(self):
        
        #rev up music...
        if pygame.mixer:
            pygame.mixer.music.load(data_dir("intro","intro1.ogg"))
            #pygame.time.wait(2500) #let fullscreen kick in,
            pygame.mixer.music.play()
        else:
            self.cur_time = time.time()
            self.elapsed_time = 0.

        im_path = data_dir("intro","introbg.png")
        self.bkgr = pygame.image.load(im_path).convert()
        screen_size = pygame.display.get_surface().get_size()
        self.bkgr = pygame.transform.scale( self.bkgr, screen_size )

        self.fonts = {}
        
        for frame,text,alpha,size in data:
            self.fonts[size] = pygame.font.Font(data_dir("intro","WALSHES.TTF"),size)
 


        self.cur = None
        self.frame = 0
        
        pygame.mouse.set_visible(False)
        

    def paint(self,screen):
        return
        #screen.fill((0,0,0))
        #pygame.display.flip()
        
        
    def loop(self):
        if pygame.mixer:
            if not pygame.mixer.music.get_busy():
                import title
                return title.Title(self.game)
        else:
            if self.elapsed_time > 15.3462460041:
                import title
                return title.Title(self.game)
                
    
    def update(self,screen):
        if pygame.mixer:
            t = pygame.mixer.music.get_pos()
        else:
            last_time = self.cur_time
            self.cur_time = time.time()
            self.elapsed_time += (self.cur_time - last_time)
            t = int(self.elapsed_time * 1000)
            


        f = t*125*4/(60*1000)
        
        for d in data:
            if f >= d[0]:
                cur = d
            
        #print f,'render',cur
        if cur != self.cur: 
            self.cur,self.frame = cur,0
        
        frame,text,alpha,size = cur
        
        if self.frame > 1 and text != 'MAD': return
        
        fnt = self.fonts[size]
        
        if self.frame == 0:
            screen.fill((255,255,255))
            img = fnt.render(text,1,(0,0,0))
            screen.blit(img,((SW-img.get_width())/2,(SH-img.get_height())/2))
            
        if self.frame > 0:
            v = 0
            if alpha == 255: v = 255
            screen.fill((v,0,0))
            bg = self.bkgr
            if text == 'MAD':
                alpha = max(0,alpha-self.frame*4)
            bg.set_alpha(alpha)
            screen.blit(bg,(0,0))
            img = fnt.render(text,1,(0,0,0))
            for dx,dy in [(-2,0),(2,0),(0,2),(0,-2)]:
                screen.blit(img,(dx+(SW-img.get_width())/2,dy+(SH-img.get_height())/2))
            
            img = fnt.render(text,1,(255,255,255))
            screen.blit(img,((SW-img.get_width())/2,(SH-img.get_height())/2))
            
        pygame.display.flip()
        
        self.frame += 1
        
        
    
    def event(self,e):
        #if e.type in [KEYDOWN, MOUSEBUTTONDOWN, JOYBUTTONDOWN]:
        if e.type in [KEYDOWN, JOYBUTTONDOWN]:
            if pygame.mixer:
                pygame.mixer.music.stop()
            import title
            return title.Title(self.game)
            #return level.Level(self.game,0)
            
        
