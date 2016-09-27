""" Subscriptions are methods which handle the interaction and manipulation
of :class:`things <qtmud.Thing>`.

Every method in this module is added to :attr:`qtmud.subscribers` when
:func:`qtmud.start`. Calls to these methods which have been :func:`scheduled
<qtmud.schedule>` as :attr:`events qtmud.events>` will be called when
:func:`qtmud.tick` is called.
"""

import qtmud
from qtmud import builders
from qtmud.services import MUDSocket


def client_login_parser(client, line):
    """ Handle log-in for arriving players - right now, just a basic check
    against qtmud.client_accounts to see if the client is there already.
    """
    output = ''
    #####
    #
    # start login process
    #
    #####
    if not hasattr(client, 'login_stage'):
        client.login_stage = 0
        output = 'Input [desired] client name and press <enter>.'
    #####
    #
    # check if client exits
    #
    #####
    elif client.login_stage == 0:
        if line in qtmud.client_accounts.keys():
            output = ('There\'s a client named {}, if you\'re them, type your '
                      'password and press <enter>'.format(line))
            client.login_stage = 2
        elif line:
            output = ('No client named {}, going to make an account with that '
                      'name. Type your desired password and press <enter>.'
                      ''.format(line))
            client.login_stage = 1
        else:
            output = ('Your client name can\'t be blank. Input what name '
                      'you\'d like to use and press <enter>.')
        client.name = line
    #####
    #
    # register new client
    #
    #####
    elif client.login_stage == 1:
        qtmud.client_accounts[client.name] = {'password' : line}
        client.login_stage = 9
        output = ('Client account registered with name {}, press '
                  '<enter> to finish logging in.'.format(client.name))
    #####
    #
    # login existing account
    #
    #####
    elif client.login_stage == 2:
        if line == qtmud.client_accounts[client.name]['password']:
            client.login_stage = 9
            output = ('That\'s the correct password, press <enter> to finish '
                      'logging in.')
        else:
            client.login_stage = 0
            output = ('That\'s not the right password for that account - '
                      'type your [desired] client name and press <enter>.')
    elif client.login_stage == 9:
        client = qtmud.builders.build_client(client)
    if output:
        qtmud.schedule('send', recipient=client, text=output)
    return True



def client_input_parser(client, line):
    """ Pushes a client's input to their designated parser subscription.
    """
    qtmud.schedule('{}'.format(client.input_parser), client=client, line=line)
    return True


def client_command_parser(client, line):
    """ The default qtmud command parser, what client input is run through
    once they've logged in.
    """
    command = line.split(' ')[0]
    if command in client.commands:
        client.commands[command](line)
    else:
        qtmud.schedule('send',
                       recipient=client,
                       text=('{} is not a valid command; check '
                             '"commands" for your commands.'.format(
                               command)))
    return True


def finger(fingerer, fingeree):
    """ A bad mimic of the *nix finger command, returns information about a
    client account.

        .. todo:: update to only use data in qtmud.client_accounts

    :param fingerer: the person requesting the finger sheet
    :param fingeree: the person who the finger sheet will be built for.
    """
    mudsocket = qtmud.active_services[MUDSocket]
    line = fingeree.split(' ')
    if len(line) == 2:
        if line[1] in ['me', 'self']:
            fingeree = fingerer
        else:
            for socket in mudsocket.clients:
                client = mudsocket.clients[socket]
                if line[1] == client.name.lower():
                    fingeree = client
                    break
        if not fingeree:
            output = 'No such client'
        else:
            builders.generate_finger(fingeree)
    else:
        output = 'syntax: finger <thing>'
    qtmud.schedule('send',
                   recipient=fingerer,
                   text=output)
    return True


def send(recipient, text):
    """ Prepares text to be sent to the recipient

    :param recipient: expected to be a :class:`thing <qtmud.Thing>,
                      specifically one with a send_buffer. (In qtmud, this
                      is only clients, though mudlibs may have more things
                      with send_buffers.
    :param text: the text to be appended to the recipient's send_buffer
    :return: True if text is added to recipient's send_buffer, otherwise False.
    """
    if hasattr(recipient, 'send_buffer'):
        recipient.send_buffer += '{}\n'.format(text)
        return True
    return False


