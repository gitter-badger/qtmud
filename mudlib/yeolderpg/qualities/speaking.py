import types


import qtmud


def say_cmd(speaker, line):
    message = ' '.join(line.split(' ')[1:])
    output = '\n{0} says: {1}'.format(speaker.name, message)
    for recipient in speaker.location.contents:
        if hasattr(recipient, 'send'):
            qtmud.schedule('send', recipient=recipient, text=output)


def apply(thing):
    if hasattr(thing, 'commands'):
        thing.commands['say'] = types.MethodType(say_cmd, thing)
    return thing
