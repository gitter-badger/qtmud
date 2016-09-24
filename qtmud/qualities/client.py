""" Methods for Clients

    .. versionadded:: 0.0.4

    Methods for Clients, expecting to be added to a :class:`thing <qtmud.Thing>`
"""
# TODO help command that prints docstring for command method

import types


import qtmud
from qtmud.services import mudsocket


def build_finger(fingeree):
    """
        Parameters:
            fingeree(object):       The Thing being fingered.
        Returns:
            str:                    The finger information of `fingeree`
    """
    finger = '- who is {}-'.format(fingeree.identity)
    for attribute in ['identity', 'name', 'nouns', 'addr']:
        if hasattr(fingeree, attribute):
            finger += ('\n{}:      {}'.format(attribute,
                                              getattr(fingeree, attribute)))
    finger += '\n'
    return finger


def commands_cmd(commander, line):
    """
        Parameters:
            commander(object):          thing with commands
            line(str):                  input from commander's client,
                                        unused here.
        Return:
            bool:                       True

        Schedules the send()ing of commander's commands to commander.
    """
    qtmud.schedule('send',
                   recipient=commander,
                   text='{}'.format(commander.commands.keys()))
    return True


def finger_cmd(fingerer, line):
    """
        Parameters:
            fingerer(object):       thing fingering another client.
            line(str):              client input, expected to be the name of
                                    a client
        Returns:
            bool:                   True

        Builds a finger of the client mentioned in `line`, and schedules its
        send()ing.
    """
    finger = str()
    line = line.split(' ')
    if len(line) == 2:
        if line[1] in ['me', 'self']:
            finger = build_finger(fingerer)
        else:
            for socket in mudsocket.clients:
                print(mudsocket.clients[socket].name)
                client = mudsocket.clients[socket]
                if line[1] == client.name.lower():
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
    """
        Parameters:
            thing(object):          client to which text will be send
            text(str):              text which will be sent to client.
        Return:
            bool:                   True

        Adds text to the thing's send_buffer - if the thing is connected
        through the socket server, this will get pushed to them and reset every
        tick.
    """
    thing.send_buffer += text + '\n'
    return True


def apply(thing):
    """
        Parameters:
            thing(object):          thing being turned into a client
        Returns:
            object:                 thing now that it is a client

        A client has an addr, send_buffer, and recv_buffer. A client also has
        commands, and is given the commands, echo, and finger commands. The
        client is also given a send() method.
    """
    client = thing
    client.addr = tuple()
    client.send_buffer = str()
    client.recv_buffer = str()
    client.commands = {'commands': types.MethodType(commands_cmd, client),
                       'echo': types.MethodType(send, client),
                       'finger': types.MethodType(finger_cmd, client)}
    client.send = types.MethodType(send, client)
    return client
