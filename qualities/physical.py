""" Makes a thing have a location, the place it exists.

    .. versionadded:: 0.0.1-feature/parsing
"""



import types


class Physical(object):
    """ Functions and attributes to be applied to Physical things.

            .. versionadded:: 0.0.1
            .. versionchanged:: 0.0.1-feature/parsing
                added whereami and move commands

        Attributes:
            location(object):       The :class:`thing <qtmud.Thing>` that
                                    :func:`contains
                                    <qtmud.qualities.Container.contains>`
                                    this thing.
    """
    def __init__(self, **kw):
        """
            .. versionadded:: 0.0.1
        """
        super(Physical, self).__init__(**kw)
        self.location = object
        return

    #pylint: disable=unused-argument,no-self-use
    def whereami(self, thing, trailing):
        """ tells thing the name of its location

            .. versionadded:: 0.0.1-feature/parsing
        """
        thing.manager.schedule('render',
                               client=thing,
                               scene=thing.location.name)

    def move(self, thing, direction):
        """ moves a thing from one location into another

            .. versionadded:: 0.0.1-feature/parsing
        """
        if not hasattr(thing.location, 'exits'):
            thing.send('You\'ve ended up in a location without any exit.'
                       'I\'m going to move you back to the starting room.')
            thing.manager.schedule('move',
                                   thing=thing,
                                   destination=thing.manager.back_room)
            return
        if direction in thing.location.exits:
            # TODO add better class/object checking
            destination = thing.location.exits[direction]
            if destination in thing.manager.qualities:
                # XXX this is a hack
                destination = thing.manager.qualities[destination][0]
            else:
                destination = thing.manager.new_thing(destination)
            try:
                thing.manager.schedule('move',
                                       thing=thing,
                                       destination=destination)
            except Exception as err:
                thing.manager.log.warning('failed to move %s,\n%s',
                                          thing.idenity,
                                          err)

    def apply(self, thing):
        """ Applies the Physical quality to the `thing`

            .. versionadded:: 0.0.1
            .. versionchanged:: 0.0.1-feature/parsing
                added whereami and move commands
        """
        if not hasattr(thing, 'location'):
            thing.location = self.location
        if hasattr(thing, 'commands'):
            thing.commands['whereami'] = types.MethodType(self.whereami, thing)
            thing.commands['move'] = types.MethodType(self.move, thing)
        return thing
