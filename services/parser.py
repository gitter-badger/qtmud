from qtmud.services import Service
from qtmud.qualities import Client

class Parser(Service):
    
    def __init__(self, manager, **kw):
        super(Parser, self).__init__(manager, **kw)
        self.subscriptions.append('parse')
    
    def tick(self, events=[]):
        if events == []:
            return False
        for event, payload in events:
            client = payload['client']
            cmd = payload['cmd']
            trailing = payload['trailing']
            if cmd == 'echo':
                try:
                    client.send(client, trailing)
                except:
                    client.send(client, 'whoops')
            if cmd == 'whoami':
                try:
                    client.send(client, '{0}'.format(client))
                except:
                    client.send(client, 'command failed')
            if cmd == 'say':
                for receipient in self.manager.qualities[Client]:
                    receipient.send(receipient, '{0} says: {1}'
                        ''.format(client, trailing))
        return
