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

# XXX If the manager instances each quality and applies from there, these 
# functions can be added to that class.
# Compare Client.send() and contains()

def contains(self, thing):
    """ simply check if `thing` is in the contents of `self` (the Container).
    """
    return thing in self.contents

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
        thing.addr = tuple
        thing.send_buffer = ''
        thing.recv_buffer = ''
        thing.send = self.send
        return thing

class Physical(object):
    """ Gives a thing some Physical qualities:
            location: where the thing is contained.
    """
    def __init__(self, **kw):
        """ create the main Client quality instance, so we don't have to 
            keep creating more of them.
        """
        # XXX ^^-^^ It might not actually do that, but that is what it 
        # *should* be doing.
        super(Physical, self).__init__(**kw)
        return
    
    def apply(self, thing):
        """ adds thing.location as class object
        """
        # XXX This might be broken/wrong, but the engine still works and 
        # this'll end up being rewritten when environments are made a thing.
        thing.location = object
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
        
    def apply(self, thing):
        """ adds list contents and function contains to thing
        """
        thing.contents = []
        thing.contains = contains

class Room(object):
    """ Gives a thing the qualities of a Room
    """
    def __init__(self, **kw):
        """ create the main Client quality instance, so we don't have to 
            keep creating more of them.
        """
        # XXX ^^-^^ It might not actually do that, but that is what it 
        # *should* be doing.
        super(Room, self).__init__(**kw)
        return
    
    def apply(self, thing):
        """ adds dict exits and if non-existent, list contents & function 
            contains
        """
        thing.exits = {}
        if not hasattr(thing, 'contents'): thing.contents = []
        if not hasattr(thing, 'contains'): thing.contains = contains
        return thing
        
