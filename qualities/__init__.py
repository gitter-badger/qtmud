""" different qualities things may have

    .. module:: qtmud.qualities
        :synopsis: different qualities things may have
    
    .. moduleauthor: Morgan Sennhauser <morgan.sennhauser@gmail.com>
    .. version added:: 0.0.1
    
    The classes representing different qualities a thing might be assigned.  
    For example, a kitchen is:
    
    * Renderable (can be looked at),
    * a Container (able to contain things, like a stove and your sandwich), 
    * and a Room (has defined exits, usually leading to other things that 
    are other Rooms.
    
    However, your room wouldn't have the Physical quality, because, despite 
    being able to contain things and be described, rooms are not actually 
    physical things themselves. 
"""

# XXX Add in more "if variable already exists" checks because that should 
# XXX just clearly be a thing.

import types

class Client(object):
    """ Turns a bland thing into a fancy Client thing.
    """
    def __init__(self, **kw):
        """ create the main Client quality instance, so we don't have to 
            keep creating more of them.
        """
        # XXX ^^-^^ It might not actually do that, but that is what it 
        # *should* be doing.
        super(Client, self).__init__(**kw)
        return

    def send(self, thing, data, end='\n'):
        """ prepare data to be sent to a client.
        """
        thing.send_buffer += data + end

    def apply(self, thing):
        """ applies the attributes:
            addr:           tuple representing the client's address
            send_buffer:    string going to be send to the client next tick()
            recv_buffer:    string received from the client this tick()
            send:           function for formating send_buffer
        """
        if not hasattr(thing, 'addr'):
            thing.addr = tuple
        if not hasattr(thing, 'send_buffer'):
            thing.send_buffer = ''
        if not hasattr(thing, 'recv_buffer'): 
            thing.recv_buffer = ''              
        if not hasattr(thing, 'name'):
            thing.name = str(thing.identity)
        if not hasattr(thing, 'send'):
            thing.send = types.MethodType(self.send, thing)  
        return thing

class Physical(object):
    """ Gives a thing some Physical qualities:
            location: where the thing is contained.
    """
    def __init__(self, **kw):
        """ Create an instance of the Physical quality.
        """
        super(Physical, self).__init__(**kw)
        return
    
    def apply(self, thing):
        """ applies the attributes:
            location: defaults to object
            
        """
        if not hasattr(thing, 'location'): thing.location = object
        return thing

class Renderable(object):
    """ Gives a thing some Renderable qualities:
            name:           the name the thing'll be referred to. set to
                            the thing's identity at first.
            description:    a long-form description of the item. set to an 
                            empty string at first.
    """
    def __init__(self, **kw):
        """ create the main Client quality instance, so we don't have to 
            keep creating more of them.
        """
        # XXX ^^-^^ It might not actually do that, but that is what it 
        # *should* be doing.
        super(Renderable, self).__init__(**kw)
        return
    
    def apply(self, thing):
        """ sets thing.name to thing.identity and adds string thing.description
        """
        thing.name, thing.description = thing.identity, ''
        return thing

class Container(object):
    def __init__(self, *a, **kw):
        """ create the main Client quality instance, so we don't have to 
            keep creating more of them.
        """
        # XXX ^^-^^ It might not actually do that, but that is what it 
        # *should* be doing.
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
        
class Sight(object):
    def __init__(self, **kw):
        super(Sight, self).__init__(**kw)
        return
    
    def look(self, thing, **payload):
        print('look been called')
        render = ('- {0} -\n'
                  '{1}\n'
                  '[ '.format(thing.location.name,
                               thing.location.description))
        for exit in thing.location.exits:
            render += (exit+', ')
        render += ' ]\n( '
        for content in thing.location.contents:
            render += (content.name+', ')
        render += ' )'
        return render
        
    
    def apply(self, thing):
        print('Sight being applied')
        if not hasattr(thing, 'look'): 
            thing.look = types.MethodType(self.look, thing)
        return thing        
