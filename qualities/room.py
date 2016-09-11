"""
    .. versionadded:: 0.0.1-features/parser
"""


import types


class Room(object):
    """ Gives a thing the qualities of a Room
    """
    def __init__(self):
        """
            .. versionadded:: 0.0.1-features/parser
        """
        self.exits = {}
        return

    def apply(self, thing):
        """ adds exits to the thing

            .. versionadded:: 0.0.1-features/parser
            .. versionchanged:: 0.0.2-features/renderer

            Adds exits to a thing.

            .. note:: Used to be dependent on Container quality, now it
                      isn't.
        """
        if not hasattr(thing, 'exits'):
            thing.exits = self.exits
        return thing
