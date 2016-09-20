""" Gives the ability to use swords

    .. moduleauthor:: emsenn <morgan.sennhauser@gmail.com>

    .. versionadded:: 0.0.3-feature/learning
    .. versionchanged:: 0.0.3-feature/diceroller
        added Swordsmanship, changed Violent
"""


import types

from qtmud.services import Parser

class Violent(object):
    """ lets a thing fight.

        .. versionadded:: 0.0.3-feature/learning
    """

    def __init__(self):
        """
            .. versionadded:: 0.0.3-feature/learning
        """
        return

    @staticmethod
    def fight(attacker, line):
        """ fight the subject of line

            .. versionadded:: 0.0.3-feature/learning
        """
        line = Parser.parse_line(attacker, line)
        if 'subject' in line:
            combatants = attacker.search(line['subject'])
            if combatants:
                if len(combatants) == 1:
                    defender = combatants[0]
                    if hasattr(defender, 'health'):
                        attacker.manager.schedule('fight',attacker=attacker,
                                                         defender=defender)
                        if hasattr(attacker, 'send'):
                            attacker.manager.schedule('send', thing=attacker,
                                                      scene = ('You start to '
                                                               'attack.'))
                        if hasattr(defender, 'send'):
                            defender.manager.schedule('send', thing=defender,
                                                      scene = ('You are '
                                                               'attacked.'))
                        return True
                    else:
                        scene = 'You cannot attack that thing.'
                elif len(combatants) > 1:
                    scene = 'You targeted too many things, try more adjectives.'
            else:
                scene = 'syntax: attack <thing>'
        else:
            scene = 'Can\'t find what you wanted to attack.'
        attacker.manager.schedule('send', thing=attacker, scene=scene)
        return True

    def apply(self, thing):
        """
            .. versionadded:: 0.0.3-feature/learning
            .. versionchanged:: 0.0.3-feature/diceroller
                added actions dict and skill levels.
        """
        thing.manager.add_qualities(thing, [Acting])
        thing.actions['fight'] = [2, 1, ('You attack {}','{} attacks you')]
        thing.attacks = {'fight'}
        if not hasattr(thing, 'fight'):
            thing.fight = types.MethodType(self.fight, thing)
        if hasattr(thing, 'commands'):
            thing.commands['fight'] = types.MethodType(self.fight, thing)
            thing.commands['attack'] = types.MethodType(self.fight, thing)
        return thing


class Swordsmanship(object):
    """ lets a thing use a sword

        .. versionadded:: 0.0.3-feature/learning
    """

    def __init__(self):
        """
            .. versionadded:: 0.0.3-feature/learning
        """
        self.swordsmanship = 1

    def stab(self, stabber, line):
        return stabber.fight(line)

    def slash(self, slasher, line):
        return slasher.fight(line)

    def parry(self, parryer, line):
        return parryer.fight(line)

    def apply(self, thing):
        thing.manager.add_qualities(thing, [Violent])
        if not hasattr(thing, 'stab'):
            thing.stab = types.MethodType(self.stab, thing)
            thing.actions['stab'] = [3, 2, ('You stab {}', '{} stabs you')]
            thing.attacks.add('stab')
        if not hasattr(thing, 'slash'):
            thing.slash = types.MethodType(self.slash, thing)
        if not hasattr(thing, 'parry'):
            thing.parry = types.MethodType(self.parry, thing)
        if hasattr(thing, 'commands'):
            thing.commands['stab'] = types.MethodType(self.stab, thing)
            thing.commands['slash'] = types.MethodType(self.slash, thing)
            thing.commands['parry'] = types.MethodType(self.parry, thing)
        return thing


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