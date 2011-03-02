"""Isometric tile engine.

<p>Note -- this engine is not finished, any may not work for your 
particular needs.  If you are able to update it, help would be 
greatly appreciated!</p>

<p>please note that this file is alpha, and is subject to modification in
future versions of pgu!</p>

"""
print 'pgu.isovid','This module is alpha, and is subject to change.'

from pgu.vid import *
import pygame
import random

import time, os
from const import data_dir

try:
    import const
    CACHE_USE_LEVEL_CACHE = const.CACHE_USE_LEVEL_CACHE
except:
    CACHE_USE_LEVEL_CACHE = 0


class Isovid(Vid):
    """Create an iso vid engine.  See [[vid]]"""
    def update(self,screen):
        return self.paint(screen)
    
    def bkgr_blit(self,img,pos):
        #pos must be an iso coordinate, centered
        
        tlayer = self.tlayer
        w,h = len(tlayer[0]),len(tlayer)
        
        tmp,y1 = self.tile_to_view((0,0))
        x1,tmp = self.tile_to_view((0,h+1))
        tmp,y2 = self.tile_to_view((w+1,h+1))
        x2,tmp = self.tile_to_view((w+1,0))
        
        pos = self.iso_to_view(pos)
        
        dest = (-x1+pos[0]-img.get_width()/2,-y1+pos[1]-img.get_height()/2)
        print dest
        self.bkgr.blit(img,dest)
        

    def load_bkgr_cache(self, level_fname, tiles_fname):
        """ try and load the painted background from cache.
            Returns True if it can load the background.  Otherwise False.
        """

        if not CACHE_USE_LEVEL_CACHE:
            return False

        #try:
        # check if the image is in cache.
        exts = [".jpg", ".tga"]
        found_image = False

        for ext in exts:
            cached_fname = data_dir('cache', 'levels', os.path.basename(level_fname))
            cached_fname = cached_fname[:-4] + ext

            if os.path.exists(cached_fname):
                # check if the cached file is newer.
                fname_stat = os.stat(level_fname)
                cached_stat = os.stat( cached_fname )
                if fname_stat.st_mtime > cached_stat.st_mtime:
                    return False
                found_image = True
                break
                #TODO: check the tiles mtime too.

        if found_image:
            print "loading :%s:" % cached_fname
            self.bkgr = pygame.image.load(cached_fname)
            self.bkgr = self.bkgr.convert()
            return True
        else:
            return False



        # check if the cached image is newer than the level tga, and the tile tga.

        # if it is valid in cache, load to the background.






    def paint(self,screen):
        
        sw,sh = screen.get_width(),screen.get_height()
        
        tlayer = self.tlayer
        blayer = self.blayer
        zlayer = self.zlayer
        
        w,h = len(tlayer[0]),len(tlayer)
        if not hasattr(self,'bkgr') and not self.load_bkgr_cache(self.level_fname, self.tiles_fname):
            t1 = time.time()

            self.bkgr = None
            v = self.view
            tmp,y1 = self.tile_to_view((0,0))
            x1,tmp = self.tile_to_view((0,h+1))
            tmp,y2 = self.tile_to_view((w+1,h+1))
            x2,tmp = self.tile_to_view((w+1,0))

            ww,hh = x2-x1,y2-y1
            self.view = pygame.Rect(x1,y1,ww,hh)
            s = pygame.Surface((ww,hh)).convert()
            s.fill((128,0,0))
            self.paint(s)
            
            s2 = pygame.Surface((ww,hh)).convert()
                
            for n in [1,2]: #,4]:
                s2.blit(s,(0,0))
                s.set_alpha(48)
                for x,y in [(-16/n,0),(16/n,0),(0,-8/n),(0,8/n)]:
                    s2.blit(s,(x+random.randrange(-2,3),y+random.randrange(-2,3)))
                s.set_alpha(255)
                s2,s = s,s2
                

            self.bkgr = s
            t2 = time.time()
            print "_" * 40
            print "time to paint background: %s" % (t2 - t1)


            # this is the caching stuff.
            if CACHE_USE_LEVEL_CACHE:
                if t2 - t1 > 1.0:
                    # the machine didn't process this fast enough, so we cache it.
                    if not os.path.exists(data_dir('cache')):
                        os.mkdir(data_dir('cache'))
                        if not os.path.exists(data_dir('cache', 'levels')):
                            os.mkdir(data_dir('cache', 'levels'))

                    try:
                        cached_fname = data_dir('cache', 'levels', os.path.basename(self.level_fname))
                        pygame.image.save(self.bkgr, cached_fname)
                    except:
                        pass
                        # no cache for this person.  Maybe no permission.




        iso_w,iso_h,iso_z,tile_w,tile_h,base_w,base_h = self.iso_w,self.iso_h,self.iso_z,self.tile_w,self.tile_h,self.base_w,self.base_h
        
        base_h2 = base_h/2
        base_w2 = base_w/2
        
        bot = tile_h/base_h2
        todo_max = sh/base_h2+bot
        #todo = [[] for y in xrange(0,todo_max)]
        todo = {}
        
        self.view.w,self.view.h = sw,sh
        view = self.view
        adj = self.adj = pygame.Rect(-self.view.x,-self.view.y,0,0)
        
        shift = pygame.Rect(adj.x,adj.y/base_h2*base_h2,0,0)
        
        for s in self.sprites:
            self.sprite_calc_irect(s)
            
            if s.irect.colliderect(self.view):
                x,y = self.iso_to_view((s.rect.centerx,s.rect.centery))
                #v = (y+adj.y)/base_h2 - 1
                #v = (y+shift.y)/base_h2 -1
                #if v >= 0 and v < todo_max:
                #    todo[v].append((s,s.image,s.irect))
                v = y/base_h2 -1
                if v not in todo: todo[v] = []
                todo[v].append((s,s.image,s.irect))
                
                if hasattr(s,'effect'):
                    e = s.effect
                    if hasattr(e,'zloop'):
                        z = 0
                        if hasattr(s,'z'):
                            z = s.z
                        
                        irect= s.irect
                        e.zloop((s.irect.x+irect.w/2,s.irect.y+irect.h/2+z),v)
                        
                        for z,img,pos in e.zpaint():
                            if z not in todo: todo[z] = []
                            todo[z].append((None,img,pygame.Rect(pos[0],pos[1],1,1)))
                            
                    
            
            #else: print 'doesnt fit',v
                
        w,h = len(tlayer[0]),len(tlayer)
        tiles = self.tiles
        
        if self.bkgr != None:
            #""
            if self.bounds == None:
                tmp,y1 = self.tile_to_view((0,0))
                x1,tmp = self.tile_to_view((0,h+1))
                tmp,y2 = self.tile_to_view((w+1,h+1))
                x2,tmp = self.tile_to_view((w+1,0))
                self.bounds = pygame.Rect(x1,y1,x2-x1,y2-y1)
            #""
            
            if self.bounds != None: self.view.clamp_ip(self.bounds)
            #print self.bounds

        ox,oy = self.screen_to_tile((0,0))
        sx,sy = self.iso_to_view((ox*iso_w,oy*iso_h))
        dx,dy = sx - self.view.x,sy - self.view.y
        
        
        if self.bkgr == None:
            print 'paint the background!!!'
            t1 = time.time()

            for i2 in xrange(-bot,self.view.h/base_h2+bot):
                tx,ty = ox + i2/2 + i2%2,oy + i2/2
                x,y = (i2%2)*base_w2 + dx,i2*base_h2 + dy
                
                #to adjust for the -1 in i1
                x,tx,ty = x-base_w,tx-1,ty+1
                for i1 in xrange(-1,self.view.w/base_w+2): #NOTE: not sure why +2
                    #print tx,ty
                    if ty >= 0 and ty < h and tx >= 0 and tx < w:
                        z = zlayer[ty][tx]*iso_z
                        if blayer != None:
                            n = blayer[ty][tx]
                            if n != 0:
                                t = tiles[n]
                                if t != None and t.image != None:
                                    screen.blit(t.image,(x-base_w2,y+z))
                                    
                                    
                    tx += 1
                    ty -= 1
                    x += base_w

            t2 = time.time()
            print "*" * 40
            print "time to paint background: %s" % (t2 - t1)

            return
        
        tmp,y1 = self.tile_to_view((0,0))
        x1,tmp = self.tile_to_view((0,h+1))
        tmp,y2 = self.tile_to_view((w+1,h+1))
        x2,tmp = self.tile_to_view((w+1,0))
        
        #print x1,y1,adj
        screen.blit(self.bkgr,(x1+adj.x,y1+adj.y))
        
        
        for i2 in xrange(-bot,self.view.h/base_h2+bot):
            tx,ty = ox + i2/2 + i2%2,oy + i2/2
            x,y = (i2%2)*base_w2 + dx,i2*base_h2 + dy
            
            #to adjust for the -1 in i1
            x,tx,ty = x-base_w,tx-1,ty+1
            for i1 in xrange(-1,self.view.w/base_w+2): #NOTE: not sure why +2
                if ty >= 0 and ty < h and tx >= 0 and tx < w:
                    z = zlayer[ty][tx]*iso_z
#                     if blayer != None:
#                         n = blayer[ty][tx]
#                         if n != 0:
#                             t = tiles[n]
#                             if t != None and t.image != None:
#                                 screen.blit(t.image,(x-base_w2,y+z))
                    n = tlayer[ty][tx]
                    if n != 0:
                        t = tiles[n]
                        if t != None and t.image != None:
                            screen.blit(t.image,(x-base_w2,y-(t.image_h-base_h)+z))
            
                tx += 1
                ty -= 1
                x += base_w
            #for s,img,irect in todo[y/base_h2]:
            #if i2 in todo:
            
            zz = (y - adj.y) / base_h2
            if zz not in todo: continue
            for s,img,irect in todo[zz]:
                z = 0
                if hasattr(s,'z'):
                    z = s.z
                screen.blit(img,(irect.x+adj.x,irect.y+adj.y+z))
                if hasattr(s,'effect'):
                    if not hasattr(s.effect,'zloop'):
                        s.effect.loop((s.irect.x+irect.w/2,s.irect.y+irect.h/2+z))
                        s.effect.paint(screen,(-adj.x,-adj.y))#(irect.x+adj.x+irect.w/2,irect.y+adj.y+irect.h/2))

        self.updates = []
        return [pygame.Rect(0,0,screen.get_width(),screen.get_height())]
        
    def iso_to_view(self,pos):
        tlayer = self.tlayer
        w,h = len(tlayer[0]),len(tlayer)
        
        x,y = pos
        
        #nx,ny = (h*self.iso_w + x - y)/2, (0 + x + y)/2
        nx,ny = (x - y)/2, (0 + x + y)/2
        
        return (nx * self.base_w / self.iso_w), (ny * self.base_h / self.iso_h)

    def view_to_iso(self,pos):
        tlayer = self.tlayer
        w,h = len(tlayer[0]),len(tlayer)
        
        x,y = pos
        
        x,y = x*self.iso_w/self.base_w, y*self.iso_h/self.base_h
        
        #x -= (self.iso_w/2) * h
        #x -= (self.iso_w/2) * h
        
        nx = (x+y) 
        ny = y*2-nx
    
        return nx,ny
    
    def tile_to_view(self,pos):
        return self.iso_to_view((pos[0]*self.iso_w,pos[1]*self.iso_h))
    
    def screen_to_tile(self,pos):
        x,y = pos
        x += self.view.x
        y += self.view.y
        x,y = self.view_to_iso((x,y))
        return x/self.iso_w,y/self.iso_h
        
    def tile_to_screen(self,pos):
        x,y = self.iso_to_view((pos[0]*self.iso_w,pos[1]*self.iso_h))
        return x-self.view.x,y-self.view.y
    
    def tga_load_tiles(self,fname,size,tdata={}):
        Vid.tga_load_tiles(self,fname,size,tdata)
        
        self.tile_w,self.tile_h = size
        self.iso_w,self.iso_h,self.iso_z = self.tile_w,self.tile_w,1
        self.base_w,self.base_h = self.tile_w,self.tile_w/2

        self.tiles_fname = fname
    

    def tga_load_level(self,fname,bg=0):
        """Load a TGA level.  
        
        <pre>Vid.tga_load_level(fname,bg=0)</pre>
        
        <dl>
        <dt>g        <dd>a Tilevid instance
        <dt>fname    <dd>tga image to load
        <dt>bg        <dd>set to 1 if you wish to load the background layer
        </dl>
        """

        if type(fname) == str: 
            img = pygame.image.load(fname)
            self.level_fname = fname
        else: 
            img = fname
            self.level_fname = repr(fname)

        w,h = img.get_width(),img.get_height()
        pad = 12
        self.resize((w+pad*2,h+pad*2),bg)
        w,h = self.size
        for y in range(0,h):
            for x in range(0,w):
                self.tlayer[y][x] = 0x1c
        w,h = img.get_width(),img.get_height()
        for y in range(0,h):
            for x in range(0,w):
                t,b,c,_a = img.get_at((x,y))
                self.tlayer[y+pad][x+pad] = t
                if bg: self.blayer[y+pad][x+pad] = b
                self.clayer[y+pad][x+pad] = c
                
     
    def resize(self,size,bg=0):
        Vid.resize(self,size,bg)
        
        tlayer = self.tlayer
        w,h = len(tlayer[0]),len(tlayer)
        
        self.zlayer = [[0 for x in xrange(0,w)] for y in xrange(0,h)]

        


    def sprite_calc_irect(self,s):
        tlayer = self.tlayer
        w,h = len(tlayer[0]),len(tlayer)
        zlayer = self.zlayer
        
        x,y = self.iso_to_view((s.rect.centerx,s.rect.centery))
        tx,ty = s.rect.centerx/self.iso_w,s.rect.centery/self.iso_h
        z = 0
        if ty >= 0 and ty < h and tx >= 0 and tx < w:
            z = zlayer[ty][tx]*self.iso_z
        
        nx,ny = x - s.shape.centerx, y - s.shape.centery + z
        
        s.irect.x,s.irect.y = nx,ny
        
        
        
    def run_codes(self,cdata,rect):
        #HACK to make run_codes work
        w,h = self.iso_w,self.iso_h
         
        img = self.tiles[0].image
        
        self.tiles[0].image = pygame.Surface((w,h))
        r = Vid.run_codes(self,cdata,rect)
        self.tiles[0].image = img
        return r
        
        
    def set(self,pos,v):
        """Set a tile in the foreground to a value.
        
        <p>Use this method to set tiles in the foreground, as it will make
        sure the screen is updated with the change.  Directly changing
        the tlayer will not guarantee updates unless you are using .paint()
        </p>
        
        <pre>Vid.set(pos,v)</pre>
        
        <dl>
        <dt>pos <dd>(x,y) of tile
        <dt>v <dd>value
        </dl>
        """
        
        #if self.tlayer[pos[1]][pos[0]] == v: return
        self.tlayer[pos[1]][pos[0]] = v
        #self.alayer[pos[1]][pos[0]] = 1
        
        #self.robot_layer[pos[1]][pos[0]] = int(v!=0)
        self.robot_layer[pos[1]][pos[0]] = int(v in (3,4,5,6,30))
        self.truck_layer[pos[1]][pos[0]] = int(v>1)
        self.castle_layer[pos[1]][pos[0]] = int(v in (3,4,5,6,30))
        
        #self.updates.append(pos)
        
        


        
        
        
        
        
        
        
        
        
        
        
        
        
        
