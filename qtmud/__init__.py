""" The main qtmud module houses some constants, the Thing class, and methods
    for start()ing and tick()ing the MUD engine.
"""

#
import logging
import pickle
import uuid
from inspect import getmembers, isfunction, isclass


from qtmud import services, subscriptions, txt

# Pick which MUDLIB you wanna load
from mudlib import fireside
# from mudlib import starhopper
# from mudlib import yeolderpg


# GLOBAL REFERENCES
NAME = 'qtmud'
""" Name of the MUD engine. """
VERSION = '0.0.4'
""" MUD engine version """

# MUDLIB
MUDLIB = fireside # choices: starhopper, yeolderpg,
""" The module representing the :term:`mudlib` you want to load. Expected to
have a load() method for loading itself into qtmud. """

CLIENT_ACCOUNT_FILE = './data/client_accounts.p'
""" The file where pickled client accounts should be stored. """

# ADDRESS INFORMATION
IP6_ADDRESS = ('2606:a000:4701:b900:5604:830e:39f3:12f8', 5788, 0, 0)
""" Your IPv6 address is expected to be a four-element tuple, where the first
element is your IPv6 address, the second is qtmud's bound IPv6 port,
and I don't know what the last two elements do, to be quite honest."""
IP4_ADDRESS = ('0.0.0.0', 5787)
""" Your IPv4 address is expected to be a tuple of ('address', port), where
address is a string and port is an integer. Set your address to 'localhost'
for testing and development, and '0.0.0.0' for production/gameplay."""

SPLASH = txt.SPLASH.format(**locals())
""" The text new connections see. """

client_accounts = dict()
""" Populated by load_client_accounts(), a list of client accounts stored by
registered name."""

events = dict()
""" Events scheduled to occur next tick, populated by :func:`schedule`."""
things = dict()
""" all the things that new_thing() has made"""
subscribers = dict()
""" Methods which will be called for any relevant :attr:`events`. Populated
by :func:`qtmud.load` to contain bound methods of the methods in
:mod:`qtmud.subscriptions` referenced by method name. """
active_services = dict()
""" Services which will have their tick() function called by
:func:`qtmud.tick`. Populated by :func:`qtmud.load` to contain instances of
the classes in :mod:`qtmud.services` referenced by class name. """
connected_clients = list()

logging.basicConfig(filename='debug.log', filemode='w',
                    format='%(asctime)s %(name)-12s %(levelname)-8s '
                           '%(message)s',
                    datefmt='%m-%d %H:%M',
                    level=logging.DEBUG)
console = logging.StreamHandler()
console.setLevel(logging.INFO)
console.setFormatter(
    logging.Formatter('%(name)-12s %(levelname)-8s %(message)s'))
log = logging.getLogger(NAME)
""" An instance of :class:`logging.Logger`, intended to be used as the main
logger for qtmud and the mudlib, called through `qtmud.log`."""
log.addHandler(console)


def load():
    """ Most importantly, puts every function from
    :mod:`qtmud.subscriptions` and every class from :mod:`qtmud.services`
    into :attr:`subscribers` and :attr:`active_services`, respectively.

    After populating `subscribers` and `active_services`, calls the start()
    method for each class in `active_services`, then attempts to load
    :attr:`MUDLIB`, if one is specified, and finally calls
    :func:`load_client_accounts`.
    """
    global active_services
    global client_accounts
    global console
    global log
    global subscribers
    #####
    #
    # load qtmud subscriptions and start() services
    #
    #####
    log.info('qtmud.load() called')
    log.info('adding qtmud.subscriptions to qtmud.subscribers')
    subscribers = {s[1].__name__: [s[1]] for
                    s in getmembers(subscriptions) if isfunction(s[1])}
    log.info('adding qtmud.services to qtmud.active_services')
    active_services = {t[1].__name__.lower(): t[1]() for
                        t in getmembers(services) if isclass(t[1])}
    log.info('qtmud.load()ed')
    #####
    #
    # load client accounts
    #
    #####
    if load_client_accounts():
        log.debug('qtmud.client_accounts populated from '
                  'qtmud.load_client_accounts()')
        pass
    log.debug('qtmud.load() finished, subscribers and active_services to '
              'follow.')
    log.debug('subscribers are: %s', ', '.join(subscribers))
    log.debug('active_services are: %s',
              ', '.join([s for s in active_services]))
    return True


def load_client_accounts(file=CLIENT_ACCOUNT_FILE):
    """ Populates :attr:`qtmud.client_accounts` with the pickle file
    specified. """
    global client_accounts
    log.debug('filling qtmud.client_accounts from %s', file)
    try:
        client_accounts = pickle.load(open(file, 'rb'))
        log.debug('qtmud.client_accounts filled from %s', file)
        return True
    except FileNotFoundError:
        log.debug('no save file found, making one at %s', file)
        pickle.dump({}, open(file, 'wb'))
        return False


def new_client_account(name, password, birthtime=None):
    """ Create a new client account in :attr:`client_accounts`"""
    client_accounts[name.lower()] = {'name': name,
                            'password': password}
    if birthtime:
        client_accounts[name]['birthtime'] = birthtime
    log.debug('made the new client %s', name)
    save_client_accounts()
    return client_accounts[name]


def new_thing(**kwargs):
    """ Creates a new thing with an identity from :func:`uuid.uuid4()`, and
    adds its identity as a key to :attr:`qtmud.things` with the thing itself
    as the value.
    """
    # TODO allow arguments and call thing.update(arguments)
    while True:
        identity = uuid.uuid4()
        if identity not in things.keys():
            break
    thing = Thing(identity)
    things[identity] = thing
    thing.update(kwargs)
    return thing


def run():
    """ main loop """
    log.info('qtmud.run()ning')
    try:
        while True:
            tick()
    except KeyboardInterrupt:
        log.info('shutdown started')
        schedule('shutdown')
        tick()


def save_client_accounts(file=CLIENT_ACCOUNT_FILE):
    global client_accounts
    log.debug('saving client_accounts')
    try:
        pickle.dump(client_accounts, open(file, 'wb'))
        return True
    except Exception as err:
        log.debug('failed to save client_accounts')
        return False


def schedule(sub, **payload):
    """ Schedules a call to sub with payload passed as parameters.
    """
    if not subscribers.get(sub, []):
        log.warning('Tried to schedule a %s event, no subscribers '
                          'listen to it though.', sub)
        return False
    for method in subscribers.get(sub, []):
        if method not in events:
            events[method] = []
        events[method].append(payload)
    return True


def search_connected_clients_by_name(name):
    return [connected_clients[connected_clients.index(c)] for c in
            connected_clients
            if hasattr(c, 'name') and c.name.lower() == name.lower()]


def search_client_accounts_by_name(name):
    return [c for c in client_accounts.keys() if c.lower() == name.lower()]


def start():
    log.info('start()ing active_services')
    for service in active_services:
        if active_services[service].start():
            log.info('%s start()ed', service)
            pass
        else:
            log.warning('%s failed to start()', service)
    return True

def tick():
    global events
    if events:
        current_events = events
        events = dict()
        for event in current_events:
            for call in current_events[event]:
                log.debug('%s event: %s', event.__name__, call)
                event(**call)
    for service in active_services:
        active_services[service].tick()
    return True


class Thing(object):
    """ Most objects clients interact with are Things

        :param identity: a UUID as created by :func:`uuid.uuid4()`

        Created with :func:`new_thing`, things are objects with a few
        attributes added on, mostly for enabling in-game reference of the
        objects.
    """
    def __init__(self, identity):
        self._name = str()
        self.identity = identity
        """ Passed by :func:`new_thing`, `identity` is stored as a UUID """
        self.nouns = {'thing'}
        """ `nouns` represent lower-case nouns which may be used to reference
            the thing.
        """
        self.name = str(identity)
        self.adjectives = set()
        self.qualities = []
        return

    @property
    def name(self):
        """ Properly-cased full name of a thing
            Any name a thing is given is also added to :attr:`Thing.nouns`,
            with the old name being removed. Same for adjectives.

            .. warning:: This has some wonkiness, in that "Eric Baez" can be
                         referred to as "Eric Baez" or "Baez" but not "Eric".
                         "Eric Thing" would work, though.
        """
        return self._name

    @name.setter
    def name(self, value):
        old_name = self._name.lower().split(' ')
        if len(old_name) > 1:
            old_adjectives = old_name[0:-1]
            for adjective in old_adjectives:
                try:
                    self.adjectives.remove(adjective)
                except KeyError:
                    pass
        try:
            self.nouns.remove(old_name[-1])
        except KeyError:
            pass
        new_name = value.lower().split(' ')
        self.nouns.add(new_name[-1])
        if len(new_name) > 1:
            adjectives = new_name[0:-1]
            for adjective in adjectives:
                self.adjectives.add(adjective)
        self.nouns.add(new_name[-1])
        self._name = value

    def update(self, attributes):
        """ Update multiple attributes of Thing at once.

            Example:
                >>> foo = new_thing()
                >>> foo.update({'name': 'eric'})
                >>> foo.name
                eric

            .. warning:: Does not properly recognize setters
        """
        # todo account for custom setters
        for attribute, value in attributes.items():
            self.__dict__[attribute] = value
        return True
