""" STARHOPPER

    .. versionadded:: 0.0.4

    Starhopper is the first MUD library (mudlib) produced using qtmud. A simple
    action adventure game, Starhopper works best when played as a session-based
    game with a few friends.

    Attributes:
        START_LOCATION(object):     first system, where new players start.
        startup_services(None):     required by qtmud
"""


import qtmud
from mudlib.starhopper import builders, subscriptions, txt

SPLASH=txt.SPLASH
START_LOCATION = builders.build_system()
qtmud.subscriptions.update([subscriptions.alert, subscriptions.attack,
                            subscriptions.death, subscriptions.hop,
                            subscriptions.salvage, subscriptions.scan_planet,
                            subscriptions.scan_ship, subscriptions.scan_star,
                            subscriptions.scan_system,
                            subscriptions.scan_wreck, subscriptions.upgrade])
players = []






def add_client(client):
    """ turn a client into a starship """
    qtmud.log.debug('%s is entering STARHOPPER', client.name)
    player = client
    player = builders.build_ship(player)
    players.append(player)
    qtmud.schedule('hop',
                   ship=player,
                   destination=START_LOCATION)
    return player


def remove_client(client):
    if hasattr(client, 'local_system'):
        client.local_system.ships.remove(client)
    return True
