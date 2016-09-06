def send(self, data, end='\n'):
    """ prepare data to be sent to a client.
    """
    self.send_buffer += data + end

def contains(self, thing):
    return thing in self.contents

class Client(object):
    """ Turns a bland thing into a fancy Client thing. adds the attributes:
            addr:           tuple representing the client's address
            send_buffer:    string going to be send to the client next tick()
            recv_buffer:    string received from the client this tick()
            send:           function for formating send_buffer\
    """
    def __init__(self, **kw):
        super(Client, self).__init__(**kw)
        return

    def apply(self, thing):
        thing.addr = tuple
        thing.send_buffer = ''
        thing.recv_buffer = ''
        thing.send = send
        return thing

class Physical(object):
    """ Gives a thing some Physical qualities:
            name:           the name the thing'll be referred to
    """
    def __init__(self, **kw):
        super(Physical, self).__init__(**kw)
        return
    
    def apply(self, thing):
        self.name, self.description = '', ''
        self.location = object
        return thing

class Container(object):
    def __init__(self, *a, **kw):
        (Container, self).__init__(*a, **kw)
        return
        
    def apply(self, thing):
        self.contents = []
        self.contains = contains

class Room(object):
    """ Gives a thing some Physical qualities:
            name:           the name the thing'll be referred to
    """
    def __init__(self, **kw):
        super(Room, self).__init__(**kw)
        return
    
    def apply(self, thing):
        if not hasattr(thing, 'contents'): thing.contents = []
        return thing
        
