import logging

logging.basicConfig(level=logging.DEBUG)

class Thing(object):
    def __init__(self, **kw):
        return

class Manager(object):
    def __init__(self, **kw):
        super(Manager, self).__init__(**kw)
        self.log = logging.getLogger(self.__module__)
        # commands the Manager is looking to pass out
        self.subscriptions = {}
        # instructions and who gave them
        self.messages = {}
        return
    
    def add_services(self, *services):
        # Add services and their subscriptions
        for service in services:
            service = service(self)
            for sub in service.subscriptions:
                self.subscribe(service,sub)

    def subscribe(self, service, sub):
        # If this is the service's first subscription...
        if service not in self.subscriptions: self.subscriptions[sub] = []
        # Now tell the Manager to hit up `service` when it's `sub` is heard
        self.subscriptions[sub].append(service)

    def run(self):
        while True:
            self.tick()
    
    def tick(self):
        # Main game sequence. Should push events out to subscribers.
        pass
