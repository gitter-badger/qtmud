""" MUD socket methods

    .. versionadded:: 0.0.4

    Attributes:
        MUD_SOCKET(object):     socket that qtmud serves MUD data through
        clients(dict):          {socket object : client body}
        connections(list):      the connections directly
        logging_in(set):        clients in the middle of logging in
"""

import select
import socket


import qtmud
import qtmud.qualities.client
import mudlib

MUD_SOCKET = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
MUD_SOCKET.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)

clients = dict()
connections = list()
logging_in = set()




def process_client_input(client, line):
    """ Process client input

        Parameters:
            client(object):         body of client who input information
            line(str):              information input by client
        Return:
            bool:                   True
    """
    command = line.split(' ')[0]
    if command in client.commands:
        client.commands[command](line)
    else:
        qtmud.schedule('send',
                       recipient=client,
                       text='invalid command: {}'.format(line))
    return True
qtmud.subscriptions.add(process_client_input)


def bind(address):
    """ bind MUD_SOCKET to address and listen

        Parameters:
            address(tuple):          expected to be (str, int), where str is
                                    hostname and int is port
        Return:
            bool:                   True if bound, otherwise False
    """
    try:
        MUD_SOCKET.bind(address)
    except OSError:
        return False
    MUD_SOCKET.listen(5)
    connections.append(MUD_SOCKET)
    return True


def tick():
    """ handles reading and writing from MUD_SOCKET

        Return:
            bool:           True
    """
    read, write, error = select.select(connections,
                                       [conn for conn,
                                        client in clients.items() if
                                        client.send_buffer != ''],
                                       [],
                                       0)
    if read:
        for conn in read:
            if conn is MUD_SOCKET:
                new_conn, addr = conn.accept()
                qtmud.log.debug('new connection accepted from %s', format(addr))
                client = qtmud.qualities.client.apply(qtmud.new_thing())
                client.update({'addr': addr,
                               'send_buffer': '',
                               'recv_buffer': ''})
                connections.append(new_conn)
                clients[new_conn] = client
                logging_in.add(client)
                qtmud.schedule('send',
                               recipient=client,
                               text=qtmud.SPLASH)
            else:
                data = conn.recv(1024)
                if data == b'':
                    connections.remove(conn)
                    mudlib.remove_client(clients[conn])
                    qtmud.log.debug('lost connection from %s',
                                    format(clients[conn].addr))
                else:
                    client = clients[conn]
                    client.recv_buffer += data.decode('utf8', 'ignore')
                    if '\n' in client.recv_buffer:
                        split = client.recv_buffer.rstrip().split('\n', 1)
                        if len(split) == 2:
                            line, client.recv_buffer = split
                        else:
                            line, client.recv_buffer = split[0], ''
                        if client in logging_in:
                            client.name = line
                            mudlib.add_client(client)
                            logging_in.remove(client)
                        else:
                            qtmud.schedule('process_client_input',
                                           client=client,
                                           line=line)
    if write:
        for conn in write:
            conn.send(clients[conn].send_buffer.encode('utf8'))
            clients[conn].send_buffer = ''
    return True
