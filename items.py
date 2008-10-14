
ITEM_COAL            = 0x0001
ITEM_WATER           = 0x0002
ITEM_PART            = 0x0010
ITEM_CANNON          = 0x0020
ITEM_ENGINE          = 0x0030
ITEM_WATERTANK       = 0x0040
ITEM_COALSTORAGEROOM = 0x0050
ITEM_ARMOUR          = 0x0060
ITEM_RUBBLE          = 0x0100
ITEM_ = 10
ITEM_ = 11
ITEM_ = 12
ITEM_ = 13
ITEM_ = 14
ITEM_ = 15
ITEM_ = 16

class Coal:
    type = ITEM_COAL

    def __init__(self, amount = 1.0):
        self.amount = amount
        self.name = "Coal"
        self.pickup_string = "Pick up some Coal?"

class Water:
    type = ITEM_WATER

    def __init__(self, amount = 1.0):
        self.amount = amount
        self.name = "Water"
        self.pickup_string = "Suck up some water?"

class Rubble:
    type = ITEM_RUBBLE

    def __init__(self):
        self.name = "Rubble"
        self.pickup_string = "Pick up some rubble?"





class Cannon:
    type = ITEM_CANNON

    def __init__(self):
        self.name = "cannon"
        self.pickup_string = "Pick up a Cannon?"



class Part:
    type = ITEM_PART

    def __init__(self, name, pickup_string):
        self.name = name
        self.pickup_string = pickup_string


class Engine:
    type = ITEM_ENGINE

    def __init__(self):
        self.name = "engine"
        self.pickup_string = "Pick up an engine?"

class WaterTank:
    type = ITEM_WATERTANK

    def __init__(self):
        self.name = "water tank"
        self.pickup_string = "Pick up a water tank?"

class CoalStorageRoom:
    type = ITEM_COALSTORAGEROOM

    def __init__(self):
        self.name = "coal storage room"
        self.pickup_string = "Pick up a coal storage room?"

class Armour:
    type = ITEM_ARMOUR

    def __init__(self):
        self.name = "armour"
        self.pickup_string = "Pick up some armour?"





def coal_new(g,t,value):
    g.clayer[t.ty][t.tx] = 0
    s = isovid.Sprite(g.images['coal'],t.rect)
    s.frame = 0

    s.item = items.Coal(1.)

    g.sprites.append(s)
    s.loop = coal_loop

    s.groups = g.string2groups('coal')
    s.agroups = g.string2groups('castle')
    s.hit = coal_hit
    
    import fire
    #s.effect = fire.Effect(64,1)


def coal_hit(g,s,a):
    #print "coal hit"
    pass



def coal_loop(g,s):
    pass
    #s.rect.clamp_ip(g.view)
    s.frame +=1
    




def cannon_tower_new(g,t,value):
    g.clayer[t.ty][t.tx] = 0
    s = isovid.Sprite(g.images['cannon_tower'],t.rect)

    s.item = items.Coal(1.)

    g.sprites.append(s)
    s.loop = cannon_tower_loop

    #s.groups = g.string2groups('cannon_tower')
    #s.agroups = g.string2groups('castle')
    #s.hit = cannon_tower_hit


def cannon_tower_hit(g,s,a):
    pass

def cannon_tower_loop(g,s):
    pass





    
def water_new(g,t,value):
    g.clayer[t.ty][t.tx] = 0

    s = isovid.Sprite(g.images['water'],t.rect)
    g.sprites.append(s)
    #s.groups = g.string2groups('coal')
    #s.agroups = g.string2groups('castle')
    #s.hit = coal_hit

    s.frame = random.randrange(0,32)
    s.loop = water_loop
    
def water_loop(g,s):

    #if s.frame%20 == 0:
    #    import explode
    #    s.effect = explode.Effect(512,128)
    #    pass
        
    s.frame += 1





def human_new(g,t,value):
    g.clayer[t.ty][t.tx] = 0

    s = isovid.Sprite(g.images['human'],t.rect)
    g.sprites.append(s)

    s.frame = random.randrange(0,32)
    s.loop = human_loop
    

def human_loop(g,s):
    s.frame += 1



def wall_new(g,t,value):
    g.clayer[t.ty][t.tx] = 0

    s = isovid.Sprite(g.images['wall'],t.rect)
    g.sprites.append(s)

    s.frame = random.randrange(0,32)
    s.loop = wall_loop
    

def wall_loop(g,s):
    s.frame += 1




def baddie_robot_new(g,t,value):
    g.clayer[t.ty][t.tx] = 0

    s = isovid.Sprite(g.images['baddie_robot'],t.rect)
    g.sprites.append(s)

    s.frame = random.randrange(0,32)
    s.loop = baddie_robot_loop
    

def baddie_robot_loop(g,s):
    s.frame += 1



# castle
# human
# factory
# coal
# water
# cannon towers
# walls
# baddie robots. not castles, but smaller sleaker ones.




