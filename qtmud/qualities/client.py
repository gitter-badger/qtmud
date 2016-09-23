import types

import qtmud
from qtmud.services import mudsocket


def build_finger(fingeree):
    finger = '- who is {}-'.format(fingeree.identity)
    for attribute in ['identity', 'name', 'nouns', 'addr']:
        if hasattr(fingeree, attribute):
            finger += ('\n{}:      {}'.format(attribute,
                                              getattr(fingeree, attribute)))
    finger += '\n'
    return finger


def commands_cmd(commander, line):
    qtmud.schedule('send',
                   recipient=commander,
                   text='{}'.format(commander.commands.keys()))
    return True


def finger_cmd(fingerer, line):
    finger = str()
    line = line.split(' ')
    if len(line) == 2:
        if line[1] in ['me', 'self']:
            finger = build_finger(fingerer)
        else:
            for socket in mudsocket.clients:
                client = mudsocket.clients[socket]
                if line[1] in client.nouns or line[1] == client.name.lower():
                    finger = build_finger(client)
                    break
        if not finger:
            finger = 'No such thing'
    else:
        finger = 'syntax: finger <thing>'
    qtmud.schedule('send',
                   recipient=fingerer,
                   text=finger)
    return True


def send(thing, text):
    thing.send_buffer += text + '\n'
    return True


def apply(thing):
    client = thing
    client.addr = tuple()
    client.send_buffer = str()
    client.recv_buffer = str()
    client.commands = {'commands': types.MethodType(commands_cmd, client),
                       'echo': types.MethodType(send, client),
                       'finger': types.MethodType(finger_cmd, client)}
    client.send = types.MethodType(send, client)
    return client
