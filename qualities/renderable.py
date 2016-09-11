""" Adds a name and description to a thing.

    .. moduleauthor:: emsenn <morgan.sennhauser@gmail.com>

    .. versionadded:: 0.0.1-features/parser
        was a part of qtmud.qualities

"""

class Renderable(object): #pylint: disable=too-few-public-methods
    """ For applying the Renderable quality to a thing.

        .. version added:: 0.0.1-features/environments

        Attributes:
            name(str):          The name of the thing.
            description(str):   The thing's description.
    """
    def __init__(self):
        """

            .. version added:: 0.0.1-feature/environments

        """
        self.name = ''
        self.description = ''
        return

    def apply(self, thing):
        """ Applies the Renderable quality to a thing

            .. version added:: 0.0.1-feature/environments
        """
        if not hasattr(thing, 'name'):
            thing.name = self.name
        if not hasattr(thing, 'description'):
            thing.description = self.description
        return thing
