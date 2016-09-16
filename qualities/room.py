""" gives a thing the qualities of a room

    .. moduleauthor:: emsenn <morgan.sennhauser@gmail.com>

    .. versionadded:: 0.0.2-feature/parser
"""


import types


class Room(object):
    """ Gives a thing the qualities of a Room

        .. versionadded:: 0.0.2-feature/parser

        Attributes:
            exits(dict):        A dict of the exits in this room, expected to
                                be in the format { 'inside' : Hotel }, where
                                'inside' is the string a thing would use to
                                reference the exit, and Hotel is a class
                                representing a Quality to be applied to a thing.
    """
    def __init__(self):
        """
            .. versionadded:: 0.0.2-feature/parser
        """
        self.exits = {}
        return

    def apply(self, thing):
        """ adds exits to the thing

            .. versionadded:: 0.0.2-feature/parser
            .. versionchanged:: 0.0.2-feature/renderer

            Adds exits to a thing.

            .. note:: Used to be dependent on Container quality, now it
                      isn't.
        """
        if not hasattr(thing, 'exits'):
            thing.exits = self.exits
        return thing
