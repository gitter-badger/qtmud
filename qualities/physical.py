""" Makes a thing have a location, the place it exists.

    .. moduleauthor:: emsenn <morgan.sennhauser@gmail.com>

    .. versionadded:: 0.0.2-feature/parser
"""


import types


class Physical(object):
    """ Functions and attributes to be applied to Physical things.

            .. versionadded:: 0.0.1
            .. versionchanged:: 0.0.2-feature/parser
                added whereami and move commands

        Attributes:
            location(object):       The :class:`thing <qtmud.Thing>` that
                                    :func:`contains
                                    <qtmud.qualities.Container.contains>`
                                    this thing.
    """
    def __init__(self):
        """
            .. versionadded:: 0.0.1
        """
        self.location = object
        return

    @staticmethod
    def whereami(thing, line):
        """ tells thing the name of its location

            .. versionadded:: 0.0.2-feature/parser
            .. versionchanged:: 0.0.2-feature/textblob
                made more than just a test command, made static method

            Parameters:
                thing(object):          The :class:`thing <qtmud.Thing>` that
                                        is asking where it is.
                line(str):              Unused, a string matching client input.

            Returns:
                bool:                   True if the thing successfully queried
                                        has a location.

        """
        if hasattr(thing, 'send'):
            if hasattr(thing.location, 'name'):
                scene = 'You\'re location is the {}'.format(thing.location.name)
            else:
                scene = 'You\'re location is indescribable, but has the ' \
                        'identity {}'.format(thing.location.identity)
            thing.manager.schedule('send',
                                   thing=thing,
                                   scene=scene)
            return True
        return False

    # TODO: Split the move command and actual movement method into two methods
    @staticmethod
    def move(mover, line):
        """ moves a thing from one location into another

            .. versionadded:: 0.0.2-feature/parser
            .. versionchanged:: 0.0.2-feature/textblob
                changed to static method

            Parameters:
                mover(object):      The :class:`thing <qtmud.Thing>` that's
                                    going to be moved.
                line(str):          The name of the destination in the keys of
                                    thing.location.exits
        """
        line = ' '.join(line.split(' ')[1:])
        # This is kinda hacky but whatever.
        if not hasattr(mover.location, 'exits'):
            mover.send('You\'ve ended up in a location without any exit.'
                       'I\'m going to move you back to the starting room.')
            mover.manager.schedule('move',
                                   thing=mover,
                                   destination=mover.manager.back_room)
            return
        if line in mover.location.exits:
            destination = mover.location.exits[line]
            # this if/else is essentially saying "if there's an instance of
            # your destination already, move there, otherwise make an instance.
            if destination in mover.manager.qualities:
                destination = mover.manager.qualities[destination][0]
            else:
                destination = mover.manager.new_thing(destination)
            try:
                mover.manager.schedule('move',
                                       thing=mover,
                                       destination=destination)
                if hasattr(mover, 'send'):
                    mover.manager.schedule('send',
                                           thing=mover,
                                           scene='You move')
                return True
            except Exception as err:
                mover.manager.log.warning('failed to move %s,\n%s',
                                          mover.identity,
                                          err)
                return False

    def apply(self, thing):
        """ Applies the Physical quality to the `thing`

            .. versionadded:: 0.0.1
            .. versionchanged:: 0.0.2-feature/parser
                added whereami and move commands
        """
        if not hasattr(thing, 'location'):
            thing.location = self.location
        if hasattr(thing, 'commands'):
            thing.commands['whereami'] = types.MethodType(self.whereami, thing)
        return thing
