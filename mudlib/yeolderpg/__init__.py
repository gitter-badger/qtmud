import random


import qtmud
from mudlib.yeolderpg.services import noisemaker
from mudlib.yeolderpg.places import moleinthewall
from mudlib.yeolderpg.qualities import player


START_LOCATION = moleinthewall.bar
startup_services = [noisemaker]


def handle_client(client):
    hero = client
    hero = player.apply(hero)
    qtmud.schedule('move',
                   thing=hero,
                   destination=START_LOCATION)
    return player


