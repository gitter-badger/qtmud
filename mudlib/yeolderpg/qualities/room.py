from mudlib.yeolderpg.qualities import container, noisy, renderable


def apply(thing):
    room = thing
    room = container.apply(room)
    room = renderable.apply(room)
    room = noisy.apply(room)
    room.exits = dict()
    return room
