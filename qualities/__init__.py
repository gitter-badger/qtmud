def send(self, data, end='\n'):
    """ prepare data to be sent to a client.
    """
    self.send_buffer += data + end

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
        thing.qualities.append(self.__class__)
        thing.addr = tuple
        thing.send_buffer = ''
        thing.recv_buffer = ''
        thing.send = send
        return thing

