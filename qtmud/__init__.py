""" qtmud core methods & Thing

    .. versionadded 0.0.4

    .. warning:: Do not rely on this API! I'm a newbie programmer and changing
                 things all the time.

    Methods for handling the schedule, instancing Things, and looking those
    things back up.
"""

import logging
import uuid
from inspect import getmembers, isfunction, isclass
from qtmud import services, subscriptions, txt

NAME = 'qtmud'
""" Name of the MUD engine. """


VERSION = '0.0.3'
""" MUD engine version """


SPLASH = txt.SPLASH.format(**locals())

events = dict()
""" events scheduled to occur next tick"""


things = dict()
""" all the things that new_thing() has made"""


subscribers = dict({s[1].__name__: [s[1]] for
                    s in getmembers(subscriptions) if isfunction(s[1])})
""" methods registered as qtmud events """
active_services = dict({t[1]: t[1]() for
                        t in getmembers(services) if isclass(t[1])})
""" services to be tick()ed """


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
CONSOLE.setFormatter(logging.Formatter('%(name)-12s %(levelname)-8s %(message)s'))
log = logging.getLogger('qtmud')
""" qtmud's logging handler, see :mod:`logging.Logger`. """
log.addHandler(CONSOLE)


def new_thing():
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
    def __init__(self, identity):
        self._name = str()
        self.identity = identity
        self.nouns = {'thing'}
        self.name = str(identity)
        self.adjectives = set()
        self.qualities = []
        return

    @property
    def name(self):
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
