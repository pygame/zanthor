import isovid
#import pygame

#set f < 1 for infinite
def effect_new(g,rect,e,f):
    s = isovid.Sprite(g.images['blank'],rect)
    s.effect = e
    
    s.frames = f
    g.sprites.append(s)
    
    s.loop = effect_loop
    
    return s
    
def effect_loop(g,s):
    s.frames -= 1
    if s.frames == 0:
        g.sprites.remove(s)
    

    