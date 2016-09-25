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
""" the name of the mudlib """

SPLASH = txt.SPLASH
""" text shown to incoming players"""
START_SYSTEM = builders.build_system()
""" the system new connections start in """

try:
    player_accounts = pickle.load(open("./data/starhopper_accounts.p", 'rb'))
except FileNotFoundError:
    qtmud.log.debug('no save file found')
    player_accounts = {}
    qtmud.schedule('save')
""" testing docs """
players = []
""" currently logged in players """
qtmud.subscribers.update({s[1].__name__ : [s[1]] for s
                          in getmembers(subscriptions) if isfunction(s[1])})

def save():
    """ save stats for accounts """
    pickle.dump(player_accounts, open("./data/starhopper_accounts.p", 'wb'))
    qtmud.log.debug('saving starhopper player_accounts')
    return True
