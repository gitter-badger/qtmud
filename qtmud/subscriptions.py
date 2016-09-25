import qtmud
from qtmud.services import MUDSocket

def finger(fingerer, fingeree):
    mudsocket = qtmud.active_services[MUDSocket]
    line = fingeree.split(' ')
    if len(line) == 2:
        if line[1] in ['me', 'self']:
            fingeree= fingerer
        else:
            for socket in mudsocket.clients:
                client = mudsocket.clients[socket]
                if line[1] == client.name.lower():
                    fingeree = client
                    break
        if not fingeree:
            output = 'No such thing'
        else:
            mudsocket.build_finger(fingeree)
    else:
        output = 'syntax: finger <thing>'
    qtmud.schedule('send',
                   recipient=fingerer,
                   text=output)
    return True

def send(recipient, text):
    if hasattr(recipient, 'send_buffer'):
        recipient.send_buffer += '{}\n'.format(text)
    return True

def process_client_input(client, line):
    command = line.split(' ')[0]
    if command in client.commands:
        client.commands[command](line)
    else:
        qtmud.schedule('send',
                       recipient=client,
                       text=('invalid command: {}. "commands" will show '
                             'you available commands.'.format(line)))
    return True