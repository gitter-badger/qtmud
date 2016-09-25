import random
import string
import types

from inspect import getmembers, isfunction


import qtmud
from mudlib.starhopper import cmds, txt
command_list = [m for m in getmembers(cmds) if isfunction(m[1])]



def build_planet():
    planet = qtmud.new_thing()
    planet.nouns.add('planet')
    planet.klass = '{}'.format(random.choice([l for l
                                              in string.ascii_uppercase]))
    return planet

def build_rat(difficulty=1):
    rat = qtmud.new_thing()
    rat.nouns.update(['ship', 'pirate', 'rat', 'scum', 'mob'])
    rat.local_system = None
    # TODO: rat_name_generator()
    rat.name = random.choice(txt.RAT_NAMES)
    rat.attack= [difficulty, difficulty]
    rat.defense = difficulty
    rat.battery=[difficulty, difficulty]
    rat.damage= [0, difficulty]
    rat.salvage = [random.randrange(difficulty), difficulty]
    rat.aggressive = True
    rat.immortal = True
    return rat


def build_ship(client=None):
    if not client:
        ship = qtmud.new_thing()
    else:
        ship = client
        for command, function in command_list:
            ship.commands[command] = types.MethodType(function, ship)
    ship.local_system = None
    ship.battery = [10, 10]
    ship.damage = [0, 10]
    ship.salvage = [0, 10]
    ship.attack = [6, 2]
    ship.defense = 2
    return ship


def build_star():
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
    system.difficulty = difficulty
    system.adjacent = dict()
    system.name = generate_system_name()
    system.sun = build_star()
    system.sun.name = 'Stellar Object {}'.format(system.name)
    system.planets = set()
    system.ships = set()
    system.debris = set()
    planet_count = random.randrange(12)
    for count in range(planet_count):
        planet = build_planet()
        planet.name = '{} {}'.format(system.name, count)
        system.planets.add(planet)
    has_station = random.choice([True, False, False])
    if has_station:
        system.station = build_station()
    for count in range(random.randrange(system.difficulty)):
        pirate = build_rat(system.difficulty)
        pirate.local_system = system
        system.ships.add(pirate)
    return system


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