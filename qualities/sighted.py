""" Gives the ability to see to a thing.

    .. moduleauthor:: emsenn <morgan.sennhauser@gmail.com>

    .. versionadded:: 0.0.1-features/parser

    Adds sight to a quality, which for now means access to the look
    function and command.
"""


import types


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

    def look(self, looker, target=''):
        """ Render ``target`` from the perspective of ``looker``.

            .. versionadded:: 0.0.1-feature/parser
            .. versionchanged:: 0.0.2-feature/renderer
                Made thing.look() directly callable.
            .. versionchanged:: 0.0.2-feature/neverforgetholidayupdate
                rely on checking the attributes of things directly, instead
                of using checks against Qualities
            .. versionchanged:: 0.0.2-feature/nametags
                use nametags instead of names to figure out what to look at.

            Parameters:
                look(object):      The class:`thing <qtmud.Thing>` that
                                    is doing the looking. Output will be
                                    written from this thing's perspective.
                target(str):        A string representing a nametag of an
                                    object in ``thing``'s environment.

            Returns:
                string:             Returns what the looker sees as a string.
        """
        if target != '' and target.split()[0] in ['at', 'in']:
            target = target.split(None, 1)[1]
        if target in ['', 'here']:
            if hasattr(looker, 'location') and looker.location is not None:
                if hasattr(looker.location, 'name'):
                    if hasattr(looker.location, 'description'):
                        scene = ('- {0} -\n'
                                 '{1}\n'
                                 '[ '.format(looker.location.name,
                                             looker.location.description))
                else:
                    scene = ('Wherever you are, you can\'t observe it.')
                if hasattr(looker.location, 'exits'):
                    for direction in looker.location.exits:
                            scene += (direction+', ')
                scene += ' ]\n( '
                if hasattr(looker.location, 'contents'):
                    for content in looker.location.contents:
                        if hasattr(content, 'name'):
                                if hasattr(content, 'location'):
                                    if content.location is looker.location:
                                        scene += (content.name+', ')
                scene += ')'
            else:
                scene = ('You\'re no place you can see.')
                looker.manager.log.debug('%s tried to look but they are'
                                        'outside of any environment.')
        elif target in ['self', 'me']:
            if hasattr(looker, 'name') and hasattr(looker, 'description'):
                scene = ('- {0} - \n'
                         '{1}'.format(looker.name, looker.description))
            else:
                scene = ('You have no renderable body, I\'m afraid.')
                look.manager.log.debug('%s tried to look at themselves '
                                        'but don\'t have a name or '
                                        'description', looker.name)
        else:
            matches = looker.search(target)
            if target in matches:
                target = matches[target]
                if type(target) is list:
                    if len(target) == 1:
                        if hasattr(target[0], 'name'):
                            if hasattr(target[0], 'description'):
                                scene = ('- {0} -\n'
                                         '{1}'.format(target[0].name,
                                                      target[0].description))
                    elif len(target) > 1:
                        scene = ('Multiple potential matches:\n')
                        for match in target:
                            if hasattr(match, 'name'):
                                scene += (match.name+'\n')
            else:
                scene = ('Whatever you tried to look at, you can\'t.')
        if hasattr(looker, 'send'):
            looker.manager.schedule('render', client=looker, scene=scene)
        return scene

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
