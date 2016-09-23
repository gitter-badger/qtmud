import types


import qtmud


def apply(thing):
    thing.location = None
    if hasattr(thing, 'commands'):
        thing.commands['whereami'] = types.MethodType(whereami_cmd, thing)
    return thing


def whereami_cmd(waldo, line):
    if waldo.location is not None:
        output = 'You\'re location is: {}'.format(waldo.location.name)
    else:
        output = 'Your location is None.'
    qtmud.schedule('send',
                   recipient=waldo,
                   text=output)
    return True
