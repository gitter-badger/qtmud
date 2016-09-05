import logging
import threading
from collections import OrderedDict

logging.basicConfig(level=logging.DEBUG)

MUD_ADDR = ('0.0.0.0', 5787)

class Thing(object):
    def __init__(self, **kw):
        self.qualities = []
        return
    
    def update(self, _dict):
        for key, value in _dict.items():
            setattr(self, key, value)

class Manager(object):
    def __init__(self, **kw):
        super(Manager, self).__init__(**kw)
        self.log = logging.getLogger(self.__module__)
        # list of things that exist
        self.things = []
        # list of services
        self.services = OrderedDict()
        # commands the Manager is looking to pass out
        self.subscriptions = {}
        # instructions and who gave them
        self.events = {}
        return
    
    def add_services(self, *services):
        # Add services and their subscriptions
        for service in services:
            self.log.info('adding {0} as service'.format(service))
            service = service(self)
            if not hasattr(service, 'subscriptions'): service.subscriptions = []
            for sub in service.subscriptions:
                self.subscribe(service,sub)
                self.log.info('subscribing {0} to event {1}'
                    ''.format(service, sub))
            self.services[service] = service
            self.log.info('{0} successfully added as service'.format(service))
        return True
                
    def schedule(self, command, **payload):
        event = (command, payload)
        for service in self.subscriptions.get(command, []):
            if service not in self.events: self.events[service] = []
            self.events[service].append(event)

    def subscribe(self, service, event):
        if service not in self.subscriptions: self.subscriptions[event] = []
        self.subscriptions[event].append(service)
    
    def new_thing(self, *qualities):
        thing = Thing()
        self.things.append(thing)
        self.log.debug('creating new thing with qualities: '
            '{0}'.format(qualities))
        for quality in qualities:
            # this is probably awful
            thing = quality().apply(thing)
        self.log.debug('created a new thing with qualities: '
            '{0}'.format(thing.qualities))
        return thing

    def run(self):
        while True:
            self.tick()
    
    def tick(self):
        # Main game sequence. Should push events out to subscribers.
        events = self.events
        self.events = {}
        for service in self.services:
            service.tick(events.pop(service, []))
        #for service in self.services:
        #    try:
        #        service.tick(events.pop(services, []))
        #    except Exception as err:
        #        self.log.debug('{0} tick failed: {1}'
        #            ''.format(service, err))
        #        return False
        return True
