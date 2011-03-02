"""
here you can define which sounds are played.

Each list defines a list of sounds which can be played when that event happens.

They get played in random order, or in cyclic order.
"""

import cyclic_list

cl = cyclic_list.cyclic_list

cannon = cl(["cannon", "cannon2", "cannon3", "cannon", "cannon"])

hitenemy = cl(["hitenemy"])

hitwall = cl(["hitwall2"])

hitground = cl(["hitground"])

destroyenemy = cl(["destroyenemy"])

# um...  us hit. ;)
ushit = cl(["ouch1", "ouch2"])

coal = cl(["coal"])
water = cl(["water"])


def get_upgrade_sound(upgrade_what):
    return "upgrade"

#TODO: need to put in the release sound, and engine noises.
release = cl(["release"])

engine_slow = cl(["engine-slow"])
engine_fast = cl(["engine-fast"])


birds = cl(["birds1", "birds2", "birds2"])

peasants = cl(["peasants1", "peasants2", "peasants3"])

squish = cl(["squish1", "squish2"])

ouch2 = cl(["ouch2"])
ouch1 = cl(["ouch1"])


