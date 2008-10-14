import pygame
import sound_info
PRINTDEBUG = 0


def tile_block(g,t,s):
    a = s
    
    c = t.config
    if (c['top'] == 1 and a._rect.bottom <= t._rect.top and a.rect.bottom > t.rect.top):
        a.rect.bottom = t.rect.top
    if (c['left'] == 1 and a._rect.right <= t._rect.left and a.rect.right > t.rect.left):
        a.rect.right = t.rect.left
    if (c['right'] == 1 and a._rect.left >= t._rect.right and a.rect.left < t.rect.right):
        a.rect.left = t.rect.right
    if (c['bottom'] == 1 and a._rect.top >= t._rect.bottom and a.rect.top < t.rect.bottom):
        a.rect.top = t.rect.bottom


class WallBlast:
    def __init__(self):
        import explode,steam
        #self.e1 = explode.Effect(64,16)
        #self.e2 = steam.Effect(128,32,24,0)
        self.e2 = steam.Effect(120,40,16,0,(143,136,129))
        
    def loop(self,pos):
        #self.e1.loop(pos)
        self.e2.loop(pos)
        
    def paint(self,screen,origin):
        #self.e1.paint(screen,origin)
        self.e2.paint(screen,origin)

def tile_wall(g,t,s):
    #when hit, this cracks
    
    if s not in g.sprites: return
    g.sprites.remove(s)

    g.level.game.sm.Play(sound_info.hitwall.nextone())
        
    tx,ty = t.tx,t.ty
    for a,dx,dy in [(2,0,0),(1,-1,0),(1,1,0),(1,0,1),(1,0,-1)]:
        v = g.get((tx+dx,ty+dy))
        if v in (4,5,6):
            v = min(7,v + a)
            g.set((tx+dx,ty+dy),v)
            
    import effect
    tw,th = g.iso_w,g.iso_h
    e = effect.effect_new(g,pygame.Rect(t.tx*tw+tw/2,t.ty*th+th/2,1,1),WallBlast(),20)
    e.z = s.z+16
    

def tile_coal(g,t,s):
    #print 'you hit coal'
    pass

    g.level.game.sm.Play(sound_info.coal.nextone())

    s.check_for_pickup(g, t)


def tile_water(g,t,s):
    #print 'you hit water'
    pass
    g.level.game.sm.Play(sound_info.water.nextone())

    s.check_for_pickup(g, t)

def tile_rubble(g,t,s):
    print 'you hit rubble'

    s.check_for_pickup(g, t)

def tile_part(g,t,s):
    #print "*"*30
    #print type(s)
    #print s
    #print g
    if PRINTDEBUG: print "generic tile part"
    s.check_for_pickup(g, t)

def tile_cannon(g,t,s):
    if PRINTDEBUG: print "you hit cannon part"
    s.check_for_pickup(g, t)

def tile_engine(g,t,s):
    if PRINTDEBUG: print "you hit engine part"
    s.check_for_pickup(g, t)

def tile_watertank(g,t,s):
    if PRINTDEBUG: print "you hit watertank part"
    s.check_for_pickup(g, t)

def tile_coalstorageroom(g,t,s):
    if PRINTDEBUG: print "you hit coalstorageroom part"
    s.check_for_pickup(g, t)

def tile_armour(g,t,s):
    if PRINTDEBUG: print "you hit armour part"
    s.check_for_pickup(g, t)


def tile_limit(g,t,s):
    print s,'out of bounds'
    if s in g.sprites:
        g.sprites.remove(s)
    #HACK
    if s in g.robots:
        g.robots.remove(s) 
    s.state = 'dead'




