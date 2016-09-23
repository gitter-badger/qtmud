import random
import string

import qtmud
from lib import starhopper


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


def apply(thing):
    system = thing
    system.name = generate_name()
    planet_count = random.randrange(12)
    for count in range(planet_count):
        planet = qtmud.new_thing()
        planet.name = generate_name()
        if count < 4:
            planet.description = 'This planet is a barren wasteland.'
        if count == 4:
            planet.description = 'This planet might be habitable.'
        if count > 4:
            planet.description = 'This planet is a frozen wasteland.'
        system.add(planet)
    starhopper.systems.add(system)
    return system
