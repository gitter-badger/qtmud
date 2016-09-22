""" space exploration rpg

    .. moduleauthor:: 0.0.3-feature/diceroller

    .. versionadded:: 0.0.3-feature/diceroller
"""

import string
import random

import qtmud
from qtmud.qualities import Container, Physical, Renderable, Room

qtmud.systems = set()

class StarSystem(object):
    def __init__(self):
        return

    def generate_name(self, system):
        """ generate system names
        """
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

    def generate_description(self, system):
        scene = 'This star system '

    def apply(self, thing):
        system = thing.manager.add_qualities(thing, [Container, Renderable,
                                                     Room])
        system.name = self.generate_name(system)
        planet_count = random.randrange(12)
        for count in range(planet_count):
            planet = system.manager.new_thing(Planet)
            planet.name = self.generate_name(planet)
            if count < 4:
                planet.description = 'This planet is a barren wasteland.'
            if count == 4:
                planet.description = 'This planet might be habitable.'
            if count > 4:
                planet.description = 'This planet is a frozen wasteland.'
            system.add(planet)
        qtmud.systems.add(system)
        return system

class Planet(object):
    def __init__(self):
        return

    def apply(self, thing):
        planet = thing.manager.add_qualities(thing, [Container, Physical,
                                                     Renderable])
        return planet