import types

import qtmud
from mudlib.yeolderpg.qualities import hearing, learning, physical, \
    renderable, sighted, speaking


def move_cmd(mover, line):
    line = ' '.join(line.split(' ')[1:])
    if line in mover.location.exits:
        destination = mover.location.exits[line]
        qtmud.schedule('move',
                       thing=mover,
                       destination=destination)
    return True


def apply(thing):
    player = thing
    player = hearing.apply(learning.apply(physical.apply(player)))
    player = sighted.apply(speaking.apply(renderable.apply(player)))
    player.commands['move'] = types.MethodType(move_cmd, player)
    return player
