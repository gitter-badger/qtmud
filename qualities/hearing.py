""" Gives the ability to listen to (hear) things.

    .. moduleauthor:: emsenn <morgan.sennhauser@gmail.com>

    .. versionadded:: 0.0.2-feature/textblob

    Adds hearing to a thing, which gives it the ability to ``listen`` to
    things around it.
"""


import types
from qtmud.services import Parser


class Hearing(object):
    """ Adds hearing to a thing it is applied to.

        .. versionadded:: 0.0.2-feature/textblob

        When :func:`applied <qtmud.qualities.Quality.apply>` by the
        :class:`manager <qtmud.Manager>`, gives a :class:`thing
        <qtmud.Thing>` the ability to hear. In practice, this means giving
        the thing the :func:`listen <qtmud.qualities.hearing.Hearing.listen>`
        method, and, if the thing is Commandable, give sit the ``listen`` command.
    """

    def __init__(self):
        """
            .. versionadded:: 0.0.2-feature/textblob
        """
        return

    def listen(self, listener, line):
        """ Render sounds of the subject in line from listener's perspective.

            .. versionadded:: 0.0.2-feature/textblob

            Parameters:
                listener(object):   The class:`thing <qtmud.Thing>` that
                                    is doing the listening. Output will be
                                    written from this thing's perspective.
                line(str):          A string representing a nametag of an
                                    object in ``thing``'s environment.

            Returns:
                bool:             True if the listening was successful.
        """
        listener = listener
        line = Parser.parse_line(listener, line)
        if 'subject' in line:
            subject = line['subject']
        elif len(line) == 1:
            subject = 'here'
        else:
            subject = None
        if subject in ['room', 'here', 'location']:
            if hasattr(listener, 'location') and listener.location is not None:
                if hasattr(listener.location, 'name') and \
                hasattr(listener.location, 'sounds'):
                    scene = ('- {} -\n{}\n'.format(listener.location.name,
                                                   listener.location.sounds))
                else:
                    scene = ('It is quiet.')
        elif subject in ['me', 'self', 'myself']:
            scene = ('You aren\'t making any sounds. Try "say"ing something.')
        else:
            matches = listener.search(**line)
            if len(matches) == 1:
                match = matches[0]
                if hasattr(match, 'name') and hasattr(match, 'sounds'):
                    scene = ('- {} -\n{}\n'.format(match.name, match.sounds))
                else:
                    scene = ('That isn\'t making any sound.')
            elif len(matches) > 1:
                scene = ('More than one match, try using the full name of '
                         'what you want:\n')
                for match in matches:
                        if hasattr(match, 'name'):
                            scene += ('{}\n'.format(match.name))
            else:
                scene = ('whatever you tried to listen to, you can\'t.')
        listener.manager.schedule('send', thing=listener, scene=scene)
        return True

    def apply(self, thing):
        """
            .. versionadded:: 0.0.2-feature/textblob

            Parameters:
                thing(object):      The :class:`thing <qtmud.Thing>` that will
                                    be given the Hearing quality.
        """
        if not hasattr(thing, 'listen'):
            thing.listen = types.MethodType(self.listen, thing)
        if hasattr(thing, 'commands'):
            thing.commands['listen'] = types.MethodType(self.listen, thing)
        return thing
