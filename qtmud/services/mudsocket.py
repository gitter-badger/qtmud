import select
import socket


import qtmud
import qtmud.qualities.client
import mudlib

clients = dict()
connections = list()
logging_in = set()


mud_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
mud_socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)


def process_client_input(client, line):
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
    try:
        mud_socket.bind(address)
    except OSError as err:
        qtmud.log.error('mudsocket failed to bind: {}'.format(err))
        qtmud.log.critical('This is fatal.')
        exit()
    mud_socket.listen(5)
    connections.append(mud_socket)
    return socket


def tick():
    r, w, e = select.select(connections,
                            [conn for conn,
                             client in clients.items() if
                             client.send_buffer != ''],
                            [],
                            0)
    if r:
        for conn in r:
            if conn is mud_socket:
                new_conn, addr = conn.accept()
                qtmud.log.debug('new connection accepted from {}'.format(addr))
                print('fooooo')
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
                # LOGIN GOES HERE
            else:
                data = conn.recv(1024)
                if data == b'':
                    connections.remove(conn)
                    # TODO finish removing client
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
                        mudlib.handle_client(client)
                        logging_in.remove(client)
                    else:
                        qtmud.schedule('process_client_input',
                                       client=client,
                                       line=line)
    if w:
        for conn in w:
            conn.send(clients[conn].send_buffer.encode('utf8'))
            clients[conn].send_buffer = ''
    return True