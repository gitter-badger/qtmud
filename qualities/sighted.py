""" Gives the ability to see to a thing.

    .. moduleauthor:: emsenn <morgan.sennhauser@gmail.com>

    .. versionadded:: 0.0.2-feature/parser

    Adds sight to a quality, which for now means access to the look
    function and command.
"""


import types
from qtmud.services import Parser


class Sighted(object):
    """ Adds sight to a thing it is applied to.

        .. versionadded:: 0.0.2-feature/parser

        When :func:`applied <qtmud.qualities.Quality.apply>` by the
        :class:`manager <qtmud.Manager>`, gives a thing sight. In this
        context, that means the :func:`look
        <qtmud.qualities.sight.Sighted.look>` function, documented below.
    """

    def __init__(self):
        """
            .. versionadded:: 0.0.2-feature/parser
        """
        return

    def look(self, looker, line):
        """ Render ``target`` from the perspective of ``looker``.

            .. versionadded:: 0.0.2-feature/parser
            .. versionchanged:: 0.0.2-feature/renderer
                Made thing.look() directly callable.
            .. versionchanged:: 0.0.2-feature/neverforgetholidayupdate
                rely on checking the attributes of things directly, instead
                of using checks against Qualities
            .. versionchanged:: 0.0.2-feature/nametags
                use nametags instead of names to figure out what to look at.
            .. versionchanged:: 0.0.2-feature/adjectives
                changed to use the new Parser parse_line() function.
            .. versionchanged:: 0.0.2-feature/textblob
                shuffled things so thing's contents render if they aren't a
                room.

            Parameters:
                look(object):      The class:`thing <qtmud.Thing>` that
                                    is doing the looking. Output will be
                                    written from this thing's perspective.
                target(str):        A string representing a nametag of an
                                    object in ``thing``'s environment.

            Returns:
                string:             Returns what the looker sees as a string.
        """
        line = Parser.parse_line(looker, line)
        scene = 'Whatever you tried to look at, you can\'t.'
        if 'subject' in line:
            subject = line['subject']
        elif len(line) == 1:
            subject = 'here'
        else:
            subject = None
        if (subject in ['room', 'here', 'location']
            and hasattr(looker, 'location')):
                subject = looker.location
        elif subject in ['me', 'self', 'myself']:
            subject = looker
        else:
            matches = looker.search(**line)
            if len(matches) == 1:
                subject = matches[0]
            elif len(matches) > 1:
                scene = ('More than one match, try using the full name of what you want:\n')
                for match in matches:
                        if hasattr(match, 'name') and hasattr(match, 'description'):
                            scene += ('{}\n'.format(match.name))
        if hasattr(subject, 'name') and hasattr(subject, 'description'):
            scene = '- {} -\n{}\n'.format(subject.name, subject.description)
        else:
            scene = 'Whatever you tried to look at can\'t be seen.'
        if hasattr(subject, 'exits') and subject.exits:
            scene += 'exits [ '
            for direction in subject.exits:
                scene += '{} , '.format(direction)
            scene += ']\n'
        if hasattr(subject, 'contents') and subject.contents:
            scene += 'contents: ( '
            for content in subject.contents:
                if hasattr(content, 'name') and hasattr(content, 'location'):
                    scene += '{}, '.format(content.name)
            scene += ')'
        looker.manager.schedule('send', thing=looker, scene=scene)
        return True

    def apply(self, thing):
        """
            .. versionadded:: 0.0.2-feature/parser

            Parameters:
                thing(object):      The :class:`thing <qtmud.Thing>` that will
                                    be given the Sighted quality.
        """
        if not hasattr(thing, 'look'):
            thing.look = types.MethodType(self.look, thing)
        if hasattr(thing, 'commands'):
            thing.commands['look'] = types.MethodType(self.look, thing)
        return thing
