from qtmud.services import Service

class Parser(Service):
    
    def __init__(self, manager, **kw):
        super(Parser, self).__init__(manager, **kw)
        self.subscriptions.append('parse')
    
    def tick(self, events=[]):
        if events == []:
            return False
        for event, payload in events:
            print(payload)
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
        return
