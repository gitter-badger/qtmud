""" Builders for in-game things.

    The methods in this module create in-game :class:`things <qtmud.Thing>` and
    provide supporting functionality.

    Methods which start with `build_` are used to create things, while methods
    which start with `generate_` create other information.
"""
import random
import string
import types
from inspect import getmembers, isfunction

import qtmud
from mudlib.starhopper import cmds, txt



def build_captain(client):
    captain = client
    for command, function in [m for m in getmembers(cmds) if isfunction(m[1])]:
        captain.commands[command] = types.MethodType(function, captain)
    captain.score = 0
    return captain

def build_planet(basis: object = None, system=None, distance=None,
                 points=0):
    if basis:
        planet = basis
    else:
        planet = qtmud.new_thing()
    planet.nouns.add('planet')
    planet.klass = 'foo'
    planet.name = '{system.name} {distance}'.format(**locals())
    system.points -= points
    planet.points = points
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


def build_frigate(ship=None):
    if not ship:
        ship = qtmud.build_ship()
    ship.klass = 'frigate'
    frigate = ship
    return frigate


def build_ship(client=None, points=10):
    ship = qtmud.new_thing()
    if client:
        ship.captain = client
    ship = build_frigate(ship=ship)
    ship.local_system = None
    ship.model = random.choice(['Firefly', 'Petunia', 'Imperial Deathbat'])
    ship.charge = 0
    ship.battery = 10
    ship.health = 10
    ship.damage = 10
    ship.salvage = [0, 10]
    ship.attack = [6, 2]
    ship.defense = 2
    ship.score = 0
    return ship


def build_star(system=None):
    """

    :param system: expected to be a :class:`qtmud.Thing>`
    :return:
    +-----------+------------------------------+-----------+----------------+
    | attribute | meaning                      | example   | affects        |
    +===========+==============================+===========+================+
    | klass     | Harvard-style classification | M3 Klass  | planet types   |
    +-----------+------------------------------+-----------+----------------+
    """
    star = qtmud.new_thing()
    star.nouns.update(['sun', 'star'])
    star.klass = [random.choice(['M', 'K', 'G', 'F', 'A', 'B', 'O']),
                  random.choice(range(9))]
    if system:
        if star.klass[0] in ['O', 'B', 'A', 'M']:
            system.points -= 20+star.klass[1]
        elif star.klass[0] in ['F', 'K']:
            system.points += star.klass[1]
        elif star.klass[1] in ['G']:
            system.points += 20+star.klass[1]
    return star


def build_station(difficulty=1):
    station = qtmud.new_thing()
    station.nouns.update(['station', 'store'])
    station.inventory = []
    for upgrade in range(random.randrange(4)):
        station.inventory.append(generate_upgrade(difficulty))
    return station


def build_planets(system=None):
    planets = list()
    if system:
        try:
            for count in range(random.randrange(int(system.points/20),
                                                int(system.points/10))):
                investment = random.randrange(9)
                planets.append(build_planet(system=system,points=investment,
                                            distance=count))
        except ValueError:
            pass
    else:
        for count in range(random.randrange(4)):
            planets.append(build_planet(system=system))
    return planets

def build_system(points=100, difficulty=1):
    qtmud.log.info('building new system')
    system = qtmud.new_thing()
    system.points = points
    system.difficulty = difficulty
    system.name = generate_system_name()
    system.star = build_star(system=system)
    system.planets = build_planets(system=system)
    system.ships = set()
    system.debris = set()
    system.neighbors = dict()
    qtmud.log.info('built %s system, %s points unspent', system.name,
                   system.points)
    return system


def build_wreck(ship=None):
    if not ship:
        ship = build_ship()
    ship.name = 'wreck of {}'.format(ship.model)
    return ship


def generate_backstory(ship):
    return '{}\n{}\n{}\n{}'.format(random.choice(txt.EXODUS_BACKSTORIES).format(
                               **locals()),
                               txt.INTERIM_BACKSTORY,
                               random.choice(txt.CAPTAIN_BACKSTORIES).format(
                               **locals()),
                               txt.END_BACKSTORY)


def generate_survey(planet):
    output = ('Planetary Survey of {planet.name}\n'
              '{planet.name} is a {planet.klass} klass planet. It has '
              '{planet.points} invested in it.')

    return output.format(**locals())


def generate_status(ship):
    output = ('You\'re flying a {ship.model}, which is a {ship.klass}.\n'
              'Your capacitor has {ship.charge} out of {ship.battery}.\n'
              'You can tolerate {ship.health} damage, and '
              'has taken {ship.damage}.\n'
              'Your attacks cost {ship.attack[1]} and do {ship.attack[0]} '
              'damage. Your ship has {ship.defense} defense.\n')

    return output.format(**locals())


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