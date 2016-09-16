""" Gives the ability to use swords

    .. moduleauthor:: emsenn <morgan.sennhauser@gmail.com>

    .. versionadded:: 0.0.3-feature/learning
"""


import types


class Violent(object):
    """ Adds swordsmanship quality to the thing it's appleid to

        .. versionadded:: 0.0.3-feature/learning
    """

    def __init__(self):
        """
            .. versionadded:: 0.0.3-feature/learning
        """
        return

    def fight(self, stabber, line):
        """ fight the subject of line

            .. versionadded:: 0.0.3-feature/learning
        """
        stabber.manager.schedule('send',thing=stabber,
                                 scene='You can\'t actually fight things.')
        return True

    def apply(self, thing):
        """
            .. versionadded:: 0.0.3-feature/learning
        """
        if not hasattr(thing, 'fight'):
            thing.fight = types.MethodType(self.fight, thing)
        if hasattr(thing, 'commands'):
            thing.commands['fight'] = types.MethodType(self.fight, thing)
        return thing