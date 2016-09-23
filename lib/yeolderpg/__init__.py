import random


import qtmud
from qtmud.services import mover
from lib.yeolderpg.places import moleinthewall


back_room = moleinthewall.bar


def death(departed):
    if hasattr(departed, 'location'):
        body = corpse.apply(qtmud.new_thing())
        qtmud.schedule('move',
                       thing=body,
                       destination=departed.location)


def roll(roller, dice_pool):
    result = 0
    for dice in range(dice_pool):
        result += random.choice([-1, 0, 0, 0, 1, 1])
    qtmud.log.debug('{} rolled a {} using {} dice'.format(roller.name,
                                                          result,
                                                          dice_pool))
    return result