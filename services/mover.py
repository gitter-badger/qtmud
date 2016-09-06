from qtmud.services import Service

class Mover(Service):
    def __init__(self, manager, **kw):
        super(Mover, self).__init__(manager, **kw)
        self.subscriptions.append('move')
        
    def tick(self, events=[]):
        if events == []:
            return False
        print(events)
        for event, payload in events:
            thing = payload['thing']
            destination = payload['destination']
            print('!!!! {0}'.format(destination))
            try:
                thing.location.contents.remove(thing)
            except:
                pass
            if destination is None:
                pass
            else:
                thing.location = destination
                thing.location.contents.append(thing)
            print(thing.location)
        return True
