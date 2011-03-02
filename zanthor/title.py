
#this file gets all the dinky little generic states

import pygame
from pygame.locals import *

import os

from pgu import engine
import pgu.text

from const import *
import util
import random

class Title(engine.State):
    
    def init(self):
        self.menu = [
            ('Start','start'),
            #('Load','load'),
            #('Save','save'),
            ('Help',Help),
            ('Credits',Credits),
            ('Quit',engine.Quit),
            ]
        self.cur = 0

        if pygame.mixer:
            pygame.mixer.music.load(data_dir("intro","zanthor.ogg"))
            pygame.mixer.music.play(-1)
        
        self.font_title = []
        for size in (160,165,170,175,180):
            self.font_title.append(pygame.font.Font(data_dir("intro","WALSHES.TTF"),size))
        self.font_main = pygame.font.Font(data_dir("menu","vinque.ttf"),32)
        
        self.rects = []
        pygame.mouse.set_visible(True)
        self.bkgr = pygame.image.load(data_dir("intro","mybkgr.png"))
        
        self.frame = 0


        
    def paint(self,screen):
        
        #print self.game.backup_castle_stats
        screen.fill((255,0,0))
        
        img = self.bkgr.subsurface((404,121,236,359))
        img = pygame.transform.rotozoom(img, random.randrange(-15,15),random.randrange(90,115)/100.0)
        x,y = 380-img.get_width()/2+random.randrange(-24,24),290-img.get_height()/2+random.randrange(-12,12)
        screen.blit(img,(x,y))
        
        fnt = random.choice(self.font_title)
        text = "Zanthor"
        fg,bg,b = (255,255,255),(0,0,0),4
        if self.frame%8 < 4: fg = (255,0x55,0x55)
        
        img = fnt.render(text,1,bg)
        x,y = (SW-img.get_width())/2+random.randrange(-8,8),100-img.get_height()/2+random.randrange(-8,8)
        for dx,dy in [(-1,0),(0,1),(1,0),(0,-1),(-1,-1),(-1,1),(1,-1),(1,1)]:
            screen.blit(img,(x+dx*b,y+dy*b))
        img = fnt.render(text,1,fg)
        screen.blit(img,(x,y))
        
        
        fnt = self.font_main
        x,y,n = 48,220,0
        self.rects= []
        
        for text,action in self.menu:
            c = (0xaa,0xaa,0xaa)
            if n == self.cur: c = (255,255,255)
            bg = (0,0,0)
            img = fnt.render(text,1,bg)
            b = 2
            for dx,dy in [(-1,0),(0,1),(1,0),(0,-1)]:
                screen.blit(img,(x+dx*b,y+dy*b))
            
            img = fnt.render(text,1,c)
            screen.blit(img,(x,y))
            self.rects.append((n,pygame.Rect(x,y,img.get_width(),img.get_height())))
            y += 40
            n += 1
        #print self.cur,n
        
        pygame.display.flip()
        
    def loop(self):
        if self.frame%3==0:
            self.repaint()
        self.frame += 1
    
    def event(self,e):
        if e.type is MOUSEMOTION:
            for n,r in self.rects:
                if r.collidepoint(e.pos):
                    self.cur = n
                    #self.repaint()

        elif e.type == JOYAXISMOTION:
            if e.axis == 1:
                if round(e.value) < 0:
                    self.cur = (self.cur-1+len(self.menu))%len(self.menu)
                elif round(e.value) > 0:
                    self.cur = (self.cur+1+len(self.menu))%len(self.menu)
        
        elif e.type is KEYDOWN:
            if e.key == K_UP:
                self.cur = (self.cur-1+len(self.menu))%len(self.menu)
                #self.repaint()
            if e.key == K_DOWN:
                self.cur = (self.cur+1+len(self.menu))%len(self.menu)
                #self.repaint()
        if (e.type is KEYDOWN and e.key == K_RETURN) or e.type in [MOUSEBUTTONDOWN, JOYBUTTONDOWN]:
            text,action = self.menu[self.cur]
            if action == 'start':
                if pygame.mixer:
                    pygame.mixer.music.stop()
                g = self.game
                g.data_reset()
                import menu
                return menu.Menu(self.game)
            else: return action(self.game)
        
#etc...


class Help(engine.State):
    def paint(self,screen):
        screen.blit(pygame.image.load(data_dir("intro","mybkgr.png")),(0,0))
        
        text = [
            'help',
            '',
            'press and hold right mouse',
            'to build up pressure.',
            'release to shoot.',
            '',
            "collect coal and water",
            "to keep steam up.",
            "",
            "arrow keys, a/w/s/d also",
            "work.  f/space to fire.",
            "",
            "you are ZANTHOR!",
            ]
            
        fnt = pygame.font.Font(data_dir("menu","vinque.ttf"),24)
        x,y = 48,20
        for line in text:
            img = fnt.render(line,0,(0,0,0))
            #x = (SW-img.get_width())/2
            #screen.blit(img,(x,y))
            pgu.text.write(screen,fnt,(x,y),(255,255,255),line,1)
            y += 32
        pygame.display.flip()
        
    def event(self,e):
        if e.type is KEYDOWN or e.type is MOUSEBUTTONDOWN:
            return Title(self.game)
        
class Credits(engine.State):
    def paint(self,screen):
        screen.fill((255,0,0))

        screen.blit(pygame.image.load(data_dir("intro","mybkgr.png")),(0,0))
        text = [
            'credits',
            '',
            'aka - graphics',
            'illume - code, etc',
            'philhassey - code, etc',
            'TimInge - music, sfx',
            '',
            ]
            
        fnt = pygame.font.Font(data_dir("menu","vinque.ttf"),32)
        x,y = 60,20
        for line in text:
            img = fnt.render(line,0,(0,0,0))
            x = (460-img.get_width())/2
            #screen.blit(img,(x,y))
            pgu.text.write(screen,fnt,(x,y),(255,255,255),line,1)
            y += 48
        pygame.display.flip()
            
        
    def event(self,e):
        if e.type is KEYDOWN or e.type is MOUSEBUTTONDOWN:
            return Title(self.game)

