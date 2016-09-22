""" Give a thing the ability to speak

    .. moduleauthor:: emsenn <morgan.sennhauser@gmail.com>

    .. versionadded:: 0.0.2-features/parser
        was a part of qtmud.qualities
    .. versionadded:: 0.0.2
"""


import types


class Speaking(object):
    """ Gives a thing the ability to ``say`` things.

        .. versionadded:: 0.0.2-feature/parser
        .. versionchanged:: 0.0.2-feature/renderer
            Updated to use manager.schedule('render') instead of client.send()
    """
    def __init__(self):
        """
            .. versionadded:: 0.0.2-feature/parser
        """
        return

    def say(self, speaker, line):
        """ schedules the rendering of data for every Client in thing's location

            .. versionadded::0.0.2-feature/parser
            .. versionchanged::0.0.2-feature/renderer
                Changed to use the manager's scheduler.
            .. versionchanged:: 0.0.2-feature/textblob
                updated to work with new Send service.
            .. versionchanged:: 0.0.3-feature/diceroller
                fixed formatting error.
        """
        if not hasattr(speaker, 'location'):
            speaker.manager.schedule('send',
                                   thing=speaker,
                                   scene='You cannot speak, for you have'
                                         'no location.')
        message = ' '.join(line.split(' ')[1:])
        if hasattr(speaker, 'name'):
            scene = '\n{0} says: {1}'.format(speaker.name, message)
        else:
            scene = '\nA voice says: {0}'.format(message)
        for recipient in speaker.location.contents:
            if hasattr(recipient, 'send'):
                recipient.manager.schedule('send', thing=recipient, scene=scene)


    def apply(self, thing):
        """
            .. versionadded:: 0.0.2-feature/parser
        """
        if not hasattr(thing, 'say'):
            types.MethodType(self.say, thing)
        if hasattr(thing, 'commands'):
            thing.commands['say'] = types.MethodType(self.say, thing)
        return thing
