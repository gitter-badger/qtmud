""" Gives the ability to see to a thing.
    .. moduleauthor:: emsenn <morgan.sennhauser@gmail.com>

    .. versionadded:: 0.0.1-features/parser

    Adds sight to a quality, which for now means access to the look
    function and command.
"""


import types
from qtmud.qualities import Physical, Renderable, Room, Container


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

    def look(self, thing, target=''):
        """ Render target from the perspective of thing.

            .. versionadded:: 0.0.1-features/parser
            .. versionchanged:: 0.0.2-features/renderer
                Made thing.look() directly callable.

            Parameters:
                thing(object):      The class:`thing <qtmud.Thing>` that
                                    is doing the looking. Output will be
                                    written from this thing's perspective.
                target(str):        A string representing a nametag of an
                                    object in ``thing``'s environment.
        """
        if target != '' and target.split()[0] == 'at':
            target = target.split(None, 1)[1]
        if target in ['', 'here']:
            if Physical in thing.qualities:
                if hasattr(thing, 'location') and thing.location is not None:
                    if Renderable in thing.location.qualities:
                        scene = ('- {0} -\n'
                                 '{1}\n'
                                 '[ '.format(thing.location.name,
                                             thing.location.description))
                    else:
                        scene = ('Wherever you are, you can\'t observe it.')
                    if Room in thing.location.qualities:
                        for direction in thing.location.exits:
                            scene += (direction+', ')
                    scene += ' ]\n( '
                    if Container in thing.location.qualities:
                        print(thing.location.contents)
                        for content in thing.location.contents:
                            if Renderable in content.qualities:
                                scene += (content.name+', ')
                    scene += ')'
                else:
                    scene = ('You\'re no place you can see.')
                    thing.manager.log.debug('%s tried to look but they are'
                                            'outside of any environment.')
            else:
                scene = ('You aren\'t physical.')
                thing.manager.log.debug('%s tried to look, but they aren\'t'
                                        'material so have no location',
                                        thing.name)
        elif target in ['self', 'me']:
            if Renderable in thing.qualities:
                scene = ('- {0} - \n'
                         '{1}'.format(thing.name, thing.description))
            else:
                scene = ('You have no renderable body, I\'m afraid.')
                thing.manager.log.debug('%s tried to look at themselves '
                                        'but lack the Renderable quality',
                                        thing.name)
        thing.manager.schedule('render', client=thing, scene=scene)

    def apply(self, thing):
        """
            .. versionadded:: 0.0.1-features/parser
        """
        if not hasattr(thing, 'look'):
            thing.look = types.MethodType(self.look, thing)
        if hasattr(thing, 'commands'):
            thing.commands['look'] = types.MethodType(self.look, thing)
        return thing
