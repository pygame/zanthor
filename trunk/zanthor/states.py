#this file gets all the dinky little generic states

import pygame
from pygame.locals import *

import os
import sys
import random
import traceback


from pgu import engine

import level
import menu
import pgu.text

import html
import messages
from const import *
import util


class SPause(engine.State):
    def __init__(self,game,state):
        self.game,self.state = game,state
    def event(self,e):
        if e.type is KEYDOWN:
            return self.state


class GameOver(engine.State):
    def __init__(self,game):
        self.game = game
        
    def init(self):
        self.bkgr = pygame.image.load(data_dir("intro","mybkgr.png"))
        self.font = pygame.font.Font(data_dir("menu","vinque.ttf"),32)

        screen_size = pygame.display.get_surface().get_size()
        orig_size = 640,480

        scaler = pygame.transform.scale

        r = self.bkgr.get_rect()
        size_scale = util.scale_rect(r, orig_size, screen_size)[2:]
        self.bkgr = scaler(self.bkgr, size_scale)


    def paint(self,screen):
        screen.blit(self.bkgr,(0,0))
        
        text = [
            'you died!',
            '',
            'but hey, this is a',
            'self-esteem building',
            'game where you get',
            'to act out your',
            'evil desires upon',
            'innocent people.',
            '',
            'press enter to',
            'give it another go',
            ]  
            
        fnt = self.font
        x,y = 48,20
        for line in text:
            pgu.text.write(screen,fnt,(x,y),(255,255,255),line,1)
            y += 36

        pygame.display.flip()



    def event(self,e):
        if e.type is KEYDOWN and e.key == K_RETURN: #or e.type is MOUSEBUTTONDOWN:
        #if e.type in [KEYDOWN, JOYBUTTONDOWN, MOUSEBUTTONDOWN]:

            the_round = 0
            
            #return level.Level(self.game, the_round)
            return menu.Menu(self.game)


class NextLevel(engine.State):
    def __init__(self,game):
        self.game = game


    def init(self):
        self.bkgr = pygame.image.load(data_dir("intro","introbg.png")).convert()
        self.bkgrb = pygame.Surface(self.bkgr.get_size())
        self.bkgrb = self.bkgrb.convert_alpha()
        self.bkgrb.fill((0,0,0, 150))
        self.bkgr.blit(self.bkgrb, (0,0))

        #self.bkgrb.set_alpha(100)

        self.frames = 0
        
        self.stats= [
                    "Engine Efficiency",
                    "Engine Speed",
                    "Cannon Balls",
                    "Cannon Power",
                    "Armour",
                    "Steam Tank",
                    "Water Tank",
                    "Coal Tank",
                    ]

        self.done = 0

        self.bkgr = pygame.image.load(data_dir("intro","mybkgr.png"))
        self.font = pygame.font.Font(data_dir("menu","vinque.ttf"),20)

        screen_size = pygame.display.get_surface().get_size()
        self.bkgr = pygame.transform.scale( self.bkgr, screen_size )
        
        self.cmds = []

    def paint(self,screen):
        screen.blit(self.bkgr,(0,0))
        
        text = [
            'you conquered!',
            '',
            ]
        n = 1
        castle = self.game.magic_castle
        #for stat in self.stats:
        #    line = '%d.  %d/5 %s'%(castle.unit.stats[',0,stat)
        #    text.append(line)
        
        import units
        self.cmds = []
        stats = self.game.magic_castle.unit.stats
        for upword in units.upgrade_words:
            line = ''
            line += "%d.  %s/%s " % (n,stats['upgrade_amounts'][upword].idx, 5)
            line += "" + upword.replace("Up","") 
            text.append(line)
            self.cmds.append(upword)
            n += 1
        text.append('')
        text.append('you get four upgrades')
        text.append('press 1-8 to upgrade')
        text.append('')
        text.append('press enter when done')
            
        fnt = self.font
        x,y = 48,20
        for line in text:
            try:
                img = fnt.render(line,0,(0,0,0))
            except:
                traceback.print_exc(sys.stderr)
            #x = (SW-img.get_width())/2
            #screen.blit(img,(x,y))
            pgu.text.write(screen,fnt,(x,y),(255,255,255),line,1)

            y += 28

        pygame.display.flip()


    def event(self,e):
        #            self.upgrade_something("UpEngine Efficiency")

        maxups = 4

        if e.type is KEYDOWN and e.key in (K_1,K_2,K_3,K_4,K_5,K_6,K_7,K_8):
            key = e.key-K_1
            upword = self.cmds[key]
            stats = self.game.magic_castle.unit.stats
            if (stats['upgrade_amounts'][upword].idx < 5) and (self.done < maxups):
                self.game.magic_castle.upgrade_something(upword)
                #stats['upgrade_amounts'][upword].idx += 1
                self.game.magic_castle.backup_castle()
                self.done += 1
            self.repaint()
            
        #if self.frames > (3 * FPS):
        if 1:
            #if e.type in [KEYDOWN, JOYBUTTONDOWN, MOUSEBUTTONDOWN]:
            if self.done == maxups and e.type == KEYDOWN and e.key == K_RETURN:
                return menu.Menu(self.game)




class GameWon(engine.State):
    def __init__(self,game):
        self.game = game
        
    def init(self):
        self.bkgr = pygame.image.load(data_dir("intro","mybkgr.png"))
        self.font = pygame.font.Font(data_dir("menu","vinque.ttf"),24)
        self.frame = 0
        
        if pygame.mixer:
            pygame.mixer.music.load(data_dir("intro","grass.ogg"))
            pygame.mixer.music.play(-1)

    def paint(self,screen):
        #screen.blit(self.bkgr,(0,0))
        screen.fill((255,0,0))
        
        img = self.bkgr.subsurface((404,121,236,359))
        img = pygame.transform.rotozoom(img, random.randrange(-15,15),random.randrange(90,115)/100.0)
        x,y = 440-img.get_width()/2+random.randrange(-24,24),240-img.get_height()/2+random.randrange(-12,12)
        screen.blit(img,(x,y))

        text = [
            'you won!',
            '',
            'you just destroyed',
            'over 11,273 pathetic',
            'innocent little',
            'sweet peasant folks.',
            '',
            'go ZANTHOR.',
            'celebrate your',
            'victory by doing',
            'whatever big robots',
            'do to celebrate!',
            '',
            'press enter to',
            'return to title',
            ]  
            
        fnt = self.font
        x,y = 48,20
        for line in text:
            img = fnt.render(line,0,(0,0,0))
            #x = (SW-img.get_width())/2
            #screen.blit(img,(x,y))
            pgu.text.write(screen,fnt,(x,y),(255,255,255),line,1)
            y += 28


        pygame.display.flip()

    def loop(self):
        self.frame += 1
        if (self.frame%3)==0:
            self.repaint()
            

    def event(self,e):
        if e.type is KEYDOWN and e.key == K_RETURN: #or e.type is MOUSEBUTTONDOWN:
        #if e.type in [KEYDOWN, JOYBUTTONDOWN, MOUSEBUTTONDOWN]:

            the_round = 0
            
            #return level.Level(self.game, the_round)
            import title
            return title.Title(self.game)


class News(engine.State):
    def __init__(self,game,state):
        self.game,self.state = game,state
    def event(self,e):
        if e.type is KEYDOWN:
            return self.state




class Pause(engine.State):
    def __init__(self,game,text,state):
        self.game,self.text,self.state = game,text,state
        
    def init(self):
        #self.font = pygame.font.Font(data_dir("menu","vinque.ttf"),32)
        self.font = pygame.font.Font(data_dir("menu","vinque.ttf"),20)

    def paint_old(self,screen):
        img = self.font.render(self.text,1,(0,0,0))
        x,y = (SW-img.get_width())/2,(SH-img.get_height())/2
        b = 2
        for dx,dy in [(-1,0,),(1,0),(0,1),(0,-1)]:
            screen.blit(img,(x+dx*b,y+dy*b))
        img = self.font.render(self.text,1,(255,255,255))
        screen.blit(img,(x,y))
        pygame.display.flip()


    def paint(self,screen):

        text = [
            'Pause',
            'Collect coal, and water to make steam.',
            'Zanthor must squash all the peasants ',
            '    to get to the next level.',
            'Move with asdw or arrow keys... ',
            '    or joystick, or mouse right click.',
            'Shoot with mouse click(left) or space bar.'
            '',
            ]
        
        fnt = self.font
        x,y = 48,20
        height = 90
        width = 80*4
        #x,y = (SW-width)/2,(SH-height)/2
        x,y = (SW-width)/2, 30
        x,y = (SW-width)/4, 30

        for line in text:
            pgu.text.write(screen,fnt,(x,y),(255,255,255),line,1)
            y += 36

        pygame.display.flip()



    def event(self,e):
        if e.type is KEYDOWN or e.type is MOUSEBUTTONDOWN:
            return self.state
        
class Prompt(engine.State):
    def __init__(self,game,text,yes,no):
        self.game,self.text,self.yes,self.no = game,text,yes,no
        
    def init(self):
        self.font = pygame.font.Font(data_dir("menu","vinque.ttf"),32)

    def paint(self,screen):
        img = self.font.render(self.text,1,(0,0,0))
        x,y = (SW-img.get_width())/2,(SH-img.get_height())/2
        b = 2
        for dx,dy in [(-1,0,),(1,0),(0,1),(0,-1)]:
            screen.blit(img,(x+dx*b,y+dy*b))
        img = self.font.render(self.text,1,(255,255,255))
        screen.blit(img,(x,y))
        pygame.display.flip()

    def event(self,e):
        if e.type is KEYDOWN and e.key == K_y:
            return self.yes
        if e.type is KEYDOWN and e.key == K_n:
            return self.no
