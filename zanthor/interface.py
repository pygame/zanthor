import pygame
from pygame.locals import *
import os
import random


import pygame.draw


import util
from pgu import gui

#import pgu.html
import html


from const import *
import units

import messages

import cyclic_list
import pygame.sprite

#class 



class StatsDraw:
    """ draws the stats health, coal, water, steam on the left side of interface.
    """
    def __init__(self):
        self.frames = 0
        self.update_frame = {}
        self.update_which = cyclic_list.cyclic_list(['Health', 'Coal', 'Water', 'Steam'])
        self.frames_health = 0

    def draw_img(self, screen, min, max, current, color, where_rect, astat):
        """ eg. min - 0, max - 100, current - 45
        """

        # this draws an image cutting off the top bit

        height = (((max - min) / (max * 1.0)) * current)
        graph_height = where_rect.h
        height = (graph_height / (max * 1.0)) * current

        clip_rect = pygame.Rect(where_rect)
        clip_rect.x = 0
        clip_rect.y = 0
        clip_rect.h = int(height)

        diff = where_rect.h - int(height)
        clip_rect.y += diff

        im_border = None

        if astat == "Health":
            # show the heart every pulse every half a second or so.
            if self.frames_health > (FPS / 2):
                k = 'heart.png'
                if self.frames_health > FPS:
                    self.frames_health = 0
            else:
                k = 'heart_pulse.png' 

            im = self.images[k]

            if not self.images.has_key(k + "laplacian"):
                self.images[k + "laplacian"] = pygame.transform.laplacian(im)

            im_border = self.images[k + "laplacian"]

            c = clip_rect.clip(im.get_rect())
            if not c.width and not c.height:
                s = None
            else:
                print im,c
                s = im.subsurface(c)

        else:
            raise "not implemented for this stat"
        
        draw_rect = pygame.Rect(where_rect)
        draw_rect.y += diff
        if s:
            screen.blit(s, draw_rect)
            
        if im_border:
            screen.blit(im_border, where_rect)
            
        return where_rect





    def draw_rect(self, screen, min, max, current, color, where_rect):
        """ eg. min - 0, max - 100, current - 45
        """
        draw_rect = pygame.Rect(where_rect)

        height = (((max - min) / (max * 1.0)) * current)
        
        graph_height = draw_rect.h

        height = (graph_height / (max * 1.0)) * current

        draw_rect.h = int(height)
        draw_rect.y += where_rect.h - draw_rect.h

        #draw_rect = multr( dxdy, draw_rect)

        s = screen.subsurface(draw_rect)
        s.fill(color)
        return where_rect


    def update_stats(self, screen, stats, robots, max_robots):
    #def update_stats(self, screen, stats):
        #print stats
        #print max_robots

        #return []

        self.interface.dirty['left_background'] = 1
        self.interface.update_left_background(screen)

        stat_rect={}
        stat_rect['Health'] = S_HEALTH
        stat_rect['Coal'] = S_COAL
        stat_rect['Water'] = S_WATER
        stat_rect['Steam'] = S_STEAM
        stat_rect['CannonPressure'] = S_CANNON_PRESSURE

        stat_color={}
        stat_color['Health'] = (255,0,0)
        stat_color['Coal'] = (0,0,0)
        stat_color['Water'] = (0,0,255)
        stat_color['Steam'] = (200,200,200)
        stat_color['CannonPressure'] = (100,100,200)



        updates = []
        update_thisone = self.update_which.nextone()

        for astat in ['Health', 'Coal', 'Water', 'Steam', 'CannonPressure']:
            # update cannon pressure every frame.  Spread the others out.
            if not (astat in [update_thisone, 'CannonPressure']):
                continue


            where_rect = stat_rect[astat]
            color = stat_color[astat]
            min =0
            max = int(stats["Max" + astat])
            current = int(stats[astat])
            #print where_rect

            #only draw the screen where the rectangle will be drawn.
            if 0:
                c = screen.get_clip()
                screen.set_clip(where_rect)
                screen.blit( self.images["background_status_left.png"], S_STATUS)
                screen.set_clip(c)

            if astat in ['Health']:
                r = self.draw_img(screen, min, max, current, color, where_rect, astat)
            else:
                r = self.draw_rect(screen, min, max, current, color, where_rect)
            updates.append(r)



        # robots.
        if 1:
            where_rect = S_PEASANTS_REMAINING
#             color = (200,200,40)
#             min =0
#             max = max_robots
#             current = int(len(robots))
# 
#             updates = []
#             r = self.draw_rect(screen, min, max, current, color, where_rect)
            
            
            # top right corner remaining 'robots' are shown.
            
            if self.robots_update:
                r = where_rect
                sc = screen.subsurface(where_rect)
                sc.fill((0,0,0))
                img = self.robots_image
                w = sc.get_width()-img.get_width()
                h = sc.get_height()-img.get_height()
                
                for n in xrange(0,self.robots_total):
                    sc.blit(img,(random.randrange(0,w),random.randrange(0,h)))


            
                updates.append(r)


        self.frames_health += 1
        self.frames += 1
        return updates



    
class Interface:
    
    def __init__(self):
        """
        """

        self.frames = 0
        self.message = messages.generate()
        self.last_message = ""
        
        self.message_font = pygame.font.Font(data_dir("menu","vinque.ttf"),20)
        self.equipment_message_font = pygame.font.Font(data_dir("menu","vinque.ttf"),14)

        self.stats = {}
        self.stats_draw = StatsDraw()
        self.stats_draw.interface = self

        self.equipment_last_message = ""
        self.equipment_message = ""


    def loop(self):
        
        self.frames += 0


    def load(self):
        """ loads the graphics/sounds/resources needed.
        """

        images_needed = ["health_overlay.png", 
                         "coal_overlay.png",
                         "water_overlay.png",
                         "steam_overlay.png",
                         "background_status_left.png",
                         "background_bottom.png",
                         "background_illustration.png",
                         "background_equipment.png",
                         "background_buttons.png",
                         "background_messages.png",

                         "button_save.png",
                         "button_load.png",
                         "button_quit.png",
                         "button_news.png",

                         "button_save_rollover.png",
                         "button_load_rollover.png",
                         "button_quit_rollover.png",
                         "button_news_rollover.png",

                         "button_save_down.png",
                         "button_load_down.png",
                         "button_quit_down.png",
                         "button_news_down.png",
                         "heart.png",
                         "heart_pulse.png",

                        ]
        self.images = {}
        self.stats_draw.images = self.images

        for i in images_needed:
            image_path = data_dir("gfx", i)
            print image_path
            if os.path.exists(image_path):
                self.images[i] = pygame.image.load(image_path)
                if i in ["heart.png", "heart_pulse.png"]:
                    self.images[i] = self.images[i].convert_alpha()
                else:
                    self.images[i] = self.images[i].convert()
            else:
                self.images[i] = None


        def scale_images(images):
            screen_size = pygame.display.get_surface().get_size()
            #scaler = pygame.transform.smoothscale
            scaler = pygame.transform.scale
            new_images = {}

            orig_size = 640,480
            for i,surf in images.items():
                if images[i]:
                    r = surf.get_rect()
                    size_scale = util.scale_rect(r, orig_size, screen_size)[2:]

                    new_images[i] = scaler( surf, size_scale)
                else:
                    new_images[i] = surf
            return new_images

        self.images = scale_images(self.images)


        self.bkgrb = pygame.Surface((S_BOTTOM_MESSAGES.w, S_BOTTOM_MESSAGES.h) )
        self.bkgrb = self.bkgrb.convert_alpha()
        self.bkgrb.fill((0,0,0, 70))


        self.dirty = {}
        d = self.dirty

        d['messages'] = 1
        d['bottom_background'] = 1
        d['left_background'] = 1
        d['background_equipment'] = 1
        d['background_illustration'] = 1
        d['background_buttons'] = 1
        d['background_messages'] = 1
        d['equipment_words'] = 1
        d[''] = 1





    def event(self, g, e):
        pass

        #TODO: handle button clicks.
        if e.type == MOUSEBUTTONDOWN:
            x,y = e.pos
            print x,y

            if S_BUTTONS_SAVE.collidepoint(x, y):
                print "save"

            if S_BUTTONS_LOAD.collidepoint(x, y):
                print "load"

            if S_BUTTONS_QUIT.collidepoint(x, y):
                print "quit"

            if S_BUTTONS_NEWS.collidepoint(x, y):
                print "news"
        if e.type == KEYDOWN:
            if e.key == K_m:
                print "ASDFSADF"
                self.new_random_message()



    def new_stats(self, stats):
        """ draws the stats with new values.
        """



    def new_random_message(self):
        self.last_message = self.message
        self.message = messages.generate()
        self.message = self.message.replace("ZANTHOR", "<b>ZANTHOR</b>")
        self.message = self.message.replace("Zanthor", "<b>ZANTHOR</b>")
        self.message = self.message.replace("zanthor", "<b>ZANTHOR</b>")
        self.dirty['messages'] = 1
        self.dirty['background_messages'] = 1


    def new_upgrade_message(self, upgrade_what):
        if upgrade_what:
            self.last_message = self.message
            self.message = messages.generate_upgrade_message(upgrade_what)
        self.dirty['messages'] = 1
        self.dirty['background_messages'] = 1






    def update_messages(self, screen):
        """
        """

        # the messages are the same... no need to update.
        if not self.dirty['messages']:
            if self.message == self.last_message:
                self.dirty['messages'] = 0
                return []

        if self.dirty['messages']:
            self.dirty['messages'] = 0

            font = self.message_font #pygame.font.Font(None, 18)
            rect = S_MESSAGES
            rect2 = pygame.Rect(S_MESSAGES)
            rect2.x -= 1
            rect2.y += 1

            aa = 0
            #color = (0x55,0xff,0x55) #(80,80,80)
            color = (0xff,0x55,0x55) #(80,80,80)
            color2 = (0,0,0) #(80,80,80)

            bgcolor = (0,0,0,0)
            s = screen
            #screen.blit(self.bkgrb, S_MESSAGES)

            #pgu.html.render(font,rect,text,aa,color,bgcolor)
            html.write(s,font,rect2,self.message,aa,color2)
            html.write(s,font,rect,self.message,aa,color)

            return [rect]
        else:
            return []






    def update_bottom_background(self, screen):
        if self.dirty['bottom_background']:
            self.dirty['bottom_background'] = 0
            screen.blit( self.images["background_bottom.png"], S_BOTTOM )


            return [S_BOTTOM]
        else:
            return []

    def update_left_background(self, screen):
        if self.dirty['left_background']:
            #FIXME: HACK: TODO: this should be 0 when stats update properly.
            self.dirty['left_background'] = 0
            screen.blit( self.images["background_status_left.png"], S_STATUS)
            return [S_STATUS]
        else:
            return []



    def new_equipment(self, stats):
        self.equipment_last_message = self.equipment_message
        self.equipment_message = "<br><br>"

        for upword in units.upgrade_words:
            self.equipment_message += "%s/%s " % (stats['upgrade_amounts'][upword].idx, 5)
            self.equipment_message += "" + upword.replace("Up","") + "<br>"
            #TODO: HACK: fix up 5 to be the maximum for that level.

        self.dirty['equipment_words'] = 1
        self.dirty['background_equipment'] = 1



    def update_background_equipment(self, screen):
        if self.dirty['background_equipment']:
            self.dirty['background_equipment'] = 0
            screen.blit( self.images["background_equipment.png"], S_ITEMS)
            return [S_ITEMS]
        else:
            return []


    def update_equipment_words(self, screen):
        """
        """

        # the messages are the same... no need to update.
        if not self.dirty['equipment_words']:
            if self.equipment_message == self.equipment_last_message:
                self.dirty['equipment_words'] = 0
                return []

        if self.dirty['equipment_words']:
            self.dirty['equipment_words'] = 0

            font = self.equipment_message_font#pygame.font.Font(None, 18)
            rect = S_ITEMS
            rect2 = pygame.Rect(S_ITEMS)
            rect2.x -= 1
            rect2.y += 1

            aa = 0
            color = (0x55,0xff,0x55) #(80,80,80)
            color2 = (0,0,0)
            bgcolor = (0,0,0,0)
            s = screen

            #pgu.html.render(font,rect,text,aa,color,bgcolor)
            html.write(s,font,rect2,self.equipment_message,aa,color2)
            html.write(s,font,rect,self.equipment_message,aa,color)

            return [rect]
        else:
            return []


    def update_background_illustration(self, screen):
        if self.dirty['background_illustration']:
            self.dirty['background_illustration'] = 0
            screen.blit( self.images["background_illustration.png"], S_ROBOT)
            
            return [S_ROBOT]
        else:
            return []



    def update_background_buttons(self, screen):
        if self.dirty['background_buttons']:
            self.dirty['background_buttons'] = 0
            s = screen.subsurface(S_BUTTONS)
            surf = self.images["background_bottom.png"]

            screen.blit( surf, S_BUTTONS, S_BOTTOM_BUTTONS)
            return [S_BUTTONS]
        else:
            return []


    def update_background_buttons(self, screen):
        if self.dirty['background_messages']:
            self.dirty['background_messages'] = 0
            surf = self.images["background_bottom.png"]

            screen.blit( surf, S_MESSAGES, S_BOTTOM_MESSAGES)
            return [S_MESSAGES]
        else:
            return []



    def update(self, tv, screen):
        """ returns a list of rects.
        """


        if self.equipment_message == "":
            self.new_equipment(tv.castle.unit.stats)


        updates = []


        # temporary interface boxes.
        if 0:
            s = screen.subsurface(S_HEALTH)
            s.fill((255,0,0))
            updates.append(S_HEALTH)

            s = screen.subsurface(S_COAL)
            s.fill((0,0,0))
            updates.append(S_COAL)

            s = screen.subsurface(S_WATER)
            s.fill((0,0,255))
            updates.append(S_WATER)

            s = screen.subsurface(S_STEAM)
            s.fill((200,200,200))
            updates.append(S_STEAM)


        updates.extend( self.update_bottom_background(screen) )
        updates.extend( self.update_left_background(screen) )

        updates.extend( self.update_background_buttons(screen) )
        updates.extend( self.update_background_illustration(screen) )
        updates.extend( self.update_background_equipment(screen) )


        updates.extend( self.update_background_buttons(screen) )



        #updates.extend( self.update_status_left(screen) )
        #updates.extend( self.update_background_equipment(screen) )
        #updates.extend( self.update_(screen) )
        
        if 0:
            screen.blit( self.images["background_status_left.png"], S_STATUS)
            updates.append(S_STATUS)


            screen.blit( self.images["background_equipment.png"], S_ITEMS)
            updates.append(S_ITEMS)


            screen.blit( self.images["background_illustration.png"], S_ROBOT)
            updates.append(S_ROBOT)


        #s = screen.subsurface(S_MESSAGES)
        #s.fill((0,200,0))

        m = self.update_messages(screen)
        updates.extend(m)




        ew = self.update_equipment_words(screen)
        updates.extend(ew)


        stats_rects = self.stats_draw.update_stats(screen, self.tv.castle.unit.stats, self.tv.robots, self.max_robots)
        updates.extend(stats_rects)


        #s = screen.subsurface(S_ROBOT)
        #s.fill((200,200,200))
        #updates.append(S_ROBOT)

        #s = screen.subsurface(S_ITEMS)
        #s.fill((250,250,250))
        #updates.append(S_ITEMS)

        #s = screen.subsurface(S_BUTTONS)
        #s.fill((150,150,200))

        if 0:
            s = screen.subsurface(S_BUTTONS_SAVE)
            s.fill((50,50,20))
            s = screen.subsurface(S_BUTTONS_LOAD)
            s.fill((50,50,20))
            s = screen.subsurface(S_BUTTONS_QUIT)
            s.fill((50,50,200))
            s = screen.subsurface(S_BUTTONS_NEWS)
            s.fill((50,150,200))


            updates.append(S_BUTTONS)


        #print updates

        return updates









if __name__=="__main__":
    pass



