import pygame
from pygame.locals import *
from const import *
#import pygame.draw

import util

import os
from pgu import engine
import pgu.text
import sound_info

"""
data = [
    (pygame.Rect(200,81,201,157),'Comfy Castle',4397,'level8.tga',100),
    (pygame.Rect(92,152,77,150),'Truthful Tower',1232,'level5.tga',100),
    (pygame.Rect(294,260,69,95),'Loyal Lookout',982,'level6.tga',100),
    (pygame.Rect(451,165,62,161),'Observatory of Honor',1444,'level7.tga',100),
    (pygame.Rect(17,335,99,58),'Simple City',214,'level1.tga',100),
    (pygame.Rect(144,390,117,52),'Valiant Village',319,'level2.tga',100),
    (pygame.Rect(325,378,118,54),'Humble Hamlet',182,'level3.tga',100),
    (pygame.Rect(509,328,96,66),'Congenial Burg',225,'level4.tga',100),
    ]
""" 
iy = img_shift_y = 44
# 
#lock,r,title,pop,n,perc,ztitle,music, selected
data = [
    (7,pygame.Rect(176, 7+iy, 213, 157),'Comfy Castle',4397,'level8.tga',70,        "Zanthor's Castle",'soundtrack3.ogg', (0,0)),

    (4,pygame.Rect(100, 179+iy, 119, 94),'Truthful Tower',1232,'level5.tga',70,     "Zanthor's Obelisk",'soundtrack2.ogg', (1,0)),
    (4,pygame.Rect(270, 179+iy, 119, 94),'Loyal Lookout',982,'level6.tga',70,       "Zanthor's Sausage Tree",'soundtrack2.ogg', (1,1)),
    (4,pygame.Rect(389, 148+iy, 123, 125),'Observatory of Honor',1444,'level7.tga',70,"Zanthor's Toothpick",'soundtrack2.ogg', (1,2)),

    (0,pygame.Rect(32, 237+iy, 144,  135),'Simple City',214,'level1.tga',80,        "Zanthor's Footstool",'soundtrack1.ogg', (2,0)),
    (0,pygame.Rect(176, 273+iy, 125, 135),'Valiant Village',319,'level2.tga',80,    "Zanthor's Garden" ,'soundtrack1.ogg', (2,1)),
    (0,pygame.Rect(301, 273+iy, 117, 83),'Humble Hamlet',182,'level3.tga',80,       "Zanthor's Coal Mine",'soundtrack1.ogg', (2,2)),
    (0,pygame.Rect(487, 273+iy, 121, 135),'Congenial Burg',225,'level4.tga',80,     "Zanthor's Rec Room",'soundtrack1.ogg', (2,3)),
    ]


def scale_data(data, size):

    orig_size = 640,480
    new_data = []
    for d in data:
        part = [d[0], util.scale_rect(d[1], orig_size, size)] + list(d[2:])
        new_data.append( part )
    
    return new_data




"""
32, 237, 144,  135
176, 273, 125, 135
231, 273, 117, 83
487, 273, 121, 135

106, 179, 109, 94
119, 94, 270, 179
123, 125, 289, 148
213, 160, 176, 8
"""


class Menu(engine.State):
    
    def init(self):
        self.bkgr = pygame.image.load(data_dir("gfx","caastles.png")).convert()

        screen_size = pygame.display.get_surface().get_size()
        self.bkgr = pygame.transform.scale( self.bkgr, screen_size )
        
        self.scaled_data = scale_data(data, screen_size)


        #rev up music...
        
        self.fonts = {}
        
        for size in [48,24]:
            self.fonts[size] = pygame.font.Font(data_dir("menu","vinque.ttf"),size)

        self.game.sm.Play(sound_info.birds[0])
        self.last_start = self.game.cur_time
        if hasattr(self.game.sm.sounds[sound_info.birds.cur()], "get_length"):
            self.last_end = self.game.elapsed_time + self.game.sm.sounds[sound_info.birds.cur()].get_length()
        else:
            self.last_end = self.game.elapsed_time + 3.0


        self.frames = 0
        self.level = None
        self.ximg = pygame.image.load(data_dir("menu","x.png")).convert_alpha()
        pygame.mouse.set_visible(True)
        self.done = self.game.data['levels']
        
        if pygame.mixer:
            pygame.mixer.music.stop()

        self.selected_row = 2
        self.selected_collum = 0

        self.show_selected = 0

        self.set_selected_parts((self.selected_row, self.selected_collum) )
        

    def paint(self,screen):
        screen.blit(self.bkgr,(0,img_shift_y))
        screen.blit(self.bkgr,(0,-SH+img_shift_y))
        
        fg = (0,0,0)
        fg2 = (62,166,49)
        fnt = self.fonts[48]
        

        text = "Sunflower Kingdom"
        img = fnt.render(text,1,fg2)
        x,y = (SW-img.get_width())/2,4
        #screen.blit(img,(x-1,y+1))
        pgu.text.write(screen,fnt,(x,y),(255,255,255),text,1)


#         img = fnt.render("Sunflower Kingdom",1,fg)
#         x,y = (SW-img.get_width())/2,4
#         screen.blit(img,(x,y))
        
        pos = pygame.mouse.get_pos()
        
        fnt = self.fonts[24]
        self.level = None
        
        done = self.done
        img = self.ximg
        for lock,r,title,pop,n,perc,ztitle,music, selected in self.scaled_data:
            if n in done:
                screen.blit(img,(r.x+(r.w-img.get_width())/2,r.y+(r.h-img.get_height())/2))

        # selected is the row/collum of that city.
        for lock,r,title,pop,n,perc,ztitle,music, selected in self.scaled_data:
            #pygame.draw.rect(screen, (0,0,0), r, 1)
            
            
            
            locked = False
            if len(self.game.data['levels']) < lock: locked = True

            if self.show_selected and selected == (self.selected_row, self.selected_collum):
                text = 'selected'
                img = fnt.render(text,1,fg)
                #x,y = r.centerx-img.get_width()/2,r.bottom-24
                x,y = r.centerx-img.get_width()/2,r.center[1]-10
                pgu.text.write(screen,fnt,(x,y),(255,255,255),text,1)

                if n not in done and not locked:
                    self.level = n,perc,music

            if locked:
                ltext = 'locked'
                img = fnt.render(ltext,1,fg)
                lx,ly = r.centerx-img.get_width()/2,r.bottom-24
                pgu.text.write(screen,fnt,(lx,ly),(255,255,255),ltext,1)


            if (self.show_selected and selected == (self.selected_row,self.selected_collum)):
                t = title
                #if n in done: 
                #    t,pop = ztitle,0
                
                text = "%s - %s  -  %d citizens"%(n,t,pop)
                text = "%s  -  %d citizens"%(t,pop)
                
                img = fnt.render(text,1,fg)
                #img2 = fnt.render(text,1,fg2)
                x,y = (SW-img.get_width())/2,SH-8-img.get_height()
                pgu.text.write(screen,fnt,(x,y),(255,255,255),text,1)


                # set this land as the selected place.
                #self.selected_row, self.selected_collum = selected

                #screen.blit(img2,(x-1,y+1))
                #screen.blit(img,(x,y))
                if n not in done and not locked:
                    self.level = n,perc,music
                #break
            
        
        pygame.display.flip()
        return
        
        
    def loop(self):
        if not self.frames % int(FPS/ 4):

            # mix the sounds in with 1. second.
            if (self.last_end - self.game.elapsed_time) < 1.:
                self.game.sm.Play(sound_info.birds.nextone())
                self.last_start = self.game.cur_time
                if hasattr(self.game.sm.sounds[sound_info.birds.cur()], "get_length"):
                    self.last_end = self.game.elapsed_time + self.game.sm.sounds[sound_info.birds.cur()].get_length()
                else:
                    # we just play for 3 seconds.
                    self.last_end = self.game.elapsed_time + 3.0

        self.frames += 1


    def update(self,screen):
        return self.paint(screen)
    
    def find_select_place(self, tobe):
        """ Returns True if it finds the level.  else returns False.
            goes through the level data to see if the tobe coords are the same as that level.
        """
        #print tobe

        found = False
        for d in self.scaled_data:
            levellock = d[0]
            pos_of_place = d[8]
            n = d[4]
            # last collumn of data  eg (0,0) is the castle at top.
            if tobe == pos_of_place:
                locked = False
                
                if len(self.game.data['levels']) < levellock:
                    locked = True
                if not locked and n not in self.done:
                    found = True
                    break

        return found


    def set_selected_parts(self, tobe):
        """ this makes sure the selected parts are within bounds.
        """

        # check to see if we can select a level.  
        #    Some levels are locked, or finished.  
        #    Some are out of bounds. eg if pressing left on far left.
        # we try going in either direction... depending on what we find.
        if tobe[1] - self.selected_collum <= 0:
            # we see if the selected place exists... otherwise we don't set it.
            for x in range(5):
                found = self.find_select_place((tobe[0], tobe[1] -x))

                if found:
                    self.selected_row, self.selected_collum = (tobe[0], tobe[1]-x )
                    break
        else:
        
            for x in range(5):
                found = self.find_select_place((tobe[0], tobe[1] +x))

                if found:
                    self.selected_row, self.selected_collum = (tobe[0], tobe[1]+x )
                    break

        # ok... we try and go up.
        if not found:
            for x in range(5):
                found = self.find_select_place((tobe[0]-x, tobe[1]))

                if found:
                    self.selected_row, self.selected_collum = (tobe[0]-x, tobe[1])
                    break



        

    
    def event(self,e):
        if e.type is MOUSEMOTION:
            for lock,r,title,pop,n,perc,ztitle,music, selected in self.scaled_data:
                if r.collidepoint(e.pos):
                    self.show_selected = True
                    self.set_selected_parts(selected)
                    
        if (((e.type in [MOUSEBUTTONDOWN, JOYBUTTONDOWN]) or 
             (e.type is KEYDOWN and e.key in [K_RETURN, K_SPACE])) and 
             (self.level != None)):
            import level
            return level.Level(self.game,*self.level)
        

        if e.type is KEYDOWN and e.key == K_ESCAPE:
            import states
            import title
            return states.Prompt(self.game,"quit? y/n",title.Title(self.game),self)
        

        if e.type in [KEYDOWN, JOYAXISMOTION]:
            self.show_selected = True

        if e.type is KEYDOWN and e.key in [K_LEFT, K_a]:
            self.set_selected_parts((self.selected_row, self.selected_collum-1))

        if e.type is KEYDOWN and e.key in [K_RIGHT, K_d]:
            self.set_selected_parts((self.selected_row, self.selected_collum+1))

        if e.type is KEYDOWN and e.key in [K_UP, K_w]:
            self.set_selected_parts((self.selected_row-1, self.selected_collum))

        if e.type is KEYDOWN and e.key in [K_DOWN, K_s]:
            self.set_selected_parts((self.selected_row+1, self.selected_collum))


        if e.type == JOYAXISMOTION:
            if e.axis == 1:
                if round(e.value) < 0:
                    # up
                    self.set_selected_parts((self.selected_row-1, self.selected_collum))
                elif round(e.value) > 0:
                    # down
                    self.set_selected_parts((self.selected_row+1, self.selected_collum))

            if e.axis == 0:
                if round(e.value) < 0:
                    # left
                    self.set_selected_parts((self.selected_row, self.selected_collum-1))
                elif round(e.value) > 0:
                    # right
                    self.set_selected_parts((self.selected_row, self.selected_collum+1))

