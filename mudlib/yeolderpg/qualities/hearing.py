""" gives a thing hearing

    .. moduleauthor:: emsenn <morgan.sennhauser@gmail.com>

    .. versionadded:: 0.0.4
"""
import types


import qtmud
from qtmud.services import parser


def listen_cmd(listener, line):
    """ listen command

        .. versionadded:: 0.0.4

        Parameters:
            listener(object):   the object doing the listening.
            line(string):       the full text of what the player input.
        Returns:
            bool:               True if the command resolves, otherwise False.

        Use player input to listen to a thing.
    """
    listener = listener
    line = parser.parse_line(line)
    output = str()
    print(line)
    if 'objekt' in line:
        objekt = line['objekt']
    elif len(line) == 1:
        objekt = 'here'
    else:
        objekt = None
    print(objekt)
    if objekt in ['room', 'here', 'location']:
        if listener.location.sounds:
            output = '{}'.format(listener.location.sounds)
        else:
            output = 'Your location is quiet.'
    elif objekt in ['me', 'self', 'myself']:
        output = 'You aren\'t making any sounds.'
    else:
        matches = parser.search_by_line(listener, **line)
        if len(matches) == 1:
            match = matches[0]
            if hasattr(match, 'noise'):
                output = '{}'.format(listener.location.sounds)
        elif len(matches) >1:
            output = 'More than one match, try using the full name:\n'
            for match in matches:
                output += '{}'.format(match.name)
        elif len(matches) == 0:
            output = 'Can\'t find that.'
    if output:
        qtmud.schedule('send',
                       recipient=listener,
                       text=output)
        return True
    else:
        qtmud.schedule('send',
                       recipient=listener,
                       text='The command failed, warning pushed to console.')
        qtmud.log.warning('listen_cmd() failed in a way i didn\'t expect!')
        return False


def apply(thing):
    listener = thing
    listener.listen = True
    if hasattr(listener, 'commands'):
        listener.commands['listen'] = types.MethodType(listen_cmd, listener)
    return listener
