""" qtmud's main module. contains Thing and Manager

    .. module:: qtmud
        :synopsis: Contains Thing & Manager classes, used for creating and
            managing objects.
    
    .. moduleauthor: Morgan Sennhauser <morgan.sennhauser@gmail.com>
    .. version added:: 0.0.1
    
    In addition to handling `Thing` and `Manager`, a few global constants 
    are set in the code below:
        NAME and VERSION can be whatever you want, but I'd suggest following
            our versioning pattern, available at docs/versioning.
        HOST & MUD_PORT are a string and integer representing where the 
            MUDSocket service will serve to.
"""

import logging
import uuid
import traceback
from collections import OrderedDict

NAME        = 'qtmud'
VERSION     = '0.0.1'
HOST        = 'localhost'
MUD_PORT    = 5787

# Currently set up to record all logging to debug.log, with only INFO 
# and higher priority messages going to console.
logging.basicConfig(filename='debug.log', filemode='w', 
                    format='%(asctime)s %(name)-12s %(levelname)-8s '
                           '%(message)s',
                    datefmt='%m-%d %H:%M',
                    level=logging.DEBUG)
CONSOLE = logging.StreamHandler()
# Change this to logging.DEBUG if you want everything on the console
CONSOLE.setLevel(logging.INFO)
CONSOLE.setFormatter(logging.Formatter('%(name)-12s %(levelname)-8s '
                                       '%(message)s'))

class Thing(object):
    """ Everything qtmud.manager handles is a thing or service.
        Things have qualities applied to them.
    """
    def __init__(self, identity, manager, **kw):
        super(Thing, self).__init__(**kw)
        self.identity, self.manager = identity, manager
        self.qualities = []
        return
    
    def update(self, _dict):
        """ Add multiple attributes to a thing.
        """
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
        self.log.addHandler(CONSOLE)
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
        """ Instance services and subscribe that instance to its subscriptions.
        """
        # Add services and their subscriptions
        for service in services:
            self.log.debug('adding %s as service', service.__name__)
            service = service(self)
            if not hasattr(service, 'subscriptions'):
                service.subscriptions = []
            for sub in service.subscriptions:
                self.subscribe(service,sub)
                self.log.debug('subscribing %s to event %s'
                               '', service.__class__.__name__, sub)
            self.services[service] = service
            self.log.debug('%s successfully added as service'
                           '', service.__class__.__name__)
        return True
                
    def schedule(self, command, **payload):
        """ schedules a command with manager, to be fired in the upcoming 
            tick()
        """
        event = (command, payload)
        for service in self.subscriptions.get(command, []):
            if service not in self.events:
                self.events[service] = []
            self.events[service].append(event)

    def subscribe(self, service, event):
        """ tells the manager that `service` is looking for `event
        """
        if service not in self.subscriptions:
            self.subscriptions[event] = []
        self.subscriptions[event].append(service)
    
    def new_thing(self, *qualities):
        """ sets up a new thing and gives it any qualities that were passed
        """
        while True:
            identity = uuid.uuid4()
            if identity not in self.things:
                break
        thing = Thing(identity, self)
        self.things.append(thing)
        self.log.debug('creating new thing...')
        self.add_qualities(thing, qualities)
        return thing

    def add_qualities(self, thing, qualities):
        """ adds qualities to a thing. qualities are extra variables or 
            functions that separate one thing from another, such as the
            Physical quality giving names and descriptions, Client setting 
            a thing up to be a client, so on.
        """
        for quality in qualities:
            if not quality in self.qualities:
                self.qualities[quality] = []
            self.qualities[quality].append(thing)
            thing.qualities.append(quality)
            thing = quality().apply(thing)
            self.log.debug('added %s quality to the thing'
                           '', quality.__name__)
            return thing
        

    def run(self):
        """ main game loop right here
        """
        while True:
            self.tick()
    
    def tick(self):
        """ main game tick(). pushes out events to subscribers, who then 
            execute them. For example, the 'move' event goes out to the 
            Mover service, which does the business of taking things out 
            of one location and into another.
        """
        # Main game sequence. Should push events out to subscribers.
        events = self.events
        self.events = {}
        for service in self.services:
            try:
                service.tick(events.pop(service, []))
            # service.tick()s shouldn't be failing, but if they do, it 
            # probably shouldn't be fatal...
            except Exception as err: #pylint: disable=broad-except
                self.log.warning('%s failed to tick: %s',
                                 service.__class__.__name__, err)
                traceback.print_exc()
        return True
