""" build objects for in-game interaction

    .. versionadded 0.0.4

    This module houses the methods for building things, and generating
    non-thing in-game objects. In this context, a thing refers to an instance
    of :class:`qtmud.Thing.`
"""
import random
import string
import types
from inspect import getmembers, isfunction

import qtmud
from mudlib.starhopper import cmds, txt


def build_planet(basis: object = None, system=None, distance=None,
                 points = None):
    """ creates a planet

    :param basis: expected to be a :class:`qtmud.Thing`
    :param system: the system the planet will live in
    :param distance: the distance from the system's sun
    :param points: how many points can be spent building the system.
    :return: an object which behaves like a planet

    Is `basis` is passed, the planet is built upon that object - which is
    expected to be an instance of :class:`qtmud.Thing`. If basis is not passed,
    the method creates a new object with :func:`qtmud.new_thing`.

    +-----------+------------------------------+-----------+----------------+
    | attribute | meaning                      | example   |                |
    +===========+==============================+===========+================+
    | klass     | Star Trek-style planet class | M Klass   | survey results |
    +-----------+------------------------------+-----------+----------------+
    | name      | SciFi-style planet name     | Omicron 6 | aesthetic       |
    +-----------+-----------------------------+-----------+-----------------+
    """
    # TODO planets have scenarios
    # TODO klass influences planet scenarios
    # TODO klass based on distance from sun.
    if basis:
        planet = basis
    else:
        planet = qtmud.new_thing()
    planet.nouns.add('planet')
    planet.klass = '{}'.format(random.choice([l for l
                                              in string.ascii_uppercase]))
    return planet


def build_rat(points=1):
    rat = build_ship()
    rat.nouns.update(['pirate', 'rat', 'scum', 'mob'])
    rat.local_system = None
    if random.choice([True, False, False, False]):
        rat.name = random.choice(txt.RAT_NAMES)
    else:
        rat.name = generate_rat_name()
    rat.aggressive = True
    return rat


def build_ship(client=None, points=10):
    if not client:
        ship = qtmud.new_thing()
    else:
        ship = client
        for command, function in [m for m in getmembers(cmds) if isfunction(m[1])]:
            ship.commands[command] = types.MethodType(function, ship)
    ship.local_system = None
    ship.model = random.choice(['Firefly', 'Petunia', 'Imperial Deathbat'])
    ship.battery = [10, 10]
    ship.damage = [0, 10]
    ship.salvage = [0, 10]
    ship.attack = [6, 2]
    ship.defense = 2
    ship.score = 0
    return ship


def build_star():
    # TODO star klass should affect description
    # TODO star klass should affect planet generation
    star = qtmud.new_thing()
    star.nouns.update(['sun', 'star'])
    star_types = ['O', 'B', 'A', 'F', 'G', 'K', 'M']
    star.klass = '{}{}'.format(random.choice(star_types),
                               random.choice(range(9)))
    return star


def build_station(difficulty=1):
    station = qtmud.new_thing()
    station.nouns.update(['station', 'store'])
    station.inventory = []
    for upgrade in range(random.randrange(4)):
        station.inventory.append(generate_upgrade(difficulty))
    return station


def build_system(difficulty=1):
    system = qtmud.new_thing()
    system.points=difficulty
    system.difficulty = difficulty
    system.name = generate_system_name()
    system.neighbors = dict()
    # build sun
    system.sun = build_star()
    # build planets
    system.planets = set()
    for count in range(random.randrange(6)):
        planet = build_planet(system=system, distance=count)
        planet.name = '{} {}'.format(system.name, count)
        system.planets.add(planet)
    # populate with ships
    system.ships = set()
    for count in range(random.randrange(system.difficulty)):
        pirate = build_rat(system.difficulty)
        pirate.local_system = system
        system.ships.add(pirate)
    # populate with debris
    system.debris = set()
    # make a station
    if random.choice([True, False, False]):
        system.station = build_station()
    # build exits
    return system


def build_wreck(ship=None):
    if not ship:
        ship = build_ship()
    ship.name = 'wreck of {}'.format(ship.model)
    return ship


def generate_system_name():
    start_sounds = list(set(string.ascii_lowercase) - {'aeiou'}
                        - {'qxc'}
                        | {'bl', 'br', 'cl', 'cr', 'dr', 'fl', 'fr', 'gl',
                           'gr', 'pl', 'pr', 'sk', 'sl', 'sm', 'sn', 'sp',
                           'st', 'str', 'sw', 'tr', 'ch', 'sh'})
    end_sounds = list(set(string.ascii_lowercase) - {'aeiou'}
                      - {'qxcsj'}
                      | {'ct', 'ft', 'mp', 'nd', 'ng', 'nk', 'nt', 'pt',
                         'sk', 'sp', 'ss', 'st', 'ch', 'sh'})
    vowels = 'aeiou'
    return ''.join(random.choice(s) for s in (start_sounds, vowels,
                                              end_sounds)).capitalize()

def generate_rat_name():
    if random.choice([True, False]):
        return random.choice(txt.RAT_NAMES)
    else:
        start_sounds = ['oo', 'uo', 'ou', 'eo', 'u', 'oe', 'ue', 'eu']
        end_sounds = ['ra', 'la', 'ba', 'mar', 'il']
        break_sounds = 'ktpdb'
        return ''.join(random.choice(s) for s in (start_sounds, break_sounds,
                                                  end_sounds)).capitalize()


def generate_upgrade(difficulty=1):
    if random.choice([True, False]):
        upgrade = ['charge', difficulty, difficulty]
    elif random.choice([True, False]):
        upgrade = ['battery', difficulty, difficulty]
    elif random.choice([True, False]):
        upgrade = ['attack', difficulty, difficulty, difficulty]
    else:
        upgrade = ['defense', difficulty, difficulty]
    return upgrade