# TODO help command that prints docstring for command method

import types
from inspect import getmembers, isfunction

import qtmud
from qtmud import cmds


def generate_finger(fingeree):
    finger = '- who is {}-'.format(fingeree.identity)
    for attribute in ['identity', 'name', 'nouns', 'addr']:
        if hasattr(fingeree, attribute):
            finger += ('\n{}:      {}'.format(attribute,
                                              getattr(fingeree, attribute)))
    finger += '\n'
    return finger


def build_client(basis=None):
    if not basis:
        client = qtmud.new_thing()
    else:
        client = basis
    client.commands = dict()
    for command, function in [m for m in getmembers(cmds) if isfunction(m[1])]:
        client.commands[command] = types.MethodType(function, client)
    client.addr = tuple()
    client.send_buffer = str()
    client.recv_buffer = str()
    return client
