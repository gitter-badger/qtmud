""" qtmud's main module contains Manager & Thing, and a few constants.

    .. moduleauthor: Morgan Sennhauser <morgan.sennhauser@gmail.com>
    
    .. versionadded:: 0.0.1
    .. versionchanged:: 0.0.1-feature/parsing
        expanded documentation
        
    This is the main module of qtmud. It contains two objects, Thing and 
    Manager, as well as several constants.
    
    qtmud expects to be started by having the 
    :class:`Manager <qtmud.Manager>` instanced, and then that object having 
    the :func:`add_services <qtmud.Manager.add_services>` function called.
    
    Attributes:
        NAME(str):      the name of the MUD being presented by qtmud.
        VERSION(str):   the version of the MUD
        HOST(str):      the hostname the MUD should be served through
        MUD_PORT(int):  the port the MUDSocket should bind to.
"""


import logging
import uuid
import traceback
from collections import OrderedDict


# Whatever you want your MUD to be called. Should be a string
NAME        = 'qtmud'
# The version of your MUD. check docs/versioning. should be a string
VERSION     = '0.0.3'
# 'localhost' for development, '0.0.0.0' for production.
HOST        = 'localhost'
# the port you want the MUDSocket service to listen over. should be integer
MUD_PORT    = 5787


# Currently set up to record all logging to debug.log, with only INFO 
# and higher priority messages going to console.
logging.basicConfig(filename='debug.log', filemode='w', 
                    format='%(asctime)s %(name)-12s %(levelname)-8s '
                           '%(message)s',
                    datefmt='%m-%d %H:%M',
                    level=logging.DEBUG)
CONSOLE = logging.StreamHandler()
# Change this to logging.DEBUG if you want everything on the console.
CONSOLE.setLevel(logging.INFO)
CONSOLE.setFormatter(logging.Formatter('%(name)-12s %(levelname)-8s '
                                       '%(message)s'))


class Thing(object):
    """ The object to be instanced by manager.new_thing()
        
        .. versionadded:: 0.0.1
        .. versionchanged:: 0.0.1-feature/parsing
            added return of successfully changed attributes to Thing.update()
        .. versionchanged:: 0.0.2-feature/nametags
        .. versionchanged:: 0.0.2-feature/textblob
            changed nametags to be a set instead of a list
        
        Parameters:
            identity(str):      a UUID created automatically by the 
                                manager.new_thing() function
            manager(object):    the manager instance which is instancing the 
                                thing.
        
        Attributes:
            identity(str):      the unique identifier for the instance, 
                                assigned by manager.new_thing()
            manager(object):    the thing's manager, the same object that 
                                called new_thing()
            nametags(set):      A set of strings that one might refer to
                                this thing with.
            qualities(list):    the instances of 
                                :class:`qualities <qtmud.Qualities>` which 
                                have been applied to the thing.

        Thing anticipates being instanced by the 
        :func:`new_thing() <qtmud.Manager.new_thing>`, which is why it 
        expects the `identity` and `manage` parameters.
    """
    def __init__(self, identity, manager):
        """
            .. versionadded:: 0.0.1
            
        """
        self.identity, self.manager = identity, manager
        self.nametags = {'thing'}
        self.adjectives = set()
        self.qualities = []
        return
    
    def __setattr__(self, attr, value):
        """ If thing has set_attr function, use it as a custom setter

            .. versionadded:: 0.0.2-feature/nametags

            Paramters:
                attr:       The attribute to be set
                value:      The value ``attr`` is going to be set to.
            
            Returns:
                bool:       True if attribute properly set, otherwise False.

            If a thing has a ``set_attr`` function, when something goes to 
            set ``attr``, use the ``set_attr`` function instead. For 
            example, :attr:`names <qtmud.qualities.renderable.Renderable.name>`
            have a :func:`set_name() 
            <qtmud.qualities.renderable.Renderable.set_name>` function that
            adds the last word of the new thing's name as a nametag.

            Example:
                Making a new thing and setting it's name
            
                >>> womble = manager.new_thing(Renderable)
                >>> womble.nametags
                [ 'thing' ]
                >>> womble.name = 'Jeffrey'
                >>> womble.nametags
                [ 'jeffrey', 'thing']
        """
        if 'set_%s' % (attr,) in self.__dict__:
            return self.__dict__['set_%s' % (attr,)](self, value)
        else:
            self.__dict__[attr] = value

    def set_adjectives(self, adjectives):
        """
            .. versionadded:: 0.0.2-feature/textblob
        """
        if type(adjectives) is set and adjectives != {}:
            for adjective in adjectives:
                self.nametags.add(adjective)
        return

    def set_nametags(self, nametags):
        """
            .. versionadded:: 0.0.2-feature/textblob
        """
        if type(nametags) is set:
            for nametag in nametags:
                self.nametags.add(nametag)
        return

    def search(self, subject=None, adjectives=None, pnp_clauses=None, **kwargs):
        """ search for in this local environment.
        
            .. versionadded:: 0.0.2-feature/nametags
            .. versionadded:: 0.0.2-feature/textblob
                rewritten to handle the output produced by Parser.parse_line()
            
            Parameters:
                target(string):         The nametag you're looking for in
                                        this thing's local environment.
        """
        matches = []
        if subject is not None:
            if hasattr(self, 'contents'):
                for content in self.contents:
                    for nametag in content.nametags:
                        if nametag == subject:
                            matches.append(content)
            if hasattr(self, 'location'):
                for content in self.location.contents:
                        for nametag in content.nametags:
                                if nametag == subject:
                                    matches.append(content)
            if adjectives is not None:
                old_matches = matches
                new_matches = []
                for match in old_matches:
                    for adjective in adjectives:
                        if adjective in match.adjectives:
                            matching_adjectives = True
                        else:
                            matching_adjectives = False
                    if matching_adjectives is True:
                        new_matches.append(match)
                matches = new_matches
        return matches

    def update(self, dict):
        """ Modify multiple attributes of the thing at once.
        
            .. versionadded:: 0.0.1
            .. versionchanged:: 0.0.1-feature/parsing
                added return of successfully updated attributes.
        
            Parameters:
                _dict(dict):    a dict of `{attr : value}` where attr is 
                                an attribute of the thing.
            
            Returns:
                dict:           a dict of successfully modified attributes and 
                                the value they were changed to.
            
            Example:
                MUDSocket after creating a qualified thing for a new client
                
                >>> client.update({'addr': addr,
                >>>                'send_buffer' : '',
                >>>                'recv_buffer' : ''})
                {'addr': ('127.0.0.1', 40440), 'recv_buffer': '', 
                'send_buffer': ''}
        """
        for attribute, value in dict.items():
            if 'set_%s' % (attribute,) in self.__dict__:
                self.__dict__['set_%s' % (attribute,)](self, value)
            else:
                self.__dict__[attribute] = value

class Manager(object):
    """ The manager of all qtmud things and services.
    
        .. versionadded:: 0.0.1
        .. versionchanged:: 0.0.2-feature/nametags
            removed unnecessary junk from __init__()
 
        When qtmud is started, it creates an instance of this class. This 
        instance is then used to handle pretty much every game occurence.
        For a design overview, check the main README.
        
        Attributes:
            log(object):                an instance of :class:`Logger 
                                        <logging.get_Logger>`, is used 
                                        throughout the engine with
                                        :func:`qtmud.Manager.log.debug`,
                                        :func:`qtmud.Manager.log.info`,
                                        :func:`qtmud.Manager.log.warning`,
                                        :func:`qtmud.Manager.log.error`, and 
                                        :func:`qtmud.Manager.log.critical`.
            things(list):               a list of every thing that the 
                                        manager has instanced this session.
            qualities(dict):            every quality which has been applied 
                                        this session, with every thing it 
                                        has been applied to as a value.
            services(OrderedDict):      an OrderedDict() of every service 
                                        the manager is controlling (sending 
                                        events to during tick()
            subscriptions(dict):        events and which services are looking 
                                        for them
            events(dict):
                                        the events that will occur during 
                                        the next tick().
    """
    def __init__(self):
        """
            .. versionadded:: 0.0.1
        
        """
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
        """ Instance services and subscribe them to their subscriptions.
        
            .. versionadded:: 0.0.1
        
            Parameters:
                *services(list):    a list of the classes to be added as 
                                    services.
            
            Returns:
                list:               a list of the services which were 
                                    successfully instanced
            
            Example:
                qtmud start script after instancing :class:`qtmud.Manager`
                
                >>> manager.add_services(MUDSocket, Mover, Parser)
                [<qtmud.services.mudsocket.MUDSocket object at 0x7f39bbbb10f0>, 
                <qtmud.services.parser.Parser object at 0x7f39bce5fdd8>, 
                <qtmud.services.mover.Mover object at 0x7f39bce6e668>]

        """
        # Add services and their subscriptions
        added_services = []
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
            added_services.append(service) 
        return added_services
                
    def schedule(self, command, **payload):
        """ schedules a `command` to be fired next `tick()`
        
            .. versionadded:: 0.0.1
            
            Parameters:
                command(str):       The command that services are 
                                    subscribed to.
                **payload(dict):    Any additional arguments, collapsed 
                                    into a dict to be handed off to the 
                                    subscribed service.

            Returns:
                tuple:              the event as given to the manager, a 
                                    tuple of (command, **payload))
        
            Checks for services that are subscribed to `command`, and 
            adds the event to any service which is.
        """
        event = (command, payload)
        for service in self.subscriptions.get(command, []):
            if service not in self.events:
                self.events[service] = []
            self.events[service].append(event)
        return event

    def subscribe(self, service, event):
        """ subscribes a service to events
        
            Parameters:
                service(object):    The service which will be notified of 
                                    the event.
                event(str):         The event the service will be notified 
                                    of, such as 'parse' or 'move'
            
            Returns:
                bool:               True if the service was successfully 
                                    subscribed to the event.
        """
        if service not in self.subscriptions:
            self.subscriptions[event] = []
        self.subscriptions[event].append(service)
        return True
    
    def new_thing(self, *qualities):
        """ create a new thing and passes *qualities to 
            add_qualities(thing, quality)
        
            Parameters:
                *qualities(list):   A list of Qualities (classes) to be 
                                    applied to the new thing.
            
            Returns:
                object:             The thing that was created, with all 
                                    qualities applied.
        
            Creates a new instance of :class:`qtmud.Thing` and gives it an 
            :attr:`identity <qtmud.Thing.identity>`. Then, adds the thing 
            to :attr:`qtmud.Manager.things`, before calling 
            :func:`add_qualities(thing, qualities) 
            <qtmud.Manager.add_qualities>` to apply the desired qualities 
            to the thing.
            
            This function then returns the finished thing, with all of its 
            qualities.

        """
        while True:
            identity = uuid.uuid4()
            if identity not in self.things:
                break
        thing = Thing(identity, self)
        self.things.append(thing)
        self.log.debug('creating new thing...')
        thing = self.add_qualities(thing, qualities)
        return thing

    def add_qualities(self, thing, qualities):
        """ adds qualities to :class:`things <qtmud.Thing>`
        
            .. versionadded:: 0.0.1
            .. versionchanged:: 0.0.2-feature/nametags
                Changed from imperative to applicative method
        
            Parameters:
                thing(object):      The :class:`thing <qtmud.Thing>` which 
                                    will have qualities applied to it.
                qualities(list):    The :mod:`qualities <qtmud.qualities>` 
                                    to be applied to ``thing``
            
            Returns:
                object:             The thing after having the qualities 
                                    :func:`applied 
                                    <qtmud.qualities.Quality.apply>`.
        """
        for quality in qualities:
            # TODO make sure quality is a class
            if not quality in self.qualities:
                self.qualities[quality] = []
            self.qualities[quality].append(thing)
            thing = quality().apply(thing)
            thing.qualities.append(quality)
            self.log.debug('added %s quality to the thing'
                           '', quality.__name__)
        return thing
        

    def run(self):
        """ Keep the manager alive
        
            .. versionadded:: 0.0.1
            
            Until a KeyboardInterrupt is noticed, this function keeps 
            qtmud calling the manager's :func:`tick() <qtmud.Manager.tick>` 
            function, keeping the game running.
        """
        while True:
            self.tick()
    
    def tick(self):
        """ qtmud's "heartbeat"
            
            .. versionadded:: 0.0.1
            
            Returns:
                bool:       True as long as nothing crashes the server.
            
            For every :class:`service <qtmud.services.Service>` in 
            :attr:`qtmud.services`, pass any 
            :attr:`events <qtmud.Manager.events>` they're
            :func:`subscribed <qtmud.Manager.subscribe>` to that service's 
            :func:`tick() <qtmud.services.Service.tick>` function.
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
