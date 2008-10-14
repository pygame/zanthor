
#i will take over the world
#zanthor shall rule the universe
#my powers can not be stopped
#my strength has no bounds
#die worthless scum
#My name is Zanthor.  I like flowers, and killing.
#fear me weak humans
#When Zanthor was little(that's me) I always wanted to grow up and be a junkie or a telemarketer.  Unfortunately it didn't turn out that way, and instead I have become a dark overlord.


data = {
    'SENTENCE':[
        '[_SENTENCE]',
        ],
    '_SENTENCE':[
        '[NAME] [WILL] [KILL] [HUMANS].',
        '[FEAR] [NAME].',
        '[HUMANS], [FEAR] [NAME].',
        '[FEAR] [NAME], [HUMANS].',
        '[NAME] [WILL] [KILL] and [KILL] [HUMANS].',
        
        '[ITEMS] [KILL] [ITEMS] [KILL].',
        
        '[NAME] [LIKES] [ITEMS].',
        'My name is [NAME].  I [LIKE] [ITEMS].',
        'My name is [NAME].  I [LIKE] [ITEMS] and [KILLING].',
        
        'I have become [NAME].',
        'I once was [WEAK].  I am now [NAME].',
        'I am [NAME].',
        'I am [NAME].  Hear me [KILL].',
        'I [KILL] [HUMANS].',
        
        '[HUMANS] will become my [SLAVES].',
        ],
        
    'NAME':[
        '[_NAME]',
        '[_NAME] the [GREAT]',
        '[_NAME] the [VERY] [GREAT]',
        '[_NAME], [KING] of [HUMANS]',
        ],
    '_NAME':[
        'Zanthor','Lord Zanthor','Evil Lord Zanthor',
        ],
    'VERY':[
        'very','exceedingly','abundantly','amazingly',
        'indisputably','amazingly','awesomely',
        'shatteringly','freighteningly','consumingly',
        ],
    'GREAT':[
        'awesome','great','all-mightly','powerful',
        'magnificent','regal','rotund','wise',
        'magestic','stately','exalted',
        ],
    'KING':[
        'king','ruler','master','owner','magistrate',
        'conqueror','captain','dictator','president',
        'potentate','overlord',
        ],
        
        
    'HUMANS':[
        '[_HUMANS]','[WEAK] [_HUMANS]','[WEAK] and [WEAK] [_HUMANS]',
        ],
    'WEAK':[
        'weak','pathetic','feable','ill-bred',
        'sorry','unworthy','poor','unfortunate',
        'sad','lost','ugly','disgusting','hideous',
        'sorry','unwelcome','measly',
        ],
    '_HUMANS':[
        'humans','people','sheep','masses','scum',
        'earthlings','citizens','fools',
        ],
        
    
    'WILL':[
        'will','plans to','aims to','must','shall','can easily',
        'will always',
        ],
        
    'LIKES':[
        'likes','loves','covets','collects','eats',
        'hordes',
        ],
    'LIKE':[
        'like','love','covet','collect','eat',
        'horde',
        ],
        
    'FEAR':[
        'fear','loath','tremble before','shy away from',
        'hide from','run from','faint near',
        ],
        
    'KILL':[
        'kill','maim','batter','harm','hurt','maltreat','mangle',
        'wound','maul','ruin','smite','break','punish',
        'blow-up','blast','ransack','destroy',
        ],
        
    'KILLING':[
        'killing','maiming','battering','harming','hurting','maltreating','mangling',
        'wounding','mauling','ruining','smiting','breaking','punishing',
        'blowing-up','blasting','ransacking','destroying'
        ],
        
        
    'SLAVES':[
        'slaves','underlings','footstool','minions','onions','breakfast',
        'flower pot mulch','belly button lint','toe jam',
        ],

        
    'ITEMS':[
        '[_ITEMS]','[_ITEMS]','[_ITEMS] and [_ITEMS]',
        ],
        
    '_ITEMS':[
        'coal','water','cannons','power','steam',
        'destruction','blasts','flowers',
        'explosions','fire','desolation',
        ],
        
     }

import random
import re

def replace(v):
    return random.choice(data[v.group(1)])
def ureplace(v):
    return v.group(0).upper()

def generate():
    text = random.choice(data['SENTENCE'])
    regex = re.compile('\[(\w+)\]')
    while '[' in text:
        text = re.sub(regex,replace,text,1)
    regex = re.compile('[\.\!\?]\s+\w')
    text = re.sub(regex,ureplace,text)
    return text[0:1].upper()+text[1:]
        
def generate_upgrade_message(upgrade_what):
    
    return "Zanthor upgrades the %s on his castle." % (upgrade_what.replace("Up",""))

def generate_win_level():
    return generate()


    
if __name__ == '__main__':
    for n in xrange(0,12):
        print generate()
        print ''

