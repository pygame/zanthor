"""

to keep the state of the castle.

"""
import random,pprint,copy

import effect,steam,explode


import pygame
from pygame.locals import *

import states
import isovid

import robot

from pgu import gui
def dist(a,b):
    return abs(a[0]-b[0])+abs(a[1]-b[1])

def sign(v):
    if v == 0: return v
    return v/abs(v)

import algo
from const import *

#from units import *
import units
import items

import sound_info



def iso_facing_to_screen_facing(kx, ky):
    if kx == 0 and ky == -1:
        kx = -1
        ky = -1

    elif kx == 0 and ky == 1:
        kx = 1
        ky = 1

    elif kx == 1 and ky == -1:
        kx = 0
        ky = -1

    elif kx == -1 and ky == -1:
        kx = -1
        ky = 0
    elif kx == -1 and ky == 1:
        kx = 0
        ky = 1
    elif kx == 1 and ky == 1:
        kx = 1
        ky = 0

    elif kx == 1 and ky == 0:
        kx = 1
        ky = -1

    elif kx == -1 and ky == 0:
        kx = -1
        ky = 1
    return (kx, ky)



class CastleSprite(isovid.Sprite):
    def __init__(self, *args, **kwargs):
        isovid.Sprite.__init__(self, *args, **kwargs)

        self.unit = units.Castle()


        self.can_move = True
        self.loop = castle_loop
        self.hit = castle_hit

        self.doing = ""

        self.frame = 0

        # counters for when hitting coal.
        self.last_hit_coal = 0
        self.last_loop = 0

        # how long ago we updated steam.
        self.last_update_steam = 0
        
        self.path = []
        self.target = None

        self.fire_state = ""

        self.direction_dx = 0
        self.direction_dy = 0
        self.last_direction_dy = 0
        self.last_direction_dx = 0
        

    def no_move(self):
        self.can_move = False

    def yes_move(self):
        self.can_move = True

    def yes_pickup(self, e):
        print "yes pickup"

        self.doing = ""
        self.yes_move()

        if not hasattr(self.item_tile, "item"):
            print "WEIRD: tile does not have an item attached?"
            print self.item_tile
            print dir(self.item_tile)
            return


        print self.item_tile.item

        # if not pickup item, then it's not picked up.
        #  this can happen if coal/water tanks are too small.
        if self.unit.pickup_item(self.item_tile.item):
            item = self.item_tile.item

            if item.type & items.ITEM_PART:
                self.upgrade_something(item.name)



            if not AUTO_PICKUP:
                # remove the buttons.
                self.g.app.main_container.remove( self.g.app.question_table )


            #tw,th = self.g.iso_w,self.g.iso_h
            tx, ty = self.item_tile.tx, self.item_tile.ty
            self.g.set((tx,ty),0)



    def no_pickup(self, e):

        if not AUTO_PICKUP:
            print "no pickup"
            #self.unit.pickup_item(self.item_sprite)
            self.doing = ""
            self.yes_move()
            # remove the buttons... if they are there.
            try:
                self.g.app.main_container.remove( self.g.app.question_table )
            except ValueError:
                pass

    def check_for_pickup(self, g, t):

        self.last_hit_coal += 1

        if AUTO_PICKUP:
            self.doing = "deciding on picking up"
            self.item_tile = t

            self.yes_pickup("")
        else:

            if not self.doing:
                print "adding button"
                #s.no_move()

                self.doing = "deciding on picking up"
                self.item_tile = t

                #TODO: show the question.


    def upgrade_something(self, upgrade_what):
        """ this upgrades something.
        """

        amount = self.unit.stats['upgrade_amounts'][upgrade_what].cur()
        self.unit.stats['upgrade_amounts'][upgrade_what].next()
        self.unit.upgrade_part(upgrade_what, amount)

        #play upgrade sound here.
        self.g.level.game.sm.Play(sound_info.get_upgrade_sound(upgrade_what))

        # update the equipment section
        self.g.level.interface.new_equipment(self.unit.stats)

        # say a message about the upgrade.
        self.g.level.interface.new_upgrade_message(upgrade_what)


    def event(self, g , e):
        tw,th = g.iso_w,g.iso_h
        s = self
        sx,sy = s.rect.centerx/tw,s.rect.centery/th



        if hasattr(e,'pos'):
            epos = e.pos[0]-S_VIEW.x,e.pos[1]-S_VIEW.y
            #print epos
            #print "sx:%s  sy:%s" % (sx, sy)
        
        if e.type is MOUSEBUTTONDOWN and e.button == 3:
            tx,ty = g.screen_to_tile(epos)
            #print 'left',tx,ty
            w,h = g.size
            if (tx,ty) != (sx,sy) and (tx >= 0 and ty >=0 and tx < w and ty <h):
                self.target = tx,ty
                self.path = algo.astar((sx,sy),(tx,ty),g.castle_layer,dist)
                #print self.path
            #elif self.doing:
            #    self.yes_pickup(e)
                
        #print e   
#        if (e.type is MOUSEBUTTONDOWN and e.button == 3 or 
#            e.type == JOYBUTTONDOWN and e.button ==JOY_FIRE_BUTTON):
        if (e.type is MOUSEBUTTONDOWN and e.button == 1):

            # use up some steam in order to fire.
            self.unit.prep_fire()
                
        if (e.type is MOUSEBUTTONUP and e.button == 1):
            tx,ty = g.screen_to_tile(epos)
            #print 'right',tx,ty
            
            x,y = g.screen_to_tile(epos)
            cannon_pressure = self.unit.try_do_fire()

            tw,th = g.iso_w,g.iso_h
            cball_new(g,self.rect,(x*tw+tw/2,y*th+th/2), self.unit.stats['Damage'],cannon_pressure*1.5)







        if e.type == JOYBUTTONDOWN:
            pass

        #if self.direction_dy != 0:
        #    self.last_direction_dy = self.direction_dy
        #if self.direction_dx != 0:
        #    self.last_direction_dx = self.direction_dx

        if e.type == JOYAXISMOTION:
            if e.axis == 0:
                if round(e.value) < 0:
                    self.direction_dx = -1
                    self.last_direction_dx = self.direction_dx
                    self.last_direction_dy = self.direction_dy
                    #print "less than"
                elif round(e.value) > 0:
                    self.direction_dx = 1
                    self.last_direction_dx = self.direction_dx
                    self.last_direction_dy = self.direction_dy
                    #print "greater than"
                else:
                    #print "nothing!"
                    self.last_direction_dx = self.direction_dx
                    self.direction_dx = 0



            if e.axis == 1:
                if round(e.value) < 0:
                    self.direction_dy = -1
                    self.last_direction_dy = self.direction_dy
                    self.last_direction_dx = self.direction_dx
                elif round(e.value) > 0:
                    self.direction_dy = 1
                    self.last_direction_dy = self.direction_dy
                    self.last_direction_dx = self.direction_dx
                else:
                    self.last_direction_dy = self.direction_dy
                    self.direction_dy = 0
                

        if (e.type == JOYBUTTONUP and e.button ==JOY_FIRE_BUTTON):
            pass

            if 0:

                self.direction_dx = 0
                self.direction_dy = 0
                tx,ty = g.screen_to_tile(epos)
                x,y = g.screen_to_tile(epos)


                if self.unit.try_fire():
                    #print (x*tw+tw/2,y*th+th/2)
                    cball_new(g,s.rect,(x*tw+tw/2,y*th+th/2), self.unit.stats['Damage'])



        if (e.type == JOYBUTTONDOWN and e.button ==JOY_FIRE_BUTTON):

            # TODO: find out which way we are facing.
            # TODO: fire in facing direction.
            self.fire_state = "firing"


        if ((e.type == JOYBUTTONDOWN and e.button ==JOY_FIRE_BUTTON) or
            (e.type == KEYDOWN and e.key in [K_f, K_LCTRL, K_RCTRL, K_SPACE])):

            sx,sy = self.rect.centerx/tw, self.rect.centery/th

            #print "last dx:%s:   last dy:%s:" % (self.last_direction_dx, self.last_direction_dy)
            #print "sx:%s:   sy:%s:" % (sx, sy)

            
            
            self.unit.prep_fire()
            
        if ((e.type == JOYBUTTONUP and e.button ==JOY_FIRE_BUTTON) or
            (e.type == KEYUP and e.key in [K_f, K_LCTRL, K_RCTRL, K_SPACE])):
            facing_x, facing_y = (self.last_direction_dx, self.last_direction_dy)
            facing_x, facing_y = iso_facing_to_screen_facing(self.last_direction_dx, self.last_direction_dy)

            x = (5 * facing_x) + sx
            y = (5 * facing_y) + sy

            #x,y = g.screen_to_tile(epos)
            cannon_pressure = self.unit.try_do_fire()

            tw,th = g.iso_w,g.iso_h
            cball_new(g,self.rect,(x*tw+tw/2,y*th+th/2), self.unit.stats['Damage'],cannon_pressure)



            # use up some steam in order to fire.
            #if self.unit.try_fire():
            #    cball_new(g,s.rect,(x*tw+tw/2,y*th+th/2), self.unit.stats['Damage'])




        
        if self.doing:
            if (
                (e.type == KEYDOWN and self.doing and e.key == K_RETURN) or
                (e.type == KEYDOWN and self.doing and e.key == K_SPACE) or
                (e.type == MOUSEBUTTONDOWN and e.button == 3) or 
                (e.type == JOYBUTTONDOWN and e.button == JOY_PICKUP_BUTTON)):
                self.yes_pickup(e)


        if e.type == KEYUP:

            if e.key in [K_UP, K_w]:
                self.last_direction_dy = self.direction_dy
                self.direction_dy = 0
            elif e.key in [K_DOWN, K_s]:
                self.last_direction_dy = self.direction_dy
                self.direction_dy = 0
            elif e.key in [K_LEFT, K_a]:
                self.last_direction_dx = self.direction_dx
                self.direction_dx = 0
            elif e.key in [K_RIGHT, K_d]:
                self.last_direction_dx = self.direction_dx
                self.direction_dx = 0


        # some testing keys.
        if e.type == KEYDOWN:

            if e.key in [K_UP, K_w]:
                self.direction_dy = -1
                self.last_direction_dy = self.direction_dy
                self.last_direction_dx = self.direction_dx
            elif e.key in [K_DOWN, K_s]:
                self.direction_dy = 1
                self.last_direction_dy = self.direction_dy
                self.last_direction_dx = self.direction_dx
            elif e.key in [K_LEFT, K_a]:
                self.direction_dx = -1
                self.last_direction_dx = self.direction_dx
                self.last_direction_dy = self.direction_dy
            elif e.key in [K_RIGHT, K_d]:
                self.direction_dx = 1
                self.last_direction_dx = self.direction_dx
                self.last_direction_dy = self.direction_dy



            if e.key == K_KP_PLUS:
                self.unit.stats['Speed'] += 1

            elif e.key == K_KP_MINUS:
                self.unit.stats['Speed'] -= 1

            elif e.key == K_h:
                self.unit.hit(2)

            elif e.key == K_r:
                #tx, ty = self.item_tile.tx, self.item_tile.ty
                # drop rubble test.
                tx,ty = self.rect.centerx/tw, self.rect.centery/th

                self.g.set((tx,ty),7)

            if UPGRADE_FUN:

                if e.key == K_1:
                    self.upgrade_something("UpEngine Efficiency")
                elif e.key == K_2:
                    self.upgrade_something("UpEngine Speed")
                elif e.key == K_3:
                    self.upgrade_something("UpCannon Balls")
                elif e.key == K_4:
                    self.upgrade_something("UpCannon Power")
                elif e.key == K_5:
                    self.upgrade_something("UpArmour")
                elif e.key == K_6:
                    self.upgrade_something("UpSteam Tank")
                elif e.key == K_7:
                    self.upgrade_something("UpWater Tank")
                elif e.key == K_8:
                    self.upgrade_something("UpCoal Tank")

                elif e.key in [K_9, K_0]:
                    pprint.pprint( self.unit.stats )

                    
            if e.key == K_y:
                #get_savable_upgrade_amounts()
                print self.backup_castle()
            if e.key == K_u:
                #get_savable_upgrade_amounts()
                print self.reset_castle()
            if e.key == K_z:
                #get_savable_upgrade_amounts()
                print self.unit.stats


            #elif e.key == K_s:
            #    r = self.unit.try_use_steam(1)
            #    print "tried to use steam :%s:" % r


    def reset_castle(self):
        """ resets the castle stats to the backup.
        """

        if self.g.level.game.backup_castle_stats:
            print "before"
            print self.unit.stats
            self.unit.stats = copy.deepcopy(self.g.level.game.backup_castle_stats)
            print "after"
            print self.unit.stats
            if hasattr(self.g, "level"):
                if hasattr(self.g.level, "interface"):
                    self.g.level.interface.new_equipment(self.unit.stats)


    def backup_castle(self):
        """ backs the castle stats up.
        """
        self.g.level.game.backup_castle_stats = copy.deepcopy(self.unit.stats)





def castle_new(g,t,value):
    g.clayer[t.ty][t.tx] = 0
    s = CastleSprite(g.images['castle'],t.rect)
    s.g = g
    #print "castle"
    #print t.rect
    s.groups = g.string2groups('castle')
    s.agroups = g.string2groups('robot')
    
    s.effect = steam.Effect(32,1)

    g.castle = s

    g.sprites.append(s)
    if g.level.game.should_restore_stats:
        pass
        #TODO:
        s.reset_castle()
        s.unit.stats['Health'] = 10.

        
        
    


def castle_hit(g,s,a):
    
    #screams of smushing go here.
    a.state = 'dead'
        
    g.level.game.sm.Play(random.choice(sound_info.squish))

    
    #print g
    #print dir(s)
    #print a

    #print "castle hit"


    # test for collision between castle sprite and other types...
    # if the sprite has an item then pop up a dialog asking the 
    #  player if they want to pick it up.

    # the player shouldn't be able to move when being asked about coal.

    #NOTE: this is only a todo if we stop the castle from moving 
    #  whilst picking things up.
    #TODO: after picking not picking up the item, how long before asking again?
    #  maybe put a timer in there for 3. seconds before asking again.


    # store the item sprite to pick up on click.
    #s.item_sprite = a
    #s.last_hit_coal += 1
    






def castle_loop(g,s):
    #print "castle loop"

    s.unit.loop()

    # update the steam every second.
    #print g.level.game.ticks_passed

    #tw,th = g.iso_w,g.iso_h

    tw,th = g.iso_w,g.iso_h
    sx,sy = s.rect.centerx/tw,s.rect.centery/th


    s.last_update_steam += g.level.game.elapsed_time

    if s.can_move:
        #s.rect.x += 1

        speed = int(s.unit.stats['Speed'])

        kx,ky = 0,0

        # put in the joystick movement.
        if kx == 0:
            kx += s.direction_dx
            #s.dx = 0
        if ky == 0:
            ky += s.direction_dy
            #s.dy = 0


        # HACK: we do a little invert here.  because hex movement is weird.
        # we try to make up joy go up on screen.

        if 1:


            if kx == 0 and ky == -1:
                kx = -1
                ky = -1

            elif kx == 0 and ky == 1:
                kx = 1
                ky = 1

            elif kx == 1 and ky == -1:
                kx = 0
                ky = -1

            elif kx == -1 and ky == -1:
                kx = -1
                ky = 0
            elif kx == -1 and ky == 1:
                kx = 0
                ky = 1
            elif kx == 1 and ky == 1:
                kx = 1
                ky = 0

            elif kx == 1 and ky == 0:
                kx = 1
                ky = -1

            elif kx == -1 and ky == 0:
                kx = -1
                ky = 1

        #if ky == 1 and kx == 0:
        #    kx = 1
        #    ky = 1

        #print kx,ky

        keyboard_or_joy_speed_slow = 1
        #if ky == 0 or kx == 0:
#        if (kx,ky) != (0,0):
#
#            if (kx,ky) == (1,1) or (kx,ky) == (-1,-1) or kx == 0 or ky == 0:
#                keyboard_or_joy_speed_slow = 0



        if (kx,ky) != (0,0):
            keyboard_or_joy = 1

            tx,ty = sx+kx,sy+ky
            if g.castle_layer[ty][tx] == 0:
                s.path = [(tx,ty)]

            
        dx,dy = 0,0
        path = s.path
        while len(path) > 0:
            g.auto_scroll = True
            bx,by = path[0]
            if (bx,by) == (sx,sy): 
                path.pop(0)
                continue
            dx,dy = bx-sx,by-sy
            #v = 4
            #s.rect.x += sign(dx)*v
            #s.rect.y += sign(dy)*v
            dx,dy = sign(dx),sign(dy)
            break

        if keyboard_or_joy_speed_slow:
            speed = int(round(speed / 2.))

        if dx != 0 or dy != 0:
            #HACK: so i can move this guy ! :)
            if 1 or s.unit.try_move():
                s.rect.x += dx*speed
                s.rect.y += dy*speed
                
            if dx < 0:
                s.setimage(g.images['castle.left'])
            if dx > 0:
                s.setimage(g.images['castle.right'])

        #s.rect.clamp_ip(g.view)
    if s.last_hit_coal:
        #print "last_hit_coal, last"
        if s.last_hit_coal == s.last_loop:
            s.last_loop = 0
            s.last_hit_coal = 0
            s.no_pickup("")
        else:
            s.last_loop = s.last_hit_coal

    #okay, so the robots are scared to death of you...
    a = s
    for r in g.robots:
        rx,ry = r.x,r.y
        ax,ay = a.rect.x,a.rect.y
        dx,dy = rx-ax,ry-ay
        dist = (dx*dx+dy*dy)**0.5
        if dist and dist < 32*3:
            r.min = min(r._min,r.min+12.0)
            inc = 16.0
            x,y = rx + dx*inc/dist, ry + dy*inc/dist
            robot.robot_shove(g,r,(x,y))


    s.frame +=1



def cball_new(g,pos,dest, damage = 1.0,pressure=16):
    #g.level.game.sm.Play(random.choice(sound_info.cannon))
    #g.level.game.sm.Play(sound_info.cannon.nextone())

    if pressure < 9:
        g.level.game.sm.Play(sound_info.cannon[0], wait=3)
        print "cannon 1 sound"
    elif pressure >= 9 and pressure < 15:
        g.level.game.sm.Play(sound_info.cannon[1], wait=3)
        print "cannon 2 sound"
    elif pressure >= 15 and pressure < 25:
        g.level.game.sm.Play(sound_info.cannon[2], wait=3)
        print "cannon 3 sound"
    elif pressure >= 25:
        print "cannon 4 sound,  two cannon 3 sounds played at once."
        g.level.game.sm.Play(sound_info.cannon[2], wait=3)
        g.level.game.sm.Play(sound_info.cannon[2], wait=3)



    # Here we use a different graphic for the cannon balls depending on Damage.
    

    if damage <= 1.:
        img_name = 'cball'
        num_steam, num_steam_add = 20, 5
    elif damage > 1. and damage < 4.:
        img_name = 'cball2'
        num_steam, num_steam_add = 30, 10
    elif damage >= 4. and damage < 6.:
        img_name = 'cball3'
        num_steam, num_steam_add = 25, 15
    elif damage >= 6. and damage < 8.:
        img_name = 'cball4'
        num_steam, num_steam_add = 35, 20
    elif damage >= 8. and damage < 10.:
        img_name = 'cball4'
        num_steam, num_steam_add = 42, 23
    elif damage >= 10.:
        img_name = 'cball4'
        num_steam, num_steam_add = 50, 25

    
    s = isovid.Sprite(g.images[img_name],pos)

    # we assign the damage that is done by this cannon ball.
    s.damage = damage
    s.num_steam, s.num_steam_add = num_steam, num_steam_add
    

    s.frame = 0

    g.sprites.append(s)
    s.loop = cball_loop
    s.hit = cball_hit
    s.groups = g.string2groups("cball")
    s.agroups = g.string2groups("robot,cannon") #,factory,truck,cannon")
    
    #s.rect, s._rect
    
    dx,dy = dest[0]-s.rect.x,dest[1]-s.rect.y
    dist = (dx*dx+dy*dy)**0.5
    if dist <= 0: return 
    v = float(pressure)
    s.vx, s.vy = dx*v/dist,dy*v/dist
    s.vz = -5
    s.z = 0

    # we add a steam effect for when firing the cannon ball.
    #   It's steamyness is different depending on the damage of the cannon.
    rect = pygame.Rect(s.rect)
    rect.x += s.vx*2
    rect.y += s.vy *2
    effect.effect_new(g,rect,steam.Effect(num_steam,num_steam_add,12,0,(255,255,255)),20)
    
    
def cball_loop(g,s):
    try:
        s.rect.x += s.vx
    except AttributeError: 
        return

    s.rect.y += s.vy
    s.z += s.vz
    s.vz += 1
    if s.vz == 8:
        if s in g.sprites:
            g.sprites.remove(s)

        img_name = get_hole_for_damage(s.damage)
        g.bkgr_blit(g.images[img_name],(s.rect.centerx,s.rect.centery))


        g.level.game.sm.Play(sound_info.hitground.nextone(), wait=3)
        
        if HOLES_ARE_TILES:
            tw,th = g.iso_w,g.iso_h
            tx,ty = s.rect.centerx/tw,s.rect.centery/th
            
            dirs = [(0,0)]
            if HOLES_ARE_TILES > 1:
                dirs.extend([(-1,0),(1,0),(0,1),(0,-1)])
            for dx,dy in dirs:
                xx,yy = tx+dx,ty+dy
                v = g.get((xx,yy))
                if v in (0,7):
                    g.set((xx,yy),30)
        

        #ss = effect.effect_new(g,s.rect,steam.Effect(20,20,8,0,(117,110,94)),20)
        num_steam, num_steam_add = s.num_steam, s.num_steam_add
        ss = effect.effect_new(g,s.rect,steam.Effect(int(num_steam*2), int(num_steam_add*2),num_steam_add,0,(0,0,0)),20)
        ss.z = 8
        
        print 'gahhh'
        a = s
        for r in g.robots:
            rx,ry = r.x,r.y
            ax,ay = a.rect.x,a.rect.y
            dx,dy = rx-ax,ry-ay
            dist = (dx*dx+dy*dy)**0.5
            if dist and dist < 32*4:
                r.min = min(r._min,r.min+12.0)
                inc = 31.0
                x,y = rx + dx*inc/dist, ry + dy*inc/dist
                robot.robot_shove(g,r,(x,y))

            if dist < 32*3: #1.5:
                r.state = 'dead'

    #print s.rect
    s.frame += 1
    
class SpriteBlast:
    def __init__(self):
        self.e1 = explode.Effect(64,16)
        #self.e2 = steam.Effect(128,32,24,0)
        self.e2 = steam.Effect(120,40,16,0)
        
    def loop(self,pos):
        self.e1.loop(pos)
        self.e2.loop(pos)
        
    def paint(self,screen,origin):
        self.e1.paint(screen,origin)
        self.e2.paint(screen,origin)

def cball_hit(g,a,b):

    # we just destroy 'robots'... aka peasants.  cball keeps going.
    if hasattr(b,'type') and b.type == 'robot':
        if b in g.sprites:
            #g.sprites.remove(b)
            b.state = 'dead'
    else:
        return cball_hit_old(g,a,b)

def get_hole_for_damage(damage):
    if damage <= 1.:
        img_name = 'hole'
    elif damage > 1. and damage < 4.:
        img_name = 'hole2'
    elif damage >= 4. and damage < 6.:
        img_name = 'hole3'
    elif damage >= 6. and damage < 8.:
        img_name = 'hole4'
    elif damage >= 8. and damage < 10.:
        img_name = 'hole4'
    elif damage >= 10.:
        img_name = 'hole4'
    return img_name


def cball_hit_old(g,a_cannon_ball,b):

    ss = effect.effect_new(g,b.rect,steam.Effect(60,20,4,0),20)


    # lets hit the unit, and see if it dies.
    if b.unit.hit(a_cannon_ball.damage):

        g.level.game.sm.Play(sound_info.destroyenemy.nextone())

#         if b.unit.name == "factory":
#             g.level.game.state = states.NextLevel(g.level.game, g.level.game.state)
#             print "you won!"
#             return

        if b in g.sprites:
            g.sprites.remove(b)

        img_name = get_hole_for_damage(a_cannon_ball.damage)

        g.bkgr_blit(g.images[img_name],(a_cannon_ball.rect.centerx,a_cannon_ball.rect.centery))
        
        #do an explosion here...
        #that looks like...
        ss = effect.effect_new(g,b.rect,SpriteBlast(),20)
    else:
        # we only play the hit sound if the thing doesn't die?
        g.level.game.sm.Play(sound_info.hitenemy.nextone())
        

    try:
        g.sprites.remove(a_cannon_ball)
    except ValueError:
        # already removed??? yeah that happens :)
        # if the ball hits more than one tile
        pass


    print "hit!", b.unit.name
    pass

