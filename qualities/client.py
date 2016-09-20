""" Makes a thing a client.

    .. moduleauthor:: emsenn <morgan.sennhauser@gmail.com>

    .. versionadded:: 0.0.2-feature/parser
        was a part of qtmud.qualities
"""

import types


class Client(object):
    """ Turns a bland thing into a fancy Client thing.

        .. versionadded:: 0.0.1
        .. versionchanged:: 0.0.2-feature/parser
            added the whoami, set, and echo commands
        
        Attributes:
            nametags(list):         List of strings representing different
                                    :attr:`nametags <qtmud.Thing.nametags>`
                                    the Client might have.
            addr(tuple):            The address the Client is connected from,
                                    expected to be a tuple of (str, int) where
                                    the string is their IP address and the int
                                    is what port they're connecting over.
            send_buffer(string):    What's going to be sent to the client on
                                    :class:`MUDSocket()'s
                                    <qtmud.services.mudsocket.MUDSocket>` next
                                    tick.
            recv_buffer(string):    A string of what the client has sent so
                                    far, updated each tick. Only processed
                                    (usually) after each line.
    """

    def __init__(self):
        """
            .. versionadded:: 0.0.1-feature/organizing
            .. versionchanged:: 0.0.2-feature/nametags
                added nametags = ['client', 'player']
            .. versionchanged:: 0.0.2-feature/textblob
                added addr, recv_buffer, send_buffer
        """
        self.nametags = ['client', 'player']
        self.addr = tuple
        self.send_buffer = ''
        self.recv_buffer = ''
        return

    @staticmethod
    def send(thing, data):
        """ prepare data to be sent to a client.

            .. versionadded:: 0.0.1
            .. versionchanged:: 0.0.2-feature/parser
                moved the end-of-line tagging to the Renderer service.
            .. versionchanged:: 0.0.2-feature/textblob
                changed to be a staticmethod
        """
        thing.send_buffer += data

    @staticmethod
    def echo(thing, line):
        """ echo some text to the client)

            .. versionadded:: 0.0.1-feature/parser
            .. versionchanged:: 0.0.2-feature/textblob
                changed to be a staticmethod
        """
        thing.send(line)

    @staticmethod
    def whoami(thing, line):
        """ tells the thing their name and identity

            .. versionadded:: 0.0.1-feature/parser
            .. versionchanged:: 0.0.2-feature/textblob
                changed to be a staticmethod
        """
        finger = ''
        if hasattr(thing, 'name'):
            finger += ('name:        {0}\n'.format(thing.name))
        finger += ('id:          {0}\n'.format(thing.identity))
        if hasattr(thing, 'nametags'):
            finger += ('nametags:    {0}\n'.format(thing.nametags))
        thing.manager.schedule('send', thing=thing, scene=finger)

    @staticmethod
    def set(client, line):
        """ sets an attribute in the client, meant to be used with the
            set command

            .. versionadded:: 0.0.2-feature/parser
            .. versionchanged:: 0.0.2-feature/textblob
                changed to be a staticmethod
        """
        line = line.split(' ')[1:]
        if line == '':
            client.manager.schedule('send',
                                    thing=client,
                                    scene=('syntax: set <attribute> <value>'
                                           'example: set name Bob'))
        attribute, value = line[0], " ".join(line[1:])
        if hasattr(client, 'set_%s' % attribute):
            client.__dict__['set_%s' % attribute](client, value)
        try:
            setattr(client, attribute, value)
        except Exception as err:
            client.manager.log.warning('unexpected exception caught '
                                       'when %s entered the command '
                                       '%s\nerror to follow:%s',
                                       client.name, line, err)
            client.send('the command failed, check console')

    @staticmethod
    def get(client, line):
        """ returns the value of the attribute in line.

            Parameters:
                client(object):         The client (a :class:`thing
                                        <qtmud.Thing>` that we're looking for
                                         the attribute of.
                line(str):              get() only uses the first word (split
                                        on space) to see which attribute we're
                                        looking for.
            Returns:
                The value of whatever attribute the first word of line is.
        """
        attribute = line.split()[0]
        if hasattr(client, attribute):
            client.manager.schedule('thing',
                                    thing=client,
                                    scene='{}'.format(client.__dict__[attribute]))

    @staticmethod
    def foo(client, line):
        print(client.qualities)

    def apply(self, thing):
        """ Applies the Client quality to `thing`

            .. versionadded:: 0.0.1
            .. versionchanged:: 0.0.1-feature/organizing
                added basic attribute overwrite protection
            .. versionchanged:: 0.0.1-feature/parser
                added commands dict to Client
            .. versionchanged:: 0.0.2-feature/nametags
                added nametags client, player, to quality application
            .. versionchanged:: 0.0.2-feature/textblob
                updated application of nametags now that they're a set.

            Parameters:
                thing(object):      The :class:`thing <qtmud.Thing>` we're
                                    going to be giving the qualities of client
                                    to.
        """
        if hasattr(thing, 'nametags'):
            for nametag in self.nametags:
                thing.nametags.add(nametag)
        if not hasattr(thing, 'addr'):
            thing.addr = self.addr
        if not hasattr(thing, 'send_buffer'):
            thing.send_buffer = self.send_buffer
        if not hasattr(thing, 'recv_buffer'):
            thing.recv_buffer = self.recv_buffer
        if not hasattr(thing, 'send'):
            thing.send = types.MethodType(self.send, thing)
        if not hasattr(thing, 'commands'):
            thing.commands = {'whoami': types.MethodType(self.whoami, thing),
                              'echo': types.MethodType(self.echo, thing),
                              'set': types.MethodType(self.set, thing),
                              'get': types.MethodType(self.get, thing),
                              'foo': types.MethodType(self.foo, thing)}
        return thing
