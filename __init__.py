import logging
import uuid
import traceback
from collections import OrderedDict

logging.basicConfig(level=logging.DEBUG)

MUD_ADDR = ('0.0.0.0', 5787)

class Thing(object):
    """ Everything qtmud.manager handles is a thing or service.
        Things have qualities applied to them.
    """
    def __init__(self, identity, manager, **kw):
        self.identity, self.manager = identity, manager
        self.qualities = []
        return
    
    def update(self, _dict):
        # Quickly update multiple qualities of a thing.
        for key, value in _dict.items():
            setattr(self, key, value)

class Manager(object):
    """ referenced across the engine as qtmud.manager, a Manager() instance 
        is the main driver of the engine, with functions for adding 
        services and handling the event scheduler.
    """
    def __init__(self, **kw):
        super(Manager, self).__init__(**kw)
        self.log = logging.getLogger(self.__module__)
        # list of all the instanced things
        self.things = []
        # dict of key:qualities, value: instanced things with those qualities
        self.qualities = {}
        # list of all the instanced services
        self.services = OrderedDict()
        # commands the Manager is looking to pass out
        self.subscriptions = {}
        # instructions and who gave them, resets every tick()
        self.events = {}
        return
    
    def add_services(self, *services):
        # Add services and their subscriptions
        for service in services:
            self.log.info('adding {0} as service'.format(service.__name__))
            service = service(self)
            if not hasattr(service, 'subscriptions'): service.subscriptions = []
            for sub in service.subscriptions:
                self.subscribe(service,sub)
                self.log.info('subscribing {0} to event {1}'
                    ''.format(service.__class__.__name__, sub))
            self.services[service] = service
            self.log.info('{0} successfully added as service'
                ''.format(service.__class__.__name__))
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
        while True:
            thing = uuid.uuid4()
            if thing not in self.things:
                break
        thing = Thing(thing, self)
        self.things.append(thing)
        self.log.info('creating new thing...')
        self.add_qualities(thing, qualities)
        self.log.info('created a new thing with qualities: '
            '{0}'.format(thing.qualities))
        return thing

    def add_qualities(self, thing, qualities):
        for quality in qualities:
            if not quality in self.qualities:
                self.qualities[quality] = []
            self.qualities[quality].append(thing)
            thing.qualities.append(quality)
            thing = quality().apply(thing)
            self.log.info('added {0} quality to the new thing'.format(quality.__name__))
        

    def run(self):
        while True:
            self.tick()
    
    def tick(self):
        # Main game sequence. Should push events out to subscribers.
        events = self.events
        self.events = {}
        for service in self.services:
            try:
                service.tick(events.pop(service, []))
            # service.tick()s shouldn't be failing, but if they do, it 
            # probably shouldn't be fatal...
            except Exception as err:
                self.log.warning('{0} failed to tick: {1}'
                    ''.format(service.__class__.__name__, err))
                traceback.print_exc()
        return True
