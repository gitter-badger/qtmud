import types
from qtmud.qualities.container import Container

class Room(object):
    """ Gives a thing the qualities of a Room
    """
    def __init__(self, **kw):
        """ create the main Client quality instance, so we don't have to 
            keep creating more of them.
        """
        super(Room, self).__init__(**kw)
        return
    
    def apply(self, thing):
        """ adds dict exits and if non-existent, list contents & function 
            contains
        """
        if not hasattr(thing, 'exits'): thing.exits = {}
        if not hasattr(thing, 'contents'): thing.contents = []
        if not hasattr(thing, 'add'):
            thing.add = types.MethodType(Container.add, thing)
        if not hasattr(thing, 'contains'):
            thing.contains = types.MethodType(Container.contains, thing)
        if not hasattr(thing, 'remove'):
            thing.remove = types.MethodType(Container.remove, thing)
        return thing
