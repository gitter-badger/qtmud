""" Give a thing the ability to speak

    .. moduleauthor:: emsenn <morgan.sennhauser@gmail.com>

    .. versionadded:: 0.0.1-features/parser
        was a part of qtmud.qualities
"""


import types


from qtmud.qualities.client import Client
from qtmud.qualities.renderable import Renderable


class Speaking(object):
    """ Gives a thing the ability to ``say`` things.

        .. versionadded:: 0.0.1-features/parser
        .. versionchanged:: 0.0.2-features/renderer
            Updated to use manager.schedule('render') instead of client.send()
    """
    def __init__(self):
        """
            .. versionadded:: 0.0.1-features/parser
        """
        return

    #pylint: disable=no-self-use
    def say(self, thing, data):
        """ schedules the rendering of data for every Client in thing's location

            .. versionadded::0.0.1-features/parser
            .. versionchanged::0.0.1-features/renderer
                Changed to use the manager's scheduler.
        """
        if not hasattr(thing, 'location'):
            thing.manager.schedule('render',
                                   client=thing,
                                   scene='You cannot speak, for you have'
                                         'no location.')
        for recipient in thing.location.contents:
            if recipient in thing.manager.qualities[Client]:
                if Renderable in thing.qualities:
                    thing.manager.schedule('render',
                                           client=recipient,
                                           scene='{0} says: {1}'
                                                 ''.format(thing.name,
                                                           data))
                else:
                    thing.manager.schedule('render',
                                           client=recipient,
                                           scene='A voice says: '
                                                 '{0}'.format(data))
    #pylint: enable=no-self-use

    def apply(self, thing):
        """
            .. versionadded:: 0.0.1-features/parser
        """
        if not hasattr(thing, 'say'):
            types.MethodType(self.say, thing)
        if hasattr(thing, 'commands'):
            thing.commands['say'] = types.MethodType(self.say, thing)
        return thing
