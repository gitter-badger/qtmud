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

    def drop(self, dropper, line):
        """
            .. versionadded:: 0.0.3-feature/noise
        """
        line = line.split(' ')[1:]
        if hasattr(dropper, 'contents'):
            for content in dropper.contents:
                if line[-1] in content.nametags:
                    if len(line) > 1:
                        adjectives = line[0:-1]
                        for adjective in adjectives:
                            if adjective in content.adjectives:
                                pass
                            else:
                                dropper.manager.schedule('send',thing=dropper,
                                                         scene='You don\'t '
                                                               'have anything '
                                                               'with that '
                                                               'name.')
                                return False
                    dropper.manager.schedule('move',thing=content,
                                             destination=dropper.location)
                    dropper.manager.schedule('send', thing=dropper,
                                             scene='You drop it.')




    def take(self, taker, line):
        """
            .. versionadded:: 0.0.2-feature/textblob
        """
        line = Parser.parse_line(taker, line)
        matches = taker.search_by_line(**line)
        if len(matches) == 1:
            subject = matches[0]
            taker.manager.schedule('move',thing=subject,destination=taker)
            scene = 'You pick {} up.'.format(subject.name)
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
        if not hasattr(thing, 'drop'):
            thing.drop = types.MethodType(self.drop, thing)
        if hasattr(thing, 'commands'):
            thing.commands['take'] = types.MethodType(self.take, thing)
            thing.commands['drop'] = types.MethodType(self.drop, thing)
        return thing
