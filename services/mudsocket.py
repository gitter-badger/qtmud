import select
import socket

import qtmud
from qtmud import MUD_ADDR
from qtmud.services import Service
from qtmud.qualities import Client, Physical

class MUDSocket(object):
    """ The socket server that handles incoming MUD-style connections.
    """
    def __init__(self, manager, **kw):
        self.manager = manager
        if type(MUD_ADDR) == tuple:
            self.address = MUD_ADDR
        elif type(MUD_ADDR) == int:
            self.address = ('0.0.0.0', MUD_ADDR)
        else:
            self.manager.log.warning('qtmud.MUD_ADDR needs to be string '
                'or tuple, got {0}'.format(type(MUD_ADDR)))
            return
        self.socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        try:
            self.socket.bind(self.address)
        except Exception as err:
            self.manager.log.error('{0} failed to bind on '
                '{1} - {2}'.format(self.__class__.__name__, self.address, err))
            self.manager.log.error('this is fatal, exit()ing')
            exit()
        self.socket.listen(5)
        self.connections = [self.socket]
        self.clients = {}
        return
    
    def tick(self, events):
        # XXX go back in and fix some long code names, repeated references, etc.
        """ Each tick, parse the incoming and outgoing data and handle it
        """
        r, w, e = select.select(self.connections, [conn for conn,
            client in self.clients.items() if client.send_buffer != ''], [], 0)
        if r:
            for conn in r:
                if conn is self.socket:
                    new_conn, addr = conn.accept()
                    client = self.manager.new_thing(Client, Physical)
                    client.update({'addr': addr, 'send_buffer' : '',
                        'recv_buffer' : ''})
                    self.connections.append(new_conn)
                    self.clients[new_conn] = client
                    self.manager.schedule('move', thing=client,
                        destination=qtmud.manager.back_room)
                else:
                    data = conn.recv(1024)
                    if data == b'':
                        self.connections.remove(conn)
                    else:
                        # do some work splitting incoming data into a command
                        self.clients[conn].recv_buffer += data.decode('utf8',
                            'ignore')
                        if '\n' in self.clients[conn].recv_buffer:
                            self.manager.log.info('{0} told us:: {1}'
                                ''.format(self.clients[conn].__class__.__name__, 
                                self.clients[conn].recv_buffer.rstrip()))
                            split = self.clients[conn].recv_buffer.rstrip().split('\n', 1)
                            if len(split) == 2:
                                line, self.clients[conn].recv_buffer = split
                            else:
                                line, self.clients[conn].recv_buffer = split[0], ''
                            if ' ' in line:
                                split = line.split(' ', 1)
                                if len(split) == 2:
                                    cmd, trailing = split
                                else:
                                    cmd, trailing = split[0], ''
                            else:
                                cmd, trailing = line, ''
                        self.manager.schedule('parse', 
                            client=self.clients[conn],
                            cmd=cmd, trailing=trailing)
        if w:
            for conn in w:
                conn.send(self.clients[conn].send_buffer.encode('utf8'))
                self.manager.log.info('we told {0}: {1}'
                    ''.format(self.clients[conn].__class__.__name__,
                        self.clients[conn].send_buffer.rstrip('\n')))
                self.clients[conn].send_buffer = ''
        return
