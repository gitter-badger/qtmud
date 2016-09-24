import qtmud
from mudlib.yeolderpg.services import noisemaker
from mudlib.yeolderpg.places import moleinthewall
from mudlib.yeolderpg.qualities import player


START_LOCATION = moleinthewall.bar
startup_services = [noisemaker]


def add_client(client):
    hero = client
    hero = player.apply(hero)
    qtmud.schedule('move',
                   thing=hero,
                   destination=START_LOCATION)
    return player

def remove_client(client):
    hero = client
    if hero.location:
        hero.location.remove(hero)
        hero.location = None
    return True