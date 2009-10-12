import isovid
from units import Factory


def factory_new(g,t,value):
    print 'factory',g.clayer[t.ty][t.tx],t.rect
    
    
    
    g.clayer[t.ty][t.tx] = 0
    g.blayer[t.ty][t.tx] = 0x14
    g.blayer[t.ty-1][t.tx] = 0x14
    g.blayer[t.ty][t.tx-1] = 0x14
    g.blayer[t.ty+1][t.tx] = 0x14
    g.blayer[t.ty][t.tx+1] = 0x14

    #s = isovid.Sprite(g.images['factory.3'],(0,0))
    #s.rect.centerx,s.rect.centery = t.rect.centerx,t.rect.centery/2
    s = isovid.Sprite(g.images['factory.3'],t.rect)
    g.sprites.append(s)
    print s.rect
    tx,ty = s.rect.centerx/g.iso_w,s.rect.centery/g.iso_h
    print tx,ty
    
    #NOTE: this is just to show off!
    #import steam
    #s.effect = steam.Effect(32,1)
    
    import fire
    s.effect = fire.Effect(16,1)
    
    #s.groups = g.string2groups('coal')
    #s.agroups = g.string2groups('castle')
    #s.hit = coal_hit

    #s.groups = g.string2groups('factory')
    #s.agroups =g.string2groups("castle")
    s.hit = factory_hit

    
    s.loop = factory_loop
    s.frame = 0
    s.type = 'factory'

    s.unit = Factory()
    
def factory_loop(g,s):
    s.unit.loop()

    tx,ty = s.rect.centerx/32,s.rect.centery/32#g.view_to_iso((s.rect.centerx,s.rect.centery))
    #print s.rect
    #print tx,ty
    #print g.tlayer[ty][tx]
    s.frame +=1
    
def factory_hit(g,a,b):
    pass
