""" service handling MUD-formatted socket connections.

    .. module:: qtmud.services.mudsocket
        :synopsis: service handling MUD-formatted socket connections.
    
    .. moduleauthor: Morgan Sennhauser <morgan.sennhauser@gmail.com>
    .. version added:: 0.0.1
    
    The service which provides socket server and basic parsing of incoming 
    and outgoing data.
"""

import select
import socket

import qtmud
from qtmud import HOST, MUD_PORT
from qtmud.qualities import Client, Physical, Renderable

class MUDSocket(object):
    """ The socket server that handles incoming MUD-style connections.
    """
    def __init__(self, manager, **kw):
        super(MUDSocket, self).__init__(**kw)
        self.manager = manager
        self.address = (HOST, MUD_PORT)
        self.socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        try:
            self.socket.bind(self.address)
        except OSError as err:
            self.manager.log.error('%s failed to bind on %s: %s', 
                                   self.__class__.__name__, 
                                   self.address,
                                   err)
            self.manager.log.critical('this is fatal, exit()ing')
            exit()
        self.socket.listen(5)
        self.connections = [self.socket]
        self.clients = {}
        return
    
    def tick(self, events): #pylint: disable=unused-variable
        # XXX go back in and fix some long code names, repeated references, etc.
        """ Each tick, parse the incoming and outgoing data and handle it
        """
        r, w, e = select.select(self.connections, #pylint: disable=invalid-name
                                [conn for conn,
                                 client in self.clients.items() if
                                 client.send_buffer != ''],
                                [],
                                0)
        if r:
            for conn in r:
                if conn is self.socket:
                    new_conn, addr = conn.accept()
                    client = self.manager.new_thing(Client, Physical, 
                                                    Renderable)
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
                                              cmd=cmd,
                                              trailing=trailing)
        if w:
            for conn in w:
                conn.send(self.clients[conn].send_buffer.encode('utf8'))
                self.clients[conn].send_buffer = ''
        return
