""" The main qtmud module houses some constants, the Thing class, and methods
    for start()ing and tick()ing the MUD engine.
"""

import logging
import uuid
from inspect import getmembers, isfunction, isclass
from qtmud import services, subscriptions, txt


NAME = 'qtmud'
""" Name of the MUD engine. """
VERSION = '0.0.4'
""" MUD engine version """
SPLASH = txt.SPLASH.format(**locals())
""" Text new clients see, filled out from :attr:`txt.SPLASH`"""


events = dict()
""" events scheduled to occur next tick, populated by :func:`schedule`"""
things = dict()
""" all the things that new_thing() has made"""
subscribers = dict()
""" methods registered as qtmud events """
active_services = dict()
""" services to be tick()ed """


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
""" An instance of :class:`logging.Logger`"""
log.addHandler(console)


def start():
    """ Most importantly, loads every function from
    :mod:`qtmud.subscriptions` and every class from :mod:`qtmud.services`
    into :attr:`subscribers` and :attr:`active_services`, respectively.

    Also sets up
    """
    global subscribers
    global active_services
    global log
    global console
    subscribers = {s[1].__name__: [s[1]] for
                    s in getmembers(subscriptions) if isfunction(s[1])}
    active_services = {t[1]: t[1]() for
                        t in getmembers(services) if isclass(t[1])}


def new_thing():
    """ Creates a new thing with an identity from :func:`uuid.uuid4()`, and
    adds its identity as a key to :attr:`qtmud.things` with the thing itself
    as the value.
    """
    while True:
        identity = uuid.uuid4()
        if identity not in things.keys():
            break
    thing = Thing(identity)
    things[identity] = thing
    return thing


def schedule(sub, **payload):
    for method in subscribers.get(sub, []):
        if method not in events:
            events[method] = []
        events[method].append(payload)
    return True


def search_by_noun(reference, adjectives, search_noun):
    matches = []
    if hasattr(reference, 'contents'):
        for content in reference.contents:
            for noun in content.nouns:
                if noun == search_noun:
                    matches.append(content)
    if hasattr(reference, 'location'):
        for content in reference.location.contents:
            for noun in content.nouns:
                if noun == search_noun:
                    matches.append(content)
        for noun in reference.location.nouns:
            if noun == search_noun:
                matches.append(reference.location)
    if adjectives:
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


def tick():
    global events
    if events:
        current_events = events
        events = dict()
        for event in current_events:
            for call in current_events[event]:
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
        for attribute, value in attributes.items():
            self.__dict__[attribute] = value
        return True
