""" Gives the ability to see to a thing.

    .. moduleauthor:: emsenn <morgan.sennhauser@gmail.com>

    .. versionadded:: 0.0.2-feature/textblob
"""


import types
from qtmud.services import Parser


class Prehensile(object):
    """
        .. versionadded:: 0.0.2-feature/textblob
    """

    def __init__(self):
        """
            .. versionadded:: 0.0.2-feature/textblob
        """
        return

    def take(self, taker, line):
        """
            .. versionadded:: 0.0.2-feature/textblob
        """
        line = Parser.parse_line(taker, line)
        matches = taker.search(**line)
        if len(matches) == 1:
            subject = matches[0]
            taker.manager.schedule('move',thing=subject,destination=taker)
            scene = 'You pick it up.'
        elif len(matches) >1:
            scene = 'More than one match, try using the full name:\n'
            for match in matches:
                if hasattr(match, 'name'):
                    scene += '{}\n'.format(match.name)
        else:
            scene = 'Cannot find that.'
        taker.manager.schedule('send', thing=taker, scene=scene)
        return True

    def apply(self, thing):
        """
            .. versionadded:: 0.0.2-feature/textblob
        """
        if not hasattr(thing, 'take'):
            thing.take = types.MethodType(self.take, thing)
        if hasattr(thing, 'commands'):
            thing.commands['take'] = types.MethodType(self.take, thing)
        return thing
