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

from qtmud.services import Service
from qtmud.qualities import Client

# XXX Todo: break up parser into a command loading service - should commands 
# come from qualities directlY?

class Parser(Service):
    """ The parsing service.
        Subscribed to 'parse' events.
        
        Expecting client, cmd, and trailing in event payload
    """
    
    def __init__(self, manager, **kw):
        """ Add this service to the manager's subscriptions for 'parse'.
        """
        super(Parser, self).__init__(manager, **kw)
        # move parser to its own folder, keep commands under there and in 
        # lib/parser?
        self.subscriptions.append('parse')
        manager.subscribe(self, 'parse')
    
    def tick(self, events=False):
        """ If Parser service has any events, parse them and respond 
            appropriately.
        """
        if events == []:
            return False
        for __, payload in events: #pylint: disable=unused-variable
            client = payload['client']
            cmd = payload['cmd']
            if 'trailing' in payload: trailing = payload['trailing']
            else: trailing = ''
            if cmd in client.commands:
                client.commands[cmd](trailing)
            else:
                client.send('{0} isnt a valid command'.format(cmd))
        return
