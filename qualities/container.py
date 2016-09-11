import types

class Container(object):
    def __init__(self):
        return
    
    def add(self, container, thing):
        """ Add a thing to the inventory of another, _if_ it isn't already 
            there.
        """
        if thing not in container.contents:
            print(container.contents)
            return container.contents.append(thing)
    
    def contains(self, container, thing):
        """ simply check if `thing` is in the contents of `self` '
            (the Container).
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
