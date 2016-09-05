from qtmud.services import Service

class Parser(Service):
    
    def __init__(self, manager, **kw):
        super(Parser, self).__init__(manager, **kw)
        self.subscriptions.append('parse')
    
    def tick(self, line):
        if line == []:
            return
        else:
            print(line)
            return
