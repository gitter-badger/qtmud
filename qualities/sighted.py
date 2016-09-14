""" Gives the ability to see to a thing.

    .. moduleauthor:: emsenn <morgan.sennhauser@gmail.com>

    .. versionadded:: 0.0.1-feature/parser

    Adds sight to a quality, which for now means access to the look
    function and command.
"""


import types
from qtmud.services import Parser


class Sighted(object):
    """ Adds sight to a thing it is applied to.

        .. versionadded:: 0.0.1-feature/parser

        When :func:`applied <qtmud.qualities.Quality.apply>` by the
        :class:`manager <qtmud.Manager>`, gives a thing sight. In this
        context, that means the :func:`look
        <qtmud.qualities.sight.Sighted.look>` function, documented below.
    """

    def __init__(self):
        """
            .. versionadded:: 0.0.1-features/parser
        """
        return

    def look(self, commander, line):
        """ Render ``target`` from the perspective of ``looker``.

            .. versionadded:: 0.0.1-feature/parser
            .. versionchanged:: 0.0.2-feature/renderer
                Made thing.look() directly callable.
            .. versionchanged:: 0.0.2-feature/neverforgetholidayupdate
                rely on checking the attributes of things directly, instead
                of using checks against Qualities
            .. versionchanged:: 0.0.2-feature/nametags
                use nametags instead of names to figure out what to look at.
            .. versionchanged:: 0.0.2-feature/adjectives
                changed to use the new Parser parse_line() function.

            Parameters:
                look(object):      The class:`thing <qtmud.Thing>` that
                                    is doing the looking. Output will be
                                    written from this thing's perspective.
                target(str):        A string representing a nametag of an
                                    object in ``thing``'s environment.

            Returns:
                string:             Returns what the looker sees as a string.
        """
        looker = commander
        line = Parser.parse_line(looker, line)
        if 'subject' in line:
            subject = line['subject']
        else:
            subject = 'here'
        if subject in ['room', 'here', 'location']:
            if hasattr(commander, 'location') and looker.location is not None:
                if hasattr(looker.location, 'name') and hasattr(looker.location, 'description'):
                    scene = ('- {} -\n{}\n'.format(looker.location.name,
                                                   looker.location.description))
                else:
                    scene = ('Wherever you are, it has no visual description.')
                if hasattr(looker.location, 'exits'):
                    scene += ('exits: [ ')
                    for direction in looker.location.exits:
                        if hasattr(direction, 'name'):
                            scene += ('{}, '.format(direction))
                    scene += (']\n')
                if hasattr(looker.location, 'contents'):
                    scene += ('contents: ( ')
                    for content in looker.location.contents:
                        if hasattr(content, 'name') and hasattr(content, 'location'):
                            if content.location is looker.location:
                                scene += ('{}, '.format(content.name))
                    scene += (')')
        elif subject in ['me', 'self', 'myself']:
            if hasattr(looker, 'name') and hasattr(looker, 'description'):
                scene = ('- {} -\n{}'.format(looker.name, looker.description))
            else:
                scene = ('You don\'t have a self to look at.')
        else:
            scene = ('whatever you tried to look at, you can\'t.')
        looker.manager.schedule('render', client=looker, scene=scene)
        return True

    def apply(self, thing):
        """
            .. versionadded:: 0.0.1-feature/parser

            Parameters:
                thing(object):      The :class:`thing <qtmud.Thing>` that will
                                    be given the Sighted quality.
        """
        if not hasattr(thing, 'look'):
            thing.look = types.MethodType(self.look, thing)
        if hasattr(thing, 'commands'):
            thing.commands['look'] = types.MethodType(self.look, thing)
        return thing
