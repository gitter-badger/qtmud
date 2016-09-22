""" Gives the ability to use swords

    .. moduleauthor:: emsenn <morgan.sennhauser@gmail.com>

    .. versionadded:: 0.0.3-feature/learning
    .. versionchanged:: 0.0.3-feature/diceroller
        added Swordsmanship, changed Violent
"""

# system imports
import types, random

# qtmud imports
from qtmud.services import Parser
from qtmud.qualities import Container, Physical, Renderable, Room, Noisy

# library imports
from qtmud.lib.yeolderpg.services import Diceroller

class Place(object):
    """ A normal place in Ye Olde RPG

        .. versionadded:: 0.0.3-feature/diceroller
    """

    def __init__(self):
        """
            .. versionadded:: 0.0.3-feature/diceroller
        """

    def apply(self, thing):
        place = thing.manager.add_qualities(thing,
                                            [Container, Renderable, Room,
                                             Noisy])
        return place

class NPC(object):
    def __init__(self):
        return

    def apply(self, thing):
        npc = thing.manager.add_qualities(thing,
                                          [Container, Physical, Renderable,
                                           Noisy])
        return npc


class Acting(object):
    """ gives a thing action points

        .. versionadded:: 0.0.3-feature/diceroller
    """

    def __init__(self):
        """
            .. versionadded:: 0.0.3-feature/diceroller
        """
        self.action_points = [10, 10]
        self.actions = dict()

    def apply(self, thing):
        if not hasattr(thing, 'action_points'):
            thing.action_points = self.action_points
        if not hasattr(thing, 'skills'):
            thing.actions = self.actions
        return thing


class Healthful(object):
    """ gives a thing health

        .. versionadded:: 0.0.3-feature/diceroller
    """

    # TODO: custom setter for health_points
    # if they're going to be less than 0, die
    def __init__(self):
        """
            .. versionadded:: 0.0.3-feature/diceroller
        """
        self.health_points = [2, 2]

    def health(self, thing, line):
        thing.manager.schedule('send',
                               thing=thing,
                               scene = ('You have {} of {} health points.'
                                        ''.format(thing.health_points[0],
                                                  thing.health_points[1])))

    def apply(self, thing):
        if not hasattr(thing, 'health_points'):
            thing.health_points = self.health_points
        if not hasattr(thing, 'health'):
            thing.health = types.MethodType(self.health, thing)
        if hasattr(thing, 'commands'):
            thing.commands['health'] = types.MethodType(self.health, thing)
        return thing


class Loot(object):
    """
        .. versionadded:: 0.0.3-feature/diceroller
    """

    def __init__(self):
        return

    def apply(self, thing):
        thing = thing.manager.add_qualities(thing, [Physical, Renderable])
        thing.name = 'some loot'
        thing.description = ('some loot you got for killing something. i hope '
                             'you feel good about yourself.')
        return thing


class Dodger(object):

    def __init__(self):
        return

    def apply(self, thing):
        if not hasattr(thing, 'actions'):
            thing = thing.manager.add_qualities(thing, [Acting])
        thing.actions['dodge'] = [3, 2]
        if not hasattr(thing, 'defenses'):
            thing.defenses = set()
        thing.defenses.add('dodge')
        if hasattr(thing, 'commands'):
            thing.commands['dodge'] = types.MethodType(self.dodge, thing)
        return thing