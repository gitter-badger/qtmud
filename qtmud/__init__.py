import logging
import uuid


NAME = 'qtmud'
VERSION = '0.0.3'

SPLASH = ('{}\n    version {}\n\nPlease input [desired] name'.format(NAME,
                                                                     VERSION))


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
log = logging.getLogger('qtmud')
log.addHandler(CONSOLE)


events = dict()
things = dict()
subscriptions = dict()


def new_thing():
    while True:
        identity = uuid.uuid4()
        if identity not in things.keys():
            break
    thing = Thing(identity)
    things[identity] = thing
    return thing


def schedule(sub, **payload):
    for method in subscriptions.get(sub, []):
        if method not in events:
            events[method] = []
        events[method].append(payload)
    return True


def search_by_line(searcher, objekt=None, adjectives=None, pnp_clauses=None,
                   verb=None):
    matches = []
    reference = searcher
    if objekt is not None:
        if pnp_clauses is not None:
            pnp_clauses.reverse()
            for clause in pnp_clauses:
                if clause[0] in ['from', 'in', 'on']:
                    references = search_by_nametag(reference,
                                                        clause[1],
                                                        clause[2])
                    if len(references) != 1:
                        return references
                    reference = references[0]
        matches = search_by_noun(reference,
                                 adjectives,
                                objekt)
    return matches


def search_by_noun(reference, adjectives, noun):
    matches = []
    print(noun)
    if hasattr(reference, 'contents'):
        for content in reference.contents:
            for nametag in content.nametags:
                if nametag == noun:
                    matches.append(content)
    if hasattr(reference, 'location'):
        for content in reference.location.contents:
            print(content.nametags)
            for nametag in content.nametags:
                if nametag == noun:
                    matches.append(content)
        for nametag in reference.location.nametags:
            if nametag == noun:
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


def subscribe(*methods):
    for method in methods:
        name = method.__name__
        if name not in subscriptions:
            subscriptions[name] = []
        subscriptions[name].append(method)
    return True


class Thing(object):
    def __init__(self, identity):
        self._name = str()
        self.identity = identity
        self.nametags = {'thing'}
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
            self.nametags.remove(old_name[-1])
        except KeyError:
            pass
        new_name = value.lower().split(' ')
        self.nametags.add(new_name[-1])
        if len(new_name) > 1:
                adjectives = new_name[0:-1]
                for adjective in adjectives:
                    self.adjectives.add(adjective)
        self.nametags.add(new_name[-1])
        self._name = value

    def update(self, to_update):
        for attribute, value in to_update.items():
            self.__dict__[attribute] = value
        return True
