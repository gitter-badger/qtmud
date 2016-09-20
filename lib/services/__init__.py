"""

    .. moduleauthor: Morgan Sennhauser <morgan.sennhauser@gmail.com>

    .. versionadded:: 0.0.3-feature/diceroller
"""

import random

#from qtmud.lib.services import Diceroller

class Fighter(object):
    def __init__(self, manager):
        """
            .. versionadded:: 0.0.3-feature/diceroller
        """
        self.manager = manager
        self.subscriptions = ['fight']

    def tick(self, events=False):
        """
            .. versionadded:: 0.0.03-feature/diceroller

        """
        if events is False:
            return False
        for event, payload in events: #pylint: disable=unused-variable
            attacker = payload['attacker']
            defender = payload['defender']
            affordable_atks = []
            affordable_defs = []
            # Find our attack
            for attack in attacker.attacks:
                if attack in attacker.actions:
                    if attacker.actions[attack][0] < attacker.action_points[0]:
                        affordable_atks.append(attack)
            if affordable_atks:
                attack = random.choice(affordable_atks)
            else:
                attack = None
            # Find our defense
            if hasattr(defender, 'defenses'):
                for defense in defender.defenses:
                    if defense in defender.defenses:
                        if defender.actions[defense][0] < defender.action_pints[0]:
                            affordable_defs.append(defense)
                if affordable_defs:
                    defense = random.choice(affordable_defs)
                    defense_cost = defender.actions[defense][0]
                else:
                    defense, defense_cost = None, None
            else:
                defense, defense_cost = None, None
            # line up the attack
            if attack:
                # This build us toward a dice roller - that's what
                # attacker.actions[attack][1] is meant to represent, the dice
                # that skill adds to your pool.
                damage = attacker.actions[attack][1]
                attacker.action_points[0] = attacker.action_points[
                                                0]-attacker.actions[attack][0]
                if hasattr(attacker, 'send'):
                    attacker.manager.schedule('send',thing=attacker,
                                            scene=attacker.actions[attack][
                                                2][0].format(defender.name))
                if hasattr(defender, 'send'):
                    defender.manager.schedule('send', thing=defender,
                                              scene=attacker.actions[
                                                  attack][2][1].format(
                                                      attacker.name))
                if defense:
                    damage = damage-defender.actions[defense][1]
                    defender.action_points[0] = defender.action_points[
                                                    0]-defender.actions[
                        defense][0]
                    if hasattr(defender, 'send'):
                        defender.manager.schedule('send',thing=defender,
                                                  scene=defender.actions[
                                                      defense][2][0].format(
                                                          attacker.name))
                    if hasattr(attacker, 'send'):
                        attacker.manager.schedule('send',thing=attacker,
                                                  scene=attacker.actions[
                                                      attack][2][1].format(
                                                              defender.name))
                if damage > 0:
                    defender.health_points[0] = defender.health_points[0]-damage
                    attack_dmg_scene = ('You did {} points of damage to '
                                        '{}'.format(damage, defender.name))
                    defense_dmg_scene = ('{} did {} points of damage to you, '
                                        'so now you have {}/{} health '
                                         'points.'.format(attacker.name,
                                                          damage,
                                                          defender.health_points[0],
                                                          defender.health_points[1]))
                    if hasattr(attacker, 'send'):
                        attacker.manager.schedule('send',thing=attacker,
                                                  scene=attack_dmg_scene)
                    if hasattr(defender, 'send'):
                        defender.manager.schedule('send',
                                                  thing=defender,
                                                  scene=defense_dmg_scene)
                    if defender.health_points[0] < 0:
                        defender.manager.schedule('death', departed=defender)
                        if hasattr(defender, 'send'):
                            defender.manager.schedule('send', thing=defender,
                                                      scene='you died')
                        attacker.manager.schedule('send', thing=attacker,
                                                  scene='you killed it')
            else:
                pass
                # no affordable attack
        return True
