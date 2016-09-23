import random
import string
import types

import qtmud
from mudlib import starhopper


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
                                              end_sounds))

def generate_star():
    star = qtmud.new_thing()
    star_types = ['O', 'B', 'A', 'F', 'G', 'K', 'M']
    star.klass = '{}{}'.format(random.choice(star_types),
                               random.choice(range(9)))
    return star

def apply(thing):
    system = thing
    system.name = generate_name()
    system.sun = generate_star()
    system.planets = set()
    planet_count = random.randrange(12)
    for count in range(planet_count):
        planet = qtmud.new_thing()
        planet.name = '{} {}'.format(system.name, count)
        planet.nouns.add('planet')
        if count < 4:
            planet.description = 'This planet is a barren wasteland.'
        if count == 4:
            planet.description = 'This planet might be habitable.'
        if count > 4:
            planet.description = 'This planet is a frozen wasteland.'
        system.planets.add(planet)
    return system
