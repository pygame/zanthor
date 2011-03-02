"""
file: sounds.py
purpose: to load all the sounds, and manage the playing of them.

Probably have different sets of sounds in here somehow.

NOTE: not using pygames channel queueing as it only allows one sound to be 
  queued.  Also the sound can only be queued on a certain channel.

"""



import pygame
import os
import glob
import time

from pygame.locals import *
from const import data_dir

SOUND_PATH = data_dir("sounds")


EXTENSIONS = [".wav", ".ogg"]

def get_sound_list(path = SOUND_PATH, extensions = EXTENSIONS):
    """ gets a list of sound names without thier path, or extension.
    """
    # load a list of sounds without path at the beginning and .ogg at the end.
    sound_list = []
    for ext in extensions:
        sound_list.extend( map(lambda x:x[len(path)+1:-4], 
                               glob.glob(os.path.join(path,"*" + ext)) 
                           ))

    return sound_list
       

SOUND_LIST = get_sound_list()

def init(path = SOUND_PATH):
    """
    """
    global SOUND_LIST, SOUND_PATH
    SOUND_PATH = path
    SOUND_LIST = get_sound_list(path)



        



class SoundManager:
    """ Controls loading, mixing, and playing the sounds.
        Having seperate classes allows different groups of sounds to be 
         loaded, and unloaded from memory easily.

        Useage:
            sm = SoundManager()
            sm.Load()

            Then every loop.
            sm.Update(elapsed_time_in_seconds)

            Then to play sounds.  eg to play data/sounds/asound.ogg
            sm.Play("asound")
    """


    def __init__(self, sound_list = SOUND_LIST, sound_path = SOUND_PATH, extensions = EXTENSIONS):
        """
	"""
	self.mixer = None
	self.music = None
	self.sounds = {}
	self.chans = {}

	self._debug_level = 0

        self.sound_list = sound_list
        self.sound_path = sound_path
        self.extensions = extensions


        # sounds which are queued to play.
        self.queued_sounds = []

    def _debug(self, x, debug_level = 0):
        """
	"""
        print x
	if self._debug_level > debug_level:
	    print x



    def Load(self, sound_list = []):
	"""Loads sounds."""
        sounds = self.sounds

	if not pygame.mixer:
	    for name in sound_list:
		sounds[name] = None
	    return
	for name in sound_list:
	    if not sounds.has_key(name):
                sound = None
                for ext in self.extensions:
                    fullname = os.path.join(self.sound_path, name+ext)
                    if(os.path.exists(fullname)):
                        try: 
                            sound = pygame.mixer.Sound(fullname)
                        except: 
                            sound = None
                            self._debug("Error loading sound", fullname)
                        break
                if not sound:
                    self._debug("could not find sound:%s: at path :%s:" % (name, self.sound_path))
		sounds[name] = sound


    def GetSound(self, name):
        """ Returns a Sound object for the given name.
	"""
	if not self.sounds.has_key(name):
	    self.Load([name])

	return self.sounds[name]



    def Stop(self, name):
        if self.chans.has_key(name):
            if self.chans[name]:
                if self.chans[name].get_busy():
                    self.chans[name].stop()

    def StopAll(self):
        """ stops all sounds.
        """

        for name in self.chans.keys():
            self.Stop(name)

    def IsSoundPlaying(self, name):

        if self.chans.has_key(name):
            return self.chans[name].get_busy()
        else:
            return 0


    def Play(self, name, 
                   volume=[1.0, 1.0], 
                   wait = 0,
                   loop = 0):
        """ Plays the sound with the given name.
	    name - of the sound.
	    volume - left and right.  Ranges 0.0 - 1.0
	    wait - used to control what happens if sound is allready playing:
                0 - will not wait if sound playing.  play anyway.
                1 - if there is a sound of this type playing wait for it.
                2 - if there is a sound of this type playing do not play again.
                3 - will not wait.  No queing of the sounds.
            loop - number of times to loop.  -1 means forever.
	"""

        vol_l, vol_r = volume

	sound = self.GetSound(name)

	if sound:
            if wait in [1,2]:

                if self.chans.has_key(name) and self.chans[name].get_busy():
                    if wait == 1:
                        # sound is allready playing we wait for it to finish.
                        self.queued_sounds.append((name, volume, wait))
                        return
                    elif wait == 2:
                        # not going to play sound if playing.
                        return
                        

	    self.chans[name] = sound.play(loop)


            if not self.chans[name]:
                if loop == 1:
                    # forces a channel to return. we fade that out,
                    #  and enqueue our one.
                    if pygame.mixer:
                        self.chans[name] = pygame.mixer.find_channel(1)

                    #TODO: does this fadeout block? YES.
                    self.chans[name].fadeout(100)
                    self.chans[name].queue(sound)
                else:
                    # the pygame api doesn't allow you to queue a sound and
                    #  tell it to loop.  So we hope for the best, and queue
                    #  the sound.
                    if wait not in [3]:
                        self.queued_sounds.append((name, volume, wait))
                    # delete the None channel here.
                    del self.chans[name]

            elif self.chans[name]:
                #self.chans[name].set_volume(vol_l, vol_r)
                self.chans[name].set_volume(vol_l)




    def Update(self, elapsed_time):
        """
        """

        for name in self.chans.keys():
            if not self.chans[name]:
                # it may be a NoneType I think.
                del self.chans[name]
            elif not self.chans[name].get_busy():
                del self.chans[name]
        old_queued = self.queued_sounds
        self.queued_sounds = []

        for snd_info in old_queued:
            # we do not queue up sounds with wait 0.
            if snd_info not in [3]:
                self.Play(*snd_info)



    def PlayMusic(self, musicname):
        """ Plays a music track.  Only one can be played at a time.
	    So if there is one playing, it will be stopped and the new 
             one started.
	"""


        try:
            music = pygame.mixer.music
        except:
            music = None

	if not music: return
	if music.get_busy():
	    #we really should fade out nicely and
	    #wait for the end music event, for now, CUT 
	    music.stop()
	#fullname = os.path.join('sounds', musicname)
	fullname = musicname
        try:
            music.load(fullname)
        except pygame.error:
            return
        
	music.play(-1)
	music.set_volume(1.0)

    def PauseMusic(self):
        self._unp_PauseMusic(1)

    def UnPauseMusic(self):
        self._unp_PauseMusic(0)


    def _unp_PauseMusic(self, p):
        try:
            music = pygame.mixer.music
        except:
            music = None

        if music:
            if p:
                music.pause()
            else:
                music.unpause()
        






class ChannelFader:
    """ For fading a channel in and out.

        cf = ChannelFader(achannel)

        # fade out to 20% volume over 2.5 seconds.
        cf.fade_out(2.5, 0.2)

        # fade in to full volume over 12.5 seconds.
        cf.fade_out(12.5, 1.0)

        # called every tick with the elapsed seconds.
        cf.Update(0.01)
    """

    def __init__(self, channel):
        self.channel = channel

        self.seconds = 0
        self.volume_to= 0
        self.fade_direction = -1
        self.last_volume = self.channel.get_volume()
        self.elapsed_time = 0
        self.passed_time = 0


    def _fade(self, seconds, volume_to, direction):
        self.seconds = seconds
        self.volume_to= volume_to
        self.fade_direction = direction
        self.last_volume = self.channel.get_volume()
        self.change_per_time = (volume_to - self.last_volume) / seconds

    def fade_in(self, seconds, volume_to):
        self._fade(seconds, volume_to, 1)


    def fade_out(self, seconds, volume_to):
        self._fade(seconds, volume_to, -1)

    def stop_fade(self):
        self.fade_direction = 0

    def Update(self, elapsed_time):
        """ - probably needs the real elapsed time.  not gameplay elapsed time.
        """
        
        if self.fade_direction == 0:
            return


        # we use the stored last volume incase something else is changing
        #  the volume.
        new_volume = self.last_volume + (self.change_per_time * elapsed_time)
        #print "prev new volume:%s" % new_volume

      
        if self.fade_direction == -1:
            if new_volume < self.volume_to:
                new_volume = self.volume_to
                self.stop_fade()

        if self.fade_direction == 1:
            if new_volume > self.volume_to:
                new_volume = self.volume_to
                self.stop_fade()

        # set volume.
        self.channel.set_volume(new_volume)
        self.last_volume = new_volume

        #print "new volume:%s" % new_volume
