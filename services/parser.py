""" handles the input from clients

    .. module:: qtmud.services.parser
        :synopsis: handles the input from clients
    
    .. moduleauthor: Morgan Sennhauser <morgan.sennhauser@gmail.com>
    .. version added:: 0.0.1
    .. version changed:: 0.0.1-feature/organizing
        Added `look` and `go` commands
    .. version changed:: 0.0.1-feature/parsing
        moved commands into their associated qualities
    
    Parser is subscribed to 'parse' events. It expects these events to have:
    
    * client - the object the client is associated with
    * cmd - the first word (split by space) of the client's line
    * trailing - everything after the first word.
    
    The code for how it works is pretty straightforward, and bad, at this 
    point, so I'm not going to bother thoroughly commenting it.
"""


from qtmud.qualities import Client


class Parser(object):
    """ To listen for client input, Parser subscribes to 'parse' events
        
        .. versionadded:: 0.0.1-features/parser 
        
    """
    
    def __init__(self, manager):
        """
            .. versionadded:: 0.0.1-features/parser
            .. versionchanged:: 0.0.2-features/renderer
                removed unnecessary dependency on :class:`Service 
                <qtmud.services.Service>`
        """
        self.subscriptions = ['parse']
        manager.subscribe(self, 'parse')
    
    def tick(self, events=False):
        """ Handle commands from the last tick.
        
            .. versionadded:: 0.0.1-features/parser
        """
        if events == []:
            return False
        for event, payload in events: #pylint: disable=unused-variable
            client = payload['client']
            cmd = payload['cmd']
            if 'trailing' in payload: trailing = payload['trailing']
            else: trailing = ''
            if cmd in client.commands:
                client.commands[cmd](trailing)
            else:
                client.send('{0} isnt a valid command'.format(cmd))
        return True
