""" STARHOPPER

    .. versionadded:: 0.0.4

    Starhopper is the first MUD library (mudlib) produced using qtmud.

    In Starhopper, new players awake as starship captains, part of a scattered
    fleet fleeing from their homeland to a new world.

    As you get closer to New Earth, the challenges you will lead your crew
    through get harder.
"""


import pickle
from inspect import getmembers, isfunction


import qtmud
from mudlib.starhopper import builders, subscriptions, txt


NAME = "STARHOPPER"
SPLASH = txt.SPLASH
START_SYSTEM = None
END_SYSTEM = None
accounts = {}
players = []




def start():
    global accounts
    global START_SYSTEM
    global END_SYSTEM
    qtmud.subscribers.update({s[1].__name__: [s[1]] for s
                              in getmembers(subscriptions) if isfunction(s[1])})
    try:
        accounts = pickle.load(open("./data/starhopper_accounts.p", 'rb'))
    except FileNotFoundError:
        qtmud.log.debug('no save file found')
        qtmud.schedule('save')
    qtmud.log.info('starhopper start()ed')
    START_SYSTEM = builders.build_system()
    qtmud.log.info('starhopper.START_SYSTEM is %s', START_SYSTEM.name)
    END_SYSTEM = builders.generate_system_name()
    qtmud.log.info('starhopper.END_SYSTEM is going to be %s', END_SYSTEM)