from qtmud.qualities import physical, container


def apply(thing):
    departed = thing
    departed = physical.apply(departed)
    departed = container.apply(departed)
    return departed
