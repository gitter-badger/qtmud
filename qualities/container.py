import types

class Container(object):
    def __init__(self, *a, **kw):
        super(Container, self).__init__(*a, **kw)
        return
    
    def add(self, thing):
        """ Add a thing to the inventory of another, _if_ it isn't already 
            there.
        """
        if thing not in self.contents:
            return self.contents.append(thing)
    
    def contains(self, thing):
        """ simply check if `thing` is in the contents of `self` '
            (the Container).
        """
        return thing in self.contents
    
    def remove(self, thing):
        """ removes a thing from another thing
        """
        if thing in self.contents: self.contents.remove(thing)
    
    def apply(self, thing):
        """ adds list contents and function contains to thing
        """
        if not hasattr(thing, 'contents'): thing.contents = []
        if not hasattr(thing, 'add'): 
            thing.add = types.MethodType(self.add, thing)
        if not hasattr(thing, 'contains'):
            thing.contains = types.MethodType(self.contains, thing)
        if not hasattr(thing, 'remove'):
            thing.remove = types.MethodType(self.contains, thing)
        return thing
