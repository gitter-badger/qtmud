def send(self, data, end='\n'):
    self.send_buffer += data + end

class Client(object):
    def __init__(self, **kw):
        super(Client, self).__init__(**kw)
        return
    

    
    def apply(self, thing):
        thing.qualities.append(self)
        thing.addr = tuple
        thing.send_buffer = ''
        thing.recv_buffer = ''
        thing.send = send
        return thing

