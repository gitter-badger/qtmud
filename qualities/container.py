""" A Container has contents that can be added to or removed from

    .. versionadded:: 0.0.1-features/parser

    From an abstract standpoint, many different things could be a 
    Container. A cardboard box would obviously be a Container, but 
    so would an office. The difference is that a box would also be 
    :class:`Physical <qtmud.qualities.physical.Physical>`, while an 
    office is more of an abstract thing, so would lack that particular 
    Quality.

    All a container really does is give a :class:`thing <qtmud.Thing>` 
    the ability to have an inventory - referred to in the game as the 
    thing's :attr:`contents <qtmud.qualities.container.Container.contents>`. 
    These contentsmight be manipulated in a lot of ways - the 
    :class:`Mover <qtmud.services.mover.Mover>` uses it to, well, move 
    things, and Sight frequently means looking at a things inventory.
"""


import types


class Container(object):
    """ Containers gain contents and methods for handling that.

        .. versionadded:: 0.0.1-features/parser
        .. versionchanged:: 0.0.2-features/renderer
 
        Attributes:
            contents(list):         The contents of the :class:`Thing 
                                    <qtmud.Thing>` has been applied to.
    """
    def __init__(self):
        """
            .. versionadded:: 0.0.1-features/parser
        """
        self.contents = []
        return
    
    def add(self, container, thing):
        """ Adds thing to the contianer's contents if thing isn't there.

            .. versionadded:: 0.0.1-features/parser
        """
        if thing not in container.contents:
            return container.contents.append(thing)
    
    def contains(self, container, thing):
        """ Check if 
        """
        return thing in container.contents
    
    def remove(self, container, thing):
        """ removes a thing from another thing
        """
        if thing in container.contents: container.contents.remove(thing)
    
    def apply(self, thing):
        """ adds list contents and function contains to thing
        """
        if not hasattr(thing, 'contents'):
            thing.contents = []
        if not hasattr(thing, 'add'): 
            thing.add = types.MethodType(self.add, thing)
        if not hasattr(thing, 'contains'):
            thing.contains = types.MethodType(self.contains, thing)
        if not hasattr(thing, 'remove'):
            thing.remove = types.MethodType(self.remove, thing)
        return thing
