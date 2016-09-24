import random
import string


import qtmud
from mudlib.starhopper import rat


def generate_name():
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


def generate_planet():
    planet = qtmud.new_thing()
    planet.nouns.add('planet')
    planet.klass = '{}'.format(random.choice([l for l
                                              in string.ascii_uppercase]))
    return planet


def generate_star():
    star = qtmud.new_thing()
    star.nouns.update(['sun', 'star'])
    star_types = ['O', 'B', 'A', 'F', 'G', 'K', 'M']
    star.klass = '{}{}'.format(random.choice(star_types),
                               random.choice(range(9)))
    return star


def generate_station():
    station = qtmud.new_thing()
    station.nouns.update(['station', 'store'])
    return station

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

def generate_system(difficulty=1):
    system = qtmud.new_thing()
    system.difficulty = difficulty
    system.adjacent = dict()
    system.name = generate_name()
    system.sun = generate_star()
    system.sun.name = 'Stellar Object {}'.format(system.name)
    system.planets = set()
    system.ships = set()
    system.debris = set()
    planet_count = random.randrange(12)
    for count in range(planet_count):
        planet = generate_planet()
        planet.name = '{} {}'.format(system.name, count)
        system.planets.add(planet)
    has_station = random.choice([True, False])
    if has_station:
        station = qtmud.new_thing()
        station.inventory = []
        for good in range(random.randrange(4)):
            station.inventory.append(generate_upgrade(difficulty))
        system.station = station
    for count in range(random.randrange(system.difficulty)):
        pirate = rat.new_rat(system.difficulty)
        pirate.local_system = system
        system.ships.add(pirate)
    return system