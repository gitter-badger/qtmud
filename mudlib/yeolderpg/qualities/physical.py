import types


import qtmud


def apply(thing):
    thing.location = None
    if hasattr(thing, 'commands'):
        thing.commands['whereami'] = types.MethodType(whereami_cmd, thing)
    return thing


def move(thing, destination):
    if thing.location:
        thing.location.remove(thing)
    thing.location = destination
    thing.location.add(thing)
    return True
qtmud.subscriptions.add(move)


def whereami_cmd(waldo, line):
    if waldo.location is not None:
        output = 'You\'re location is: {}'.format(waldo.location.name)
    else:
        output = 'Your location is None.'
    qtmud.schedule('send',
                   recipient=waldo,
                   text=output)
    return True
