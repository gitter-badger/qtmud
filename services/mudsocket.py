""" service handling MUD-formatted socket connections.

    .. moduleauthor: Morgan Sennhauser <morgan.sennhauser@gmail.com>
    
    .. version added:: 0.0.1
    .. version changed:: 0.0.1-feature/environments
        Added applying the Sight quality to incoming connections
    .. version changed:: 0.0.1-feature/parsing
        Added applying the Container and Speaking qualities to incoming 
        connections.
    
    The service which provides socket server and basic parsing of incoming 
    and outgoing data.
"""

# TODO write better documentation for qtmud.services.mudsocket

import select
import socket


import qtmud
from qtmud import HOST, MUD_PORT, SPLASH
# These are all the qualities that are applied to a client's thing to make 
# it useful.
from qtmud.qualities import (Client, Physical, Container, Sighted, Renderable,
                             Speaking, Hearing, Prehensile, Learning)


class MUDSocket(object):
    """ A service which handles a socket connection.
    
        Parameters:
            manager(object):        automatically passed by 
                                    :func:`add_services()  
                                    <qtmud.Manager.add_services>`, the 
                                    :class:`manager <qtmud.Manager>`
        
        Attributes:
            manager(object):        The same as the manager above.
            
        The MUDSocket service handles the socket connection. It has no 
        real API for interacting with the rest of qtmud, and needs to be 
        rewritten and documented once we explore client accounts.
    """
    def __init__(self, manager):
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
        self.logging_in = set()
        return
    
    def tick(self, events): #pylint: disable=unused-variable
        # XXX go back in and fix some long code names, repeated references, etc.
        """ Each tick, parse the incoming and outgoing data and handle it.

            .. versionadded:: 0.0.1-feature/environments
            .. versionchanged:: 0.0.3-feature/noise
                Fixed Issue #9, clients not being removed when disconnecting
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
                    client = self.manager.new_thing(Client)
                    client.update({'addr': addr,
                                   'send_buffer' : '',
                                   'recv_buffer' : ''})
                    self.connections.append(new_conn)
                    self.clients[new_conn] = client
                    client.manager.schedule('send',
                                            thing=client,
                                            scene=(qtmud.SPLASH))
                    self.logging_in.add(client)
                else:
                    data = conn.recv(1024)
                    if data == b'':
                        self.connections.remove(conn)
                        self.manager.schedule('move',
                                                thing=self.clients[conn],
                                                destination=None)
                    else:
                        client = self.clients[conn]
                        client.recv_buffer += data.decode('utf8',
                                                                      'ignore')
                        if '\n' in client.recv_buffer:
                            split = client.recv_buffer.rstrip().split('\n', 1)
                            if len(split) == 2:
                                line, client.recv_buffer = split
                            else:
                                line = split[0]
                                client.recv_buffer = ''
                            if client in self.logging_in:
                                client.name = line
                                scene = ('Giving you some qualities: '
                                         'Container, Hearing, '
                                         'Learning, Physical, Renderable, '
                                         'Sighted, Speaking, and Prehensile.')
                                client.manager.schedule('send',
                                                        thing=client,
                                                        scene=scene)
                                client.manager.add_qualities(client,
                                                             [Container,
                                                              Hearing,
                                                              Learning,
                                                              Physical,
                                                              Renderable,
                                                              Sighted,
                                                              Speaking,
                                                              Prehensile])
                                client.manager.schedule('move',
                                                        thing=client,
                                                        destination=client.manager.back_room)
                                self.logging_in.remove(client)
                            else:
                                self.manager.schedule('parse',
                                                      commander=client,
                                                      line=line)
        if w:
            for conn in w:
                conn.send(self.clients[conn].send_buffer.encode('utf8'))
                self.clients[conn].send_buffer = ''
        return
