import random


import qtmud
from mudlib.yeolderpg.qualities import corpse


def death(departed):
    if hasattr(departed, 'location'):
        body = corpse.apply(qtmud.new_thing())
        qtmud.schedule('move',
                       thing=body,
                       destination=departed.location)
    return True


def roll(roller, dice_pool):
    result = 0
    for dice in range(dice_pool):
        result += random.choice([-1, 0, 0, 0, 1, 1])
    qtmud.log.debug('{} rolled a {} using {} dice'.format(roller.name,
                                                          result,
                                                          dice_pool))
    return result
