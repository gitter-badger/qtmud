import types


import qtmud
from qtmud.services import parser


def listen_cmd(listener, line):
    listener = listener
    line = parser.parse_line(line)
    qtmud.schedule('send',
                   recipient=listener,
                   text='You\'re actually deaf.')
    return True


def apply(thing):
    listener = thing
    listener.listen = True
    if hasattr(listener, 'commands'):
        listener.commands['listen'] = types.MethodType(listen_cmd, listener)
    return listener
