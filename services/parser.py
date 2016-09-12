""" handles the input from clients

    .. module:: qtmud.services.parser
        :synopsis: handles the input from clients
    
    .. moduleauthor: Morgan Sennhauser <morgan.sennhauser@gmail.com>
    .. version added:: 0.0.1
    .. version changed:: 0.0.1-feature/organizing
        Added `look` and `go` commands
    .. version changed:: 0.0.1-feature/parser
        moved commands into their associated qualities
    
    Parser is subscribed to 'parse' events. It expects these events to have:
    
    * client - the object the client is associated with
    * cmd - the first word (split by space) of the client's line
    * trailing - everything after the first word.
    
    The code for how it works is pretty straightforward, and bad, at this 
    point, so I'm not going to bother thoroughly commenting it.
"""


class Parser(object):
    """ To listen for client input, Parser subscribes to 'parse' events
        
        .. versionadded:: 0.0.1-features/parser 
        
    """
    
    def __init__(self, manager):
        """
            .. versionadded:: 0.0.1-feature/parser
            .. versionchanged:: 0.0.2-feature/renderer
                removed unnecessary dependency on :class:`Service 
                <qtmud.services.Service>`
        """
        self.subscriptions = ['parse']
        self.manager = manager
        self.manager.subscribe(self, 'parse')
    
    def tick(self, events=False):
        """ Handle commands from the last tick.
        
            .. versionadded:: 0.0.1-feature/parser
            .. versionchanged:: 0.0.2-feature/nametags
                Added better failure control.
            
            Parameters:
                events(list):       set to False by default, expected to 
                                    be a list of tuples in the format of 
                                    ``[('render', {payload})]``
                
            Returns:
                bool:               True if there were events to process,
                                    otherwise False.
            
            The ``payload`` of each event is expected to have:
                
                * ``client`` - represents the client who is trying to have 
                  their command parsed.
                * ``cmd`` - a single word that represent's the command 
                  ``client`` is trying to execute.
                * ``trailing`` - this one is optional, and is any text that 
                  came after the ``cmd`` in the player's input.

            If the Bob inputs ``say hello there skippy``, ``client`` would 
            be the object that represent's Bob's avatar, ``cmd`` would be 
            ``say``, and ``trailing`` would be ``hello there skippy``.
            
            If ``cmd`` (in this case ``say``) is in the client's list of 
            :attr:`commands <qtmud.qualities.client.Client.commands>`,
            then the method that command points to will be called, with 
            ``trailing`` as an argument. In our example, ``bob.say('hello 
            there skippy')``.
        """
        if events == []:
            return False
        for event, payload in events: #pylint: disable=unused-variable
            client = payload['client']
            cmd = payload['cmd']
            if 'trailing' in payload: trailing = payload['trailing']
            else: trailing = ''
            if hasattr(client, 'commands') and cmd in client.commands:
                client.commands[cmd](trailing)
            elif hasattr(client, 'send'):
                client.manager.schedule('render',
                                        client=client,
                                        scene=('{0} isnt a valid command'
                                              ''.format(cmd)))
                self.manager.log.debug('client %s input invalid command "%s"',
                               client.identity,
                               (cmd + trailing))
            else:
                self.manager.log.debug('client %s input invalid command "%s"'
                                       'and has no send() method over which '
                                       'to communicate.',
                                       client.identity,
                                       (cmd + trailing)) 
        return True
