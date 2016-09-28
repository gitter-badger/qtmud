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


def build_client(thing=None):
    #####
    #
    # make a client thing
    #
    #####
    if not thing:
        client = qtmud.new_thing()
    else:
        client = thing
    qtmud.connected_clients.append(client)
    #####
    #
    # add commands to the client
    #
    #####
    client.commands = dict()
    for command, function in [m for m in getmembers(cmds) if isfunction(m[1])]:
        client.commands[command] = types.MethodType(function, client)
    #####
    #
    # add aliases
    #
    #####
    client.input_parser = 'client_command_parser'
    #####
    #
    # address, send_buffer, recv_buffer
    #
    #####
    client.addr = tuple()
    client.send_buffer = str()
    client.recv_buffer = str()
    client.channels = list()
    return client
