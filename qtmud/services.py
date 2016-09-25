import select
import socket

import qtmud
from qtmud.builders import build_client

MUD_SOCKET = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
MUD_SOCKET.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)



class MUDSocket(object):
    def __init__(self):
        self.logging_in = set()
        self.clients = dict()
        self.connections = list()


    def bind(self, address):
        try:
            MUD_SOCKET.bind(address)
        except OSError:
            return False
        MUD_SOCKET.listen(5)
        self.connections.append(MUD_SOCKET)
        return True


    def tick(self):
        read, write, error = select.select(self.connections,
                                           [conn for conn,
                                            client in self.clients.items() if
                                            client.send_buffer != ''],
                                           [],
                                           0)
        if read:
            for conn in read:
                if conn is MUD_SOCKET:
                    new_conn, addr = conn.accept()
                    qtmud.log.debug('new connection accepted from %s', format(addr))
                    client = build_client()
                    client.update({'addr': addr,
                                   'send_buffer': '',
                                   'recv_buffer': ''})
                    self.connections.append(new_conn)
                    self.clients[new_conn] = client
                    self.logging_in.add(client)
                    qtmud.schedule('send',
                                   recipient=client,
                                   text=qtmud.SPLASH)
                else:
                    data = conn.recv(1024)
                    if data == b'':
                        self.connections.remove(conn)
                        qtmud.log.debug('lost connection from %s',
                                        format(self.clients[conn].addr))
                        qtmud.schedule('client_disconnect',client=self.clients[
                            conn])
                    else:
                        client = self.clients[conn]
                        client.recv_buffer += data.decode('utf8', 'ignore')
                        if '\n' in client.recv_buffer:
                            split = client.recv_buffer.rstrip().split('\n', 1)
                            if len(split) == 2:
                                line, client.recv_buffer = split
                            else:
                                line, client.recv_buffer = split[0], ''
                            if client in self.logging_in:
                                qtmud.schedule('client_login',
                                               client=client,
                                               line=line)
                            else:
                                qtmud.schedule('process_client_input',
                                               client=client,
                                               line=line)
        if write:
            for conn in write:
                conn.send(self.clients[conn].send_buffer.encode('utf8'))
                self.clients[conn].send_buffer = ''
        return True