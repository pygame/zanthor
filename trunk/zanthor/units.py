""" For storing the units information.  All in one file for ease of tweaking.
"""

from const import *
import items


import cyclic_list



upgrade_amounts = {}
u= upgrade_amounts
cl = cyclic_list.cyclic_list

u['UpEngine Efficiency'] = cl([1.0, 2.0, 2.0, 2.0, 2.0,  3.0, 3.0, 3.0, 3.0, 3.0,   4.0, 4.0, 4.0, 4.0, 4.0 ])
u['UpEngine Speed']      = cl([1.0, 2.0, 2.0, 2.0, 2.0,  3.0, 3.0, 3.0, 3.0, 3.0,   4.0, 4.0, 4.0, 4.0, 4.0 ])
u['UpCannon Balls']      = cl([1.0, 2.0, 2.0, 2.0, 2.0,  3.0, 3.0, 3.0, 3.0, 3.0,   4.0, 4.0, 4.0, 4.0, 4.0 ])
u['UpArmour']            = cl([1.0, 2.0, 2.0, 2.0, 2.0,  3.0, 3.0, 3.0, 3.0, 3.0,   4.0, 4.0, 4.0, 4.0, 4.0 ])
u['UpSteam Tank']        = cl([1.0, 2.0, 2.0, 2.0, 2.0,  3.0, 3.0, 3.0, 3.0, 3.0,   4.0, 4.0, 4.0, 4.0, 4.0 ])
u['UpWater Tank']        = cl([1.0, 2.0, 2.0, 2.0, 2.0,  3.0, 3.0, 3.0, 3.0, 3.0,   4.0, 4.0, 4.0, 4.0, 4.0 ])
u['UpCoal Tank']         = cl([1.0, 2.0, 2.0, 2.0, 2.0,  3.0, 3.0, 3.0, 3.0, 3.0,   4.0, 4.0, 4.0, 4.0, 4.0 ])
u['UpCannon Power']      = cl([1.0, 2.0, 2.0, 2.0, 2.0,  3.0, 3.0, 3.0, 3.0, 3.0,   4.0, 4.0, 4.0, 4.0, 4.0 ])


upgrade_words = ["UpEngine Efficiency", "UpEngine Speed", "UpCannon Balls", "UpCannon Power", "UpArmour", "UpSteam Tank", "UpWater Tank", "UpCoal Tank"]






class BaseUnit:

    def __init__(self, *args, **kwargs):

        self.stats = {"Armour":0., 
                      "Speed":20., 
                      "Weight":1., 
                      "Health":5., 
                      "Water":10., 
                      "Coal":10.,
                      "Steam": 0., 
                      "CannonPressure": 0., 
                      "MaxCannonPressure": 16., 
                      "EngineEfficiency": 1,
                      "MaxHealth":10., 
                      "MaxWater":70., 
                      "MaxCoal":70.,
                      "MaxSteam": 100., 
                      "Temperature": 0., 
                      "Damage": 1., 
                      "WeaponSteam": 1., 
                      "MoveSteam": 0.05,
                      "GenerateSteamCoal": 0.05,
                      "GenerateSteamWater": 0.05,
                      }
        self.parts = {}
        


    def pickup_item(self, item):
        """ this picks up the item passed in, and adds it to the robot.
        """


        if item.type == items.ITEM_COAL:

            if self.stats['Coal'] >= self.stats['MaxCoal']:
                return 0
            else:
                self.stats['Coal'] += item.amount
                if self.stats['Coal'] >= self.stats['MaxCoal']:
                    self.stats['Coal'] = self.stats['MaxCoal']
                return 1

        if item.type == items.ITEM_WATER:

            if self.stats['Water'] >= self.stats['MaxWater']:
                return 0
            else:
                self.stats['Water'] += item.amount
                if self.stats['Water'] >= self.stats['MaxWater']:
                    self.stats['Water'] = self.stats['MaxWater']

                return 1
            
        if item.type & items.ITEM_PART:
            self.parts[item.name] = item
            return 1

        return 0


    def hit(self, damage_amount):
        """
        """
        # we can't do negative damage.
        x = damage_amount / (self.stats['Armour']+ 1.0)
        if x > 0:
            self.stats['Health'] -= x

        if self.stats['Health'] <= 0:
            return 1
        else:
            return 0

    def try_move(self):
        return self.try_use_steam(self.stats['MoveSteam'])

    def try_fire(self):
        #print "depricated"
        return self.try_use_steam(self.stats['WeaponSteam'])
    
    def prep_fire(self):
        self.stats['CannonPressure'] = 4

    def try_do_fire(self):

        if self.stats['CannonPressure'] > self.stats['MaxCannonPressure']:
            self.stats['CannonPressure'] = self.stats['MaxCannonPressure']

        if self.stats['CannonPressure'] > self.stats['Steam']:
            self.stats['CannonPressure'] = self.stats['Steam']

        if self.stats['CannonPressure'] < MIN_CANNON_PRESSURE:
            self.stats['CannonPressure'] = MIN_CANNON_PRESSURE

        if self.try_use_steam(self.stats['CannonPressure']):
            pressure = self.stats['CannonPressure']
            self.stats['CannonPressure'] = 0
            return pressure
        else:
            self.stats['CannonPressure'] = 0
            return MIN_CANNON_PRESSURE


    def try_use_steam(self, amount):
        """ returns 1 if you can, else 0.  It uses up the steam regardless.
        """

        amount /= 2
        #print "try use steam."

        # 
        if amount > self.stats['Steam']:
            self.stats['Steam'] = 0.
            return 0
        else:
            self.stats['Steam'] -= amount
            return 1


    def loop(self):
        self.generate_steam()
        
        if self.stats['CannonPressure']:
            self.stats['CannonPressure'] += 1.2
            if self.stats['CannonPressure'] > self.stats['MaxCannonPressure']:
                self.stats['CannonPressure'] = self.stats['MaxCannonPressure']
            if self.stats['CannonPressure'] > self.stats['Steam']:
                self.stats['CannonPressure'] = self.stats['Steam']
                



    def generate_steam(self):
        """ Returns amount of steam it generates from coal & water given.
        """

        coal = self.stats["GenerateSteamCoal"]
        water = self.stats["GenerateSteamWater"]


        # not allowed negatives...
        assert(coal >= 0)
        assert(water >= 0)

        # if no coal, or no water, then you can't have steam.
        if not coal or not water:
            print "no coal, or no water passed in for generation"
            steam = 0
            return 0
        else:

            # can only use what we have.
            if water > self.stats['Water']:
                water = self.stats['Water']

            if coal > self.stats['Coal']:
                coal = self.stats['Coal']

            self.stats['Water'] -= water
            self.stats['Coal'] -= coal


            if coal == 0 or water == 0:
                steam = 0
            else:
                #calculate how much steam we use.
                # ... this is just the average of the coal and water.
                steam = coal + water
                if steam > 0:
                    steam = steam / 2
                else:
                    pass
                    #print "no coal, or no water left"

        steam = steam * self.stats["EngineEfficiency"]

        total_steam = self.stats['Steam'] + steam
        if total_steam > self.stats['MaxSteam']:
            #print "too much steam"
            self.stats['Steam'] = self.stats['MaxSteam']
        else:
            self.stats['Steam'] += steam

        return steam


    def upgrade_part(self, part_up, amount):
        """ call this to upgrade one part.
            part_up - 
                      UpEngine Efficiency
                      UpEngine Speed
                      UpCannon Balls
                      UpArmour
                      UpSteam Tank
                      UpWater Tank
                      UpCoal Tank
                      UpCannon Power
        """

        print "upgrading :%s" % part_up


        if part_up == "UpEngine Efficiency":
            self.stats['EngineEfficiency'] += amount
        if part_up == "UpEngine Speed":
            self.stats['Speed'] += amount
        if part_up == "UpCannon Balls":
            self.stats['Damage'] += amount
        if part_up == "UpArmour":
            self.stats['Armour'] += amount
        if part_up == "UpSteam Tank":
            self.stats['MaxSteam'] += amount
        if part_up == "UpWater Tank":
            self.stats['MaxWater'] += amount
        if part_up == "UpCoal Tank":
            self.stats['MaxCoal'] += amount
        if part_up == "UpCannon Power":
            self.stats['MaxCannonPressure'] += amount


class Castle(BaseUnit):
    
    def __init__(self, *args, **kwargs):
        BaseUnit.__init__(self, *args, **kwargs)

        self.name = "castle"

        self.stats = {"Armour":0., 
                      "Speed":10., 
                      "Weight":1., 
                      "Health":10., 
                      "Water":65., 
                      "Coal":65.,
                      "Steam": 100., 
                      "EngineEfficiency": 3.,

                      "CannonPressure": 0., 
                      "MaxCannonPressure": 16., 
                      "MaxHealth":10., 
                      "MaxWater":70., 
                      "MaxCoal":70.,
                      "MaxSteam": 100., 
                      "Temperature": 0., 
                      "Damage": 1., 
                      "WeaponSteam": 1., 
                      "MoveSteam": 0.05,
                      "GenerateSteamCoal": 0.05,
                      "GenerateSteamWater": 0.05,

                      "UpEngine Speed":0,
                      "UpEngine Efficiency":0,
                      "UpCannon Balls":0,
                      "UpCannon Power":0,
                      "UpArmour":0,
                      "UpSteam Tank":0,
                      "UpWater Tank":0,
                      "UpCoal Tank":0,
                      "upgrade_amounts": upgrade_amounts,
                      }


class Robot(BaseUnit):
    

    def __init__(self, *args, **kwargs):
        BaseUnit.__init__(self, *args, **kwargs)
        self.name = "baddie_robot"

        self.stats = {"Armour":0., 
                      "Speed":20., 
                      "Weight":1., 
                      "Health":5., 
                      "Water":10., 
                      "Coal":10.,
                      "EngineEfficiency": 1,
                      "Steam": 100., 
                      "CannonPressure": 0., 
                      "MaxCannonPressure": 16., 
                      "MaxHealth":70., 
                      "MaxWater":70., 
                      "MaxCoal":70.,
                      "MaxSteam": 70., 
                      "Temperature": 0., 
                      "Damage": 1., 
                      "WeaponSteam": 1., 
                      "MoveSteam": 0.05,
                      "GenerateSteamCoal": 0.05,
                      "GenerateSteamWater": 0.05,
                      }


class CannonTower(BaseUnit):
    

    def __init__(self, *args, **kwargs):
        BaseUnit.__init__(self, *args, **kwargs)

        self.name = "cannon_tower"

        self.stats = {"Armour":0., 
                      "Speed":0., 
                      "Weight":1., 
                      "Health":3., 
                      "Water":10., 
                      "Coal":10.,
                      "Steam": 100.,
                      "MaxHealth":70., 
                      "EngineEfficiency": 1,
                      "MaxWater":70., 
                      "MaxCoal":70.,
                      "MaxSteam": 70., 
                      "CannonPressure": 0., 
                      "MaxCannonPressure": 16., 

                      "Temperature": 0.,
                      "Damage": 1.,
                      "WeaponSteam": 1.,
                      "MoveSteam": 0.05,
                      "GenerateSteamCoal": 0.05,
                      "GenerateSteamWater": 0.05,
                      }


class CoalTruck(BaseUnit):
    

    def __init__(self, *args, **kwargs):
        BaseUnit.__init__(self, *args, **kwargs)
        self.name = "coal_truck"

        self.stats = {"Armour":0., 
                      "Speed":20., 
                      "Weight":1., 
                      "Health":5., 
                      "Water":10., 
                      "Coal":10.,
                      "Steam": 100., 
                      "EngineEfficiency": 1,
                      "MaxHealth":70., 
                      "MaxWater":70., 
                      "MaxCoal":70.,
                      "MaxSteam": 70., 
                      "CannonPressure": 0., 
                      "MaxCannonPressure": 16., 

                      "Temperature": 0., 
                      "Damage": 1., 
                      "WeaponSteam": 1., 
                      "MoveSteam": 0.05,
                      "GenerateSteamCoal": 0.05,
                      "GenerateSteamWater": 0.05,
                      }


class Factory(BaseUnit):

    def __init__(self, *args, **kwargs):
        BaseUnit.__init__(self, *args, **kwargs)
        self.name = "factory"

        self.stats = {"Armour":0., 
                      "Speed":20., 
                      "Weight":1., 
                      "Health":5., 
                      "Water":10., 
                      "EngineEfficiency": 1,
                      "Coal":10.,
                      "Steam": 100., 
                      "MaxHealth":70., 
                      "MaxWater":70., 
                      "MaxCoal":70.,
                      "MaxSteam": 70., 
                      "CannonPressure": 0., 
                      "MaxCannonPressure": 16., 

                      "Temperature": 0., 
                      "Damage": 1., 
                      "WeaponSteam": 1., 
                      "MoveSteam": 0.05,
                      "GenerateSteamCoal": 0.05,
                      "GenerateSteamWater": 0.05,
                      }






