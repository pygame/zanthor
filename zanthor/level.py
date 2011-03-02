import os, random, time

import pygame
#from pgu import isovid
import isovid
from pgu import gui

from pygame.locals import *
from const import *
import const
import human, castle, items
import interface
import states

import truck,cannon,robot
import factory


import tiles
import menu
import flock



class Level:
    def __init__(self,game,_round,perc,music):
        self.game = game
        self.round = _round
        self.percent = perc
        
        self.tv = tv = isovid.Isovid()
        self.tv.level = self
        

        self.last_mouse_event_time = time.time()
        self.last_mouse_moves = 0


        if music:
            if pygame.mixer:
                pygame.mixer.music.load(data_dir("intro",music))
                pygame.mixer.music.play(-1)

        tdata = {
            
            0x01:('castle',tiles.tile_coal,None),
            0x02:('castle',tiles.tile_water,None),
            #0x03:('castle',tiles.tile_block,{'top':1,'bottom':1,'left':1,'right':1}),
            #0x04:('castle',tiles.tile_block,{'top':1,'bottom':1,'left':1,'right':1}),
            #0x05:('castle',tiles.tile_block,{'top':1,'bottom':1,'left':1,'right':1}),
            #0x06:('castle',tiles.tile_block,{'top':1,'bottom':1,'left':1,'right':1}),
            #0x03:('cball',tiles.tile_wall,None),
            0x04:('cball',tiles.tile_wall,None),
            0x05:('cball',tiles.tile_wall,None),
            0x06:('cball',tiles.tile_wall,None),
            0x07:('castle',tiles.tile_rubble,None),

            8:('castle',tiles.tile_part,None),
            9:('castle',tiles.tile_part,None),
            10:('castle',tiles.tile_part,None),
            11:('castle',tiles.tile_part,None),
            12:('castle',tiles.tile_part,None),
            13:('castle',tiles.tile_part,None),
            14:('castle',tiles.tile_part,None),
            15:('castle',tiles.tile_part,None),

            

            0x1c:('castle,cball,robot',tiles.tile_limit,None), #remove item from level if it goes here.
            }
            #TODO: FIXME:
            

        tv.tga_load_tiles(data_dir("gfx","tiles2.tga"),(32,64),tdata)
        
        tv.tiles[1].item = items.Coal(3.0) #HERE!!
        tv.tiles[2].item = items.Water(3.0)

        tv.tiles[8].item = items.Part("UpEngine Efficiency", "")
        tv.tiles[9].item = items.Part("UpEngine Speed", "")
        tv.tiles[10].item = items.Part("UpCannon Balls", "")
        tv.tiles[11].item = items.Part("UpArmour", "")
        tv.tiles[12].item = items.Part("UpSteam Tank", "")
        tv.tiles[13].item = items.Part("UpWater Tank", "")
        tv.tiles[14].item = items.Part("UpCoal Tank", "")
        tv.tiles[15].item = items.Part("UpCannon Power", "")


        tv.tiles[7].item = items.Rubble()



        #TODO: add in the rubble item.
        
        fname = self.round
        if fname == 0: fname = 'test2.tga'
        tv.tga_load_level(data_dir("levels",fname),1)
        
        #NOTE: blur the background
        for n in xrange(0,1):
            layer = tv.blayer
            nlayer= [[0 for x in xrange(0,tv.size[0])] for y in xrange(0,tv.size[1])]
            w,h = tv.size
            for y in xrange(0,h):
                for x in xrange(0,w):
                    v = 0
                    for dx,dy in [(-1,-1),(0,-1),(1,-1),(-1,0),(1,0),(-1,1),(0,1),(1,1)]:
                        xx = min(max(x+dx,0),w-1)
                        yy = min(max(y+dy,0),h-1)
                        v += layer[yy][xx]
                    v /= 8
                    nlayer[y][x] = v
            for y in xrange(0,h):
                for x in xrange(0,w):
                    layer[y][x] = nlayer[y][x]
                    
                    
                        
        
        #NOTE: this layer is for enemies "astar" stuff
        tv.truck_layer= [[0 for x in xrange(0,tv.size[0])] for y in xrange(0,tv.size[1])]
        tv.robot_layer= [[0 for x in xrange(0,tv.size[0])] for y in xrange(0,tv.size[1])]
        tv.castle_layer= [[0 for x in xrange(0,tv.size[0])] for y in xrange(0,tv.size[1])]
        #this is for robots to see who is near by
        tv.robot_list_layer= [[[] for x in xrange(0,tv.size[0])] for y in xrange(0,tv.size[1])]

        
        #this is to init all the astar layers, forcefully...
        #since load_level shortcuts all the .set() stuff
        for y in xrange(0,tv.size[1]):
            for x in xrange(0,tv.size[0]):
                tv.set((x,y),tv.get((x,y)))
        
        
        
        tv.view.x = -220
        tv.view.y = -64
        tv.view.w,tv.view.h = S_VIEW.w,S_VIEW.h
        #tv.view.w,tv.view.h = SW,SH
        #print "view"
        #print tv.view
        
        
        tv.tile_w,tv.tile_h = 32,64
        tv.iso_w,tv.iso_h = 32,32
        tv.base_w,tv.base_h = 32,16
        tv.iso_z = 1


        #best#shape = (8,64-24,16,16)
        shape = (0,48,32,16)
        
        
        #shape = (2,64-30,28,28)
        #shape = (16,64-16,1,1)

        idata = [
            #('castle',data_dir('gfx', 'castle1.png'),(8,64-16,16,8)),
            #('coal',data_dir('gfx', 'coal.png'),(8,64-16,16,8)),
            #('castle',tv.tiles[8].image,shape),
            ('coal',tv.tiles[1].image,shape),
            ('water',tv.tiles[2].image,shape),

            ('UpEngine Efficiency',tv.tiles[8].image,shape),
            ('UpEngine Speed',     tv.tiles[9].image,shape),
            ('UpCannon Balls',     tv.tiles[10].image,shape),
            ('UpArmour',           tv.tiles[11].image,shape),
            ('UpSteam Tank',       tv.tiles[12].image,shape),
            ('UpWater Tank',       tv.tiles[13].image,shape),
            ('UpCoal Tank',        tv.tiles[14].image,shape),
            ('UpCannon Power',     tv.tiles[15].image,shape),

            ('factory.1',tv.tiles[3].image,shape),
            ('factory.2',tv.tiles[4].image,shape),
            ('factory.3',tv.tiles[5].image,shape),
            ('cannon_tower',tv.tiles[11].image,shape),
            ('wall',tv.tiles[23].image,shape),
            ('human',tv.tiles[9].image,shape),
            ('baddie_robot',tv.tiles[10].image,shape),
            
            ('truck',tv.tiles[15].image,shape),
            ('cannon',tv.tiles[11].image,shape),
            #('cball',tv.tiles[14].image,shape),
            ('cball',tv.tiles[32].image,shape),
            ('cball2',tv.tiles[33].image,shape),
            ('cball3',tv.tiles[34].image,shape),
            ('cball4',tv.tiles[35].image,shape),
            ('robot',tv.tiles[12].image.subsurface(0,24,32,32+8),(8,24,16,16)),
            ]
        timg = pygame.image.load(data_dir("gfx","tiles2.tga")).convert_alpha()
        img = timg.subsurface((0,64*2+32,64,64+32))
        shape = (16,32+32,32,32)
        idata.append(('castle',img,shape))
        idata.append(('castle.left',img,shape))
        idata.append(('castle.right',pygame.transform.flip(img,-1,0),shape))

        cdata = {
            1:(castle.castle_new,None),
            #2:(coal_new,None),
            #3:(water_new,None),
            4:(factory.factory_new,None),
            
            #16:(cannon_tower_new,None),
            #17:(baddie_robot_new,None),
            #18:(wall_new,None),
            #19:(human_new,None),
            
            5:(truck.truck_new,None),
            6:(cannon.cannon_new,None),
            7:(robot.robot_new,None),
            
        }

        #tv.load_images(idata) #should do this later, but i'm
        #using a quick hack for now
        for name,img,shape in idata:
            tv.images[name]=img,shape
        
        tw,th = tv.iso_w,tv.iso_h
        w,h = tv.size
        border = tw*2
        rect = pygame.Rect(-border,-border,tw*w+border*2,th*h+border*2)
        #tv.robots = flock.Flock(rect,tw*3/2)
        tv.robots = flock.Flock(rect,tw*2)
        tv.run_codes(cdata,(0,0,tv.size[0],tv.size[1]))
        
        tv.robots_total = len(tv.robots)




        # 
        self.interface = interface.Interface()
        self.interface.load()

        self.interface.tv = tv
        self.interface.max_robots = len(tv.robots)


        # ??? what does this code do???



        for k,v in tv.images.items():
            shape = None
            print v
            if len(v) > 1:
                img,shape = v
            else: img = v
            
            img2 = pygame.Surface((img.get_width(),img.get_height())).convert()
            ck = (255,0,255)
            img2.fill(ck)
            img2.blit(img,(0,0))
            img2.set_colorkey(ck)
            
            if shape != None:
                tv.images[k] = img2,shape
            else:
                tv.images[k] = img2
        
        n = 0
        for t in tv.tiles:
            if t != None and t.image != None:
                ck = (255,0,255,255)
                img = t.image
                minh = 64
                maxh = 0
                x = 16
                for y in xrange(0,64):
                    c = img.get_at((x,y))
                    if c[3] == 255:
                        minh = min(minh,y)
                        maxh = max(maxh,y)
                        
                if minh > maxh:
                    img2 = None
                    print 'ahh',n
                elif minh != 0 or maxh != 63:
                    t.h = maxh-minh
                    img = img.subsurface(0,minh,32,maxh-minh)
                    img2 = pygame.Surface((img.get_width(),img.get_height())).convert()
                    ck = (255,0,255)
                    img2.fill(ck)
                    img2.blit(img,(0,0))
                    img2.set_colorkey(ck)
                else: 
                    img2 = pygame.Surface((img.get_width(),img.get_height())).convert()
                    ck = (255,0,255)
                    img2.fill(ck)
                    img2.blit(img,(0,0))
                    img2.set_colorkey(ck)

                
                t.image = img2
            n += 1

        #load a few more images...
        tv.images['hole'] = pygame.image.load(data_dir('gfx','hole.png')).convert_alpha()
        tv.images['hole2'] = pygame.image.load(data_dir('gfx','hole2.png')).convert_alpha()
        tv.images['hole3'] = pygame.image.load(data_dir('gfx','hole3.png')).convert_alpha()
        tv.images['hole4'] = pygame.image.load(data_dir('gfx','hole4.png')).convert_alpha()
        
        img = pygame.Surface((1,1)).convert()
        img.fill((255,0,255))
        img.set_colorkey((255,0,255))
        tv.images['blank'] = img
        
        tv.auto_scroll = True
        
        self.hairs = pygame.image.load(data_dir("gfx","hairs.tga")).convert_alpha()

        self.frames = 0
        self.hair_update = None
        
        self.game.magic_castle = tv.castle
        self.interface.stats_draw.robots_total = 0
        self.interface.stats_draw.robots_update = 0

        self.last_show_hairs = False

    def init(self):
        #blah blah
        pass
    
    def paint(self,screen):
        
        tv = self.tv
        
        # we set these variables because the can change.
        SCROLL_MOUSE, SCROLL_AUTO, SCROLL_BORDER = const.get_mouse_info()


        show_hairs = True
        
        if self.frames > FPS: #don't scroll for at least a second...
            sv = pygame.Rect(S_VIEW)
            border = 8
            sv.x += border
            sv.y += border
            sv.w -= border*2
            sv.h -= border *2
            v = tv.view
            x,y = pygame.mouse.get_pos()
            inc = SCROLL_MOUSE
            if not sv.collidepoint((x,y)): tv.auto_scroll = False
            if x <= sv.left: 
                v.x -= inc
                show_hairs = False
            if x >= sv.right: 
                v.x += inc
                show_hairs = False
            if y <= sv.top: 
                v.y -= inc
                show_hairs = False
            if y >= sv.bottom: 
                v.y += inc
                show_hairs = False
            c = tv.castle.irect
            if not v.contains(c):
                if v.left > c.left: v.left = c.left
                if v.right < c.right: v.right = c.right
                if v.top > c.top: v.top = c.top
                if v.bottom < c.bottom: v.bottom = c.bottom
        
        v = tv.view
        p = tv.castle.irect
        border = SCROLL_BORDER
        
        inc = SCROLL_AUTO
        if self.frames < 5: #HACK, i don't know what it'll be...
            inc = 16384


        # if it isn't moved for a while we turn off mouse look.
        when_last_moved = time.time() - self.last_mouse_event_time

        if when_last_moved > 3.:
            const.DISABLE_MOUSE_LOOK = 1

        # if we move the mouse enough mouse look will go back on.
        if self.last_mouse_moves > 20:
            self.last_mouse_moves = 0
            const.DISABLE_MOUSE_LOOK = 0



        if const.DISABLE_MOUSE_LOOK:
            tv.auto_scroll = True

        #print "autoscrol is :%s:" % tv.auto_scroll
        if tv.auto_scroll:
            if p.left-border < v.left: 
                v.left = max(v.left-inc,p.left-border)
            if p.right+border > v.right: 
                v.right = min(v.right+inc,p.right+border)
            if p.top-border < v.top: 
                v.top = max(v.top-inc,p.top-border)
            if p.bottom+border > v.bottom: 
                v.bottom =min(v.bottom+inc, p.bottom+border)
        
        b = tv.bounds
        #print "*"*30
        #print "b is:"
        #print b
        #print "v is:"
        #print v
        if b != None:
            v.left = max(v.left,b.left)
            v.right = min(v.right,b.right)
            v.top = max(v.top,b.top)
            v.bottom = min(v.bottom,b.bottom)
        
        updates = []
        
        s = screen.subsurface(S_VIEW)
        #s.fill((0,0,0))
        self.tv.paint(s)
        
        updates.append(S_VIEW)
        
        vv = len(self.tv.robots)- (self.tv.robots_total*(100-self.percent)/100)
        if vv != self.interface.stats_draw.robots_total:
            self.interface.stats_draw.robots_image = self.tv.images['robot'][0]
            self.interface.stats_draw.robots_total = vv
            #self.interface.dirty['background_illustration'] = 1
            self.interface.stats_draw.robots_update = 1



        #
        interface_rects = self.interface.update(tv, screen)
        self.interface.stats_draw.robots_update = 0
        updates.extend(interface_rects)
        

        if self.hair_update != None:
            updates.append(self.hair_update)
            self.hair_update = None
        


        if show_hairs == True:
            bmx,bmy = pygame.mouse.get_pos()

            if self.last_show_hairs != show_hairs:
                pass
                #pygame.mouse.set_visible(False)
                #pygame.mouse.set_pos((bmx,bmy))

            mx,my = pygame.mouse.get_pos()
            hairs = self.hairs
            hw,hh = hairs.get_width(),hairs.get_height()
            hr = pygame.Rect((mx-hw/2,my-hh/2,hw,hh))
            tmp = pygame.Surface((hw,hh),0,32)
            tmp.blit(screen,(0,0),hr)
            screen.blit(hairs,hr)
            updates.append(hr)
        else:
            #bmx,bmy = pygame.mouse.get_pos()

            if self.last_show_hairs != show_hairs:
                pass
                #pygame.mouse.set_visible(True)
                #pygame.mouse.set_pos((bmx,bmy))
       
        pygame.display.update(updates)
        
        if show_hairs == True:
            screen.blit(tmp,hr)
            self.hair_update = hr
        self.last_show_hairs = show_hairs
        
    def update(self,screen):
        self.paint(screen)
        #[pygame.Rect(0,0,screen.get_width(),screen.get_height())]
        

    
    def loop(self):
        
        tv = self.tv
        
        #HACK for optimization of gfx
        tv.tiles[0].image = pygame.Surface((32,32))
        
        self.tv.loop()
        
        tv.tiles[0].image= None
        pass
        

        if self.frames%(FPS*12) == 0:
            self.interface.new_random_message()
        
        
        #if not self.frames % 5:
        #    flock.flock(tv.robots, 1, 1)
        #else:
        #    flock.flock(tv.robots, 0, 0)
        #    pass
        
        tv.robots.loop() #flock 'em
        
#         for r in tv.robots:
#             r._frect = r.frect
#             r.frect = pygame.Rect(r.rect)


        self.frames +=1

        #check to see if the beat the level...
        if (tv.robots_total-len(tv.robots))*100/tv.robots_total >= self.percent:

            tv.castle.unit.stats['Health'] = 10.
            tv.castle.backup_castle()
            self.game.robots_left = len(tv.robots)
            self.game.max_robots = self.interface.max_robots

            #self.interface.max_robots = len(tv.robots)

            import states
            self.game.data['levels'].append(self.round)
            if len(self.game.data['levels']) == 8:
                return states.GameWon(self.game)
            
            return states.NextLevel(self.game)


    def event(self,e):
#         if e.type is MOUSEMOTION and 1 in e.buttons:
#             self.tv.view.x -= e.rel[0]
#             self.tv.view.y -= e.rel[1]

        # if the castle is in a pickup state, then see if enter or right click.

        # note the time when the mouse is moved.
        if e.type in [MOUSEMOTION, MOUSEBUTTONDOWN, MOUSEBUTTONUP]:
            self.last_mouse_event_time = time.time()
            self.last_mouse_moves += 1

        self.interface.event(self.tv,e)

        self.tv.castle.event(self.tv,e)
        
        if e.type is KEYDOWN and e.key in (K_RETURN,K_p, K_h):
            import states
            return states.Pause(self.game,"pause",self)
        
        if e.type is KEYDOWN and e.key == K_ESCAPE:
            import states
            import menu
            return states.Prompt(self.game,"give up? y/n",menu.Menu(self.game),self)
        
        #CHEAT keys
        if e.type is KEYDOWN and e.key == K_F10:
            import menu
            import states
            return states.GameOver(self.game)
        if e.type is KEYDOWN and e.key in [K_F11, K_n]:
            import menu
            import states
            self.game.data['levels'].append(self.round)
            return states.NextLevel(self.game)
        if e.type is KEYDOWN and e.key in [K_F12, K_v]:
            import menu
            import states
            self.game.data['levels'].append(self.round)
            return states.GameWon(self.game)

        if e.type is KEYDOWN and e.key in [K_m]:
            const.DISABLE_MOUSE_LOOK = not const.DISABLE_MOUSE_LOOK
    

        #bound the mouse position
#         x,y = pygame.mouse.get_pos()
#         r = pygame.Rect(x,y,1,1)
#         r.clamp_ip(S_VIEW)
#         pygame.mouse.set_pos((r.x,r.y))

        

