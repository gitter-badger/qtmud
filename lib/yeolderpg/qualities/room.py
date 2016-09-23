from qtmud.qualities import container, renderable, noisy

def apply(thing):
    room = thing
    room = container.apply(room)
    room = renderable.apply(room)
    room = noisy.apply(room)
    room.exits = dict()
    return room
