if 0:
    try:
        #0/0 #HACK: so i can CTRL-c out
        import psyco
        psyco.profile()
        print 'psyco installed'
    except:
        print 'psyco not installed'

import os,sys,time,copy


import pygame
from pygame.locals import *





from pgu import engine
from pgu import timer

from const import *

if 0:
    # this can be used to figure out how big the desktop is...
    pygame.display.init()
    screen = pygame.display.set_mode((0,0))
    SW, SH = screen.get_size()
    import const
    const.SW, const.SH = screen.get_size()



import states
import level
import units
import sounds

import traceback

import intro
import menu



class Game(engine.Game):
    def init(self):
        #self.timer = timer.Timer(FPS)
        self.timer = timer.Speedometer() 
        self.clock = pygame.time.Clock()
        self.elapsed_time = 0
        self.last_time = time.time()
        self.cur_time = self.last_time

        self.clock.tick(FPS)

        # start a song playing here as things load.
        self.sm = sounds.SoundManager()
        #self.sm.PlayMusic( data_dir('music', "intro.ogg") )
        self.sm.PlayMusic( data_dir('intro', "intro1.ogg") )
        self.sm.Load()


        # for saving the states between levels.
        

        self.data_reset()
        self.should_restore_stats = True
        


    def tick(self):
        r =  self.timer.tick()
	if r != None: 
            #print r
            print "fps :%s:" % self.clock.get_fps()
        self.cur_ticks = self.clock.tick(FPS) #to not limit it
        self.cur_time = time.time()

        self.elapsed_time = self.cur_time - self.last_time

        self.sm.Update(self.elapsed_time)
        #print "&"*20
        #print self.elapsed_time
        #print self.clock.get_fps()
        #for name in dir(self):
        #    print name,getattr(self,name)


    def save_castle_data(self):
        """
        """
        
    def data_reset(self):
        self.data = {}
        self.data['levels'] = []
        self.upgradable_amounts = None
        self.castle_stats = None

        self.backup_upgradable_amounts = None
        self.backup_castle_stats = None

        
    def event(self,e):
        #capture special events on a top level,
        #should only be used for screen shots, forced quits, 
        #magic cheat buttons, etc... debug keys and the like ...
        if e.type is QUIT:
            self.state = engine.Quit(self)
            return 1
        
#         if e.type is KEYDOWN and e.key == K_F10:
#             self.state = states.SPause(self,self.state)
#             return 1

#         if e.type == KEYDOWN and e.key == K_ESCAPE:
#             self.state = engine.Quit(self)
#             return 1






def do_main(no_intro = 0, the_level = 0):
    global flags

    pygame.mixer.pre_init(22050, -16, 2, 1024)

    pygame.init()
    pygame.font.init()
    #pygame.display.set_caption("The Wrath of ZANTHOR") #It's powered by steam!")
    pygame.display.set_caption("The Wrath of ZANTHOR!  It's powered by steam!  h key for help")

    #flags = FULLSCREEN
    print flags
    print (SW,SH)
    screen = pygame.display.set_mode((SW,SH), flags)



    pygame.joystick.init()

    joystics =[]

    num_joys = pygame.joystick.get_count()


    print "initialising joys", num_joys
    for x in range(num_joys):
        print "x joy is:", x
        j=pygame.joystick.Joystick(x)
        j.init()
        joystics.append(j)

    print "initialising joys: done."





    game = Game()
    game.should_restore_stats = True
    game.backup_upgradable_amounts = None
    game.backup_castle_stats = None


    # the intro is not done first.
    #game.run(states.Title(game),screen)
    if no_intro == 0:
        game.run(intro.Intro(game),screen)
        
    elif no_intro == 1:
        #game.run(level.Level(game, 0,100),screen)
        game.run(menu.Menu(game),screen)
    elif no_intro == 3:
        # we load the level number from the levels defined in menu.
        n = menu.data[no_intro][4]
        perc = menu.data[no_intro][5]
        music = menu.data[no_intro][7]
        game.run(level.Level(game,n,perc,music),screen)
    else:
        game.run(level.Level(game,no_intro,100,None),screen)
    


def main():
    global flags

    if 'speed' in sys.argv:
        FPS = 65535

    the_level = None
    #flags ^= FULLSCREEN
    flags = 0
    if 'fullscreen' in sys.argv or 'full' in sys.argv:
        flags ^= FULLSCREEN

    if 'nointro' in sys.argv or "no" in sys.argv:
        no_intro =1
    elif 'next' in sys.argv or "nextlevel" in sys.argv:
        no_intro =2 #uhh, i removed this because i'm dumb
    elif 'l' in sys.argv:
        # main.py l 5
        # we play the level given as an index into menu.data
        the_level = int(sys.argv[-1])
        no_intro =3
    else:
        no_intro =0
        
    #jump to any level by specifying, e.g. "level8.tga"
    for fname in sys.argv:
        if '.tga' in fname:
            no_intro = fname


    if "profile" in sys.argv:
        import hotshot
        import hotshot.stats
        import tempfile
        import os
 
        profile_data_fname = tempfile.mktemp("prf")
        try:
            prof = hotshot.Profile(profile_data_fname)
            prof.run('do_main(no_intro, the_level = the_level)')
            del prof
            s = hotshot.stats.load(profile_data_fname)
            s.strip_dirs()
            print "cumulative\n\n"
            s.sort_stats('cumulative').print_stats()
            print "By time.\n\n"
            s.sort_stats('time').print_stats()
            del s
        finally:
            # clean up the temporary file name.
            try:
                os.remove(profile_data_fname)
            except:
                # may have trouble deleting ;)
                pass
    else:
        try:
            do_main(no_intro, the_level = the_level)
        except:
            traceback.print_exc(sys.stderr)
