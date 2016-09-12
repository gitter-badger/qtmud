import types


class Client(object):
    """ Turns a bland thing into a fancy Client thing.

        .. versionadded:: 0.0.1
        .. versionchanged:: 0.0.1-feature/parser
            added the whoami, set, and echo commands
        
        Attributes:
            nametags(list):     List of strings representing different
                                :attr:`nametags <qtmud.Thing.nametags>`
                                the Client might have.
    """
    def __init__(self):
        """
            .. versionadded:: 0.0.1-feature/organizing
            .. versionchanged:: 0.0.2-feature/nametags
                added nametags = ['client']
        """
        self.nametags = ['client', 'player']
        return

    def send(self, thing, data):
        """ prepare data to be sent to a client.

            .. versionadded:: 0.0.1
            .. versionchanged:: 0.0.2-feature/parser
                moved the end-of-line tagging to the Renderer service.
        """
        thing.send_buffer += data

    def echo(self, thing, data):
        """ echo some text to the client)

            .. versionadded:: 0.0.1-feature/parser
        """
        thing.send(data)

    def whoami(self, thing, data):
        """ tells the thing their name and identity

            .. versionadded:: 0.0.1-feature/parser
        """
        finger = ''
        if hasattr(thing, 'name'):
            finger += ('name:        {0}\n'.format(thing.name))
        finger += ('id:          {0}\n'.format(thing.identity))
        if hasattr(thing, 'nametags'):
            finger += ('nametags:    {0}\n'.format(thing.nametags))
        thing.manager.schedule('render',client=thing,scene=finger)

    def set(self, thing, trailing):
        """ sets an attribute in the client, meant to be used with the
            set command

            .. version added:: 0.0.1-version/parser
        """
        if trailing == '':
            thing.manager.schedule('render',
                                   client=thing,
                                   scene=('syntax: set <attribute> <value>'
                                          'example: set name Bob'))
        trailing = trailing.split()
        attribute, value = trailing[0], " ".join(trailing[1:])
        if hasattr(thing, 'set_%s' % attribute):
            thing.__dict__['set_%s' % (attribute)](thing, value)
        try:
            setattr(thing, attribute, value)
        except Exception as err:
            thing.manager.log.warning('unexpected exception caught '
                                     'when %s entered the command '
                                     '%s %s\nerror to follow:%s',
                                     client.name, cmd, trailing, err)
            thing.send('the command failed, check console')

    def get(self, thing, trailing):
        attribute = trailing.split()[0]
        if hasattr(thing, attribute):
            thing.manager.schedule('render',
                                   client=thing,
                                   scene='{0}'.format(thing.__dict__[attribute]))

    def apply(self, thing):
        """ Applies the Client quality to `thing`

            .. versionadded:: 0.0.1
            .. versionchanged:: 0.0.1-feature/organizing
                added basic attribute overwrite protection
            .. versionchanged:: 0.0.1-feature/parser
                added commands dict to Client
            .. versionchanged:: 0.0.2-feature/nametags

            addr:           tuple representing the client's address
            send_buffer:    string going to be send to the client next tick()
            recv_buffer:    string received from the client this tick()
            send:           function for formating send_buffer
            whoami:         function for telling Client its name & identity
            echo:           function for testing Client's send/receive parsing
            set:            function for setting Client's attributes.
        """
        if hasattr(thing, 'nametags'):
            for nametag in self.nametags:
                if nametag not in self.nametags:
                    thing.nametags.insert(0, nametag)
        if not hasattr(thing, 'addr'):
            thing.addr = tuple
        if not hasattr(thing, 'send_buffer'):
            thing.send_buffer = ''
        if not hasattr(thing, 'recv_buffer'): 
            thing.recv_buffer = ''
        if not hasattr(thing, 'name'):
            thing.name = str(thing.identity)
        if not hasattr(thing, 'send'):
            thing.send = types.MethodType(self.send, thing)
        if not hasattr(thing, 'commands'):
            thing.commands = {'whoami': types.MethodType(self.whoami, thing),
                              'echo': types.MethodType(self.echo, thing),
                              'set': types.MethodType(self.set, thing),
                              'get': types.MethodType(self.get, thing)}
        return thing
