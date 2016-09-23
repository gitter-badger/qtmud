import types

import qtmud
from lib.yeolderpg.qualities import speaking, sighted, learning


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
    player = speaking.apply(sighted.apply(learning.apply(player)))
    player.commands['move'] = types.MethodType(move_cmd, player)
    return player