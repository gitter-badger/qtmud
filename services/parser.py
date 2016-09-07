""" handles the input from clients

    .. module:: qtmud.services.parser
        :synopsis: handles the input from clients
    
    .. moduleauthor: Morgan Sennhauser <morgan.sennhauser@gmail.com>
    .. version added:: 0.0.1
    
    Parser is subscribed to 'parse' events. It expects these events to have:
    
    * client - the object the client is associated with
    * cmd - the first word (split by space) of the client's line
    * trailing - everything after the first word.
    
    The code for how it works is pretty straightforward, and bad, at this 
    point, so I'm not going to bother thoroughly commenting it.
"""

from qtmud.services import Service
from qtmud.qualities import Client

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
    
    def tick(self, events=False):
        """ If Parser service has any events, parse them and respond 
            appropriately.
        """
        if events is False:
            return False
        for event, payload in events: #pylint: disable=unused-variable
            client = payload['client']
            cmd = payload['cmd']
            trailing = payload['trailing']
            # XXX Watch for these errors and build proper exceptions as 
            # they're discovered.
            if cmd == 'echo':
                try:
                    client.send(client, trailing)
                    break 
                except Exception as err:
                    self.manager.log.warning('unexpected exception caught '
                                             'when %s entered the command '
                                             '%s %s\nerror to follow:%s', 
                                             client.name, cmd, trailing, err)
                    client.send(client, 'the command failed, check console')
            elif cmd == 'whoami':
                try:
                    client.send(client, '{0}'.format(client.name))
                except Exception as err:
                    self.manager.log.warning('unexpected exception caught '
                                             'when %s entered the command '
                                             '%s %s\nerror to follow:%s', 
                                             client.name, cmd, trailing, err)
                    client.send(client, 'the command failed, check console')
            elif cmd == 'say':
                for recipient in client.location.contents:
                    if recipient in self.manager.qualities[Client]:
                        recipient.send(recipient, '{0} says: {1}'
                                       ''.format(client.name, trailing))
            elif cmd == 'whereami':
                try:
                    client.send(client, '{0}'.format(client.location.name))
                except Exception as err:
                    self.manager.log.warning('unexpected exception caught '
                                             'when %s entered the command '
                                             '%s %s\nerror to follow:%s', 
                                             client.name, cmd, trailing, err)
                    client.send(client, 'the command failed, check console')
            elif cmd == 'set':
                if trailing == '':
                    client.send('syntax: set <attribute> <value>',
                                'example: set name Bob')
                trailing = trailing.split()
                attribute, value = trailing[0], " ".join(trailing[1:])
                try:
                    setattr(client, attribute, value)
                except Exception as err:
                    self.manager.log.warning('unexpected exception caught '
                                             'when %s entered the command '
                                             '%s %s\nerror to follow:%s', 
                                             client.name, cmd, trailing, err)
                    client.send(client, 'the command failed, check console')
            else:
                client.send(client, '{0} isnt a valid command'.format(cmd))
        return
