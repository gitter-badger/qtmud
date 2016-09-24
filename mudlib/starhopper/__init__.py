""" STARHOPPER

    .. versionadded:: 0.0.4

    The basic idea for starhopper gameplay is:

    * Client gets logged in, turned into Ship
    * Ship is put into a star system, which has a sun, planets, and stations -
      stores
    * Ship can "hop" from one system to the next. Each system has a difficulty,
      which increases the further from the starting system you.
    * Pirates spawn in systems, and attack players in that room. Their health
      and attack and such are based on difficulty.
    * Dead pirates can be "salvaged"
    * Salvage can be sold to stations
    * Stations sell upgrades for your ship
    * hop forward and backward, getting bigger and better ship stuff.
"""


import random


import qtmud
from mudlib.starhopper import rat, ship, starsystem


START_LOCATION = starsystem.generate_system()

startup_services = None

STARHOPPER_SPLASH = """
  * S * T * A * R *     * H * O * P * P * E * R *\n\n\n

Welcome to STARHOPPER, one of qtmud's testing libraries.\n
In STARHOPPER, you play a brave starship captain, who is struggling against
incredible odds to make it from Here to There.\n\n

The stellar system you start in is peaceful.\n
"scan" it to take a look around.\n\n

Once you move on, though, you\'ll have to fight space pirates of increasing
difficulty. You can "salvage" their wrecks, and "sell" the salvage to any
stations you come across. Some stations will let you "buy" upgrades,
which you can use to defeat even tougher pirates.\n
"""


def add_client(client):
    """ turn a client into a starship """
    qtmud.log.debug('%s is entering STARHOPPER', client.name)
    player = client
    player = ship.make_ship(player)
    qtmud.schedule('send',
                   recipient=player,
                   text=STARHOPPER_SPLASH)
    qtmud.schedule('hop',
                   ship=player,
                   destination=START_LOCATION)
    return player


def remove_client(client):
    if hasattr(client, 'local_system'):
        client.local_system.ships.remove(client)
    return True


def attack(attacker, defender):
    if attacker.battery[0] <= 0:
        qtmud.schedule('send', recipient=attacker,
                       text='You need more battery.\n')
        return False
    output = ['You are attacked!\n', 'You attack!\n']
    attacker.battery[0] += -(attacker.attack[1])
    damage = attacker.attack[0] - defender.defense
    if damage > 0:
        defender.damage[0] += damage
        output[0] += 'You\'re hit for {} damage\n'.format(damage)
        output[1] += 'You damage {}\n'.format(defender.name)
        if defender.damage[0] >= defender.damage[1]:
            qtmud.schedule('death',
                           departed=defender)
    elif damage == 0:
        output[0] += 'The engagement is a stalemate.\n'
        output[1] += 'The engagement is a stalemate.\n'
    elif damage < 0:
        output[0] += 'Your defenses enable you to counter.\n'
        output[1] += 'Your opponent\'s defense enables them to counter.\n'
        qtmud.schedule('attack', attacker=defender, defender=attacker)
    qtmud.schedule('send', recipient=defender, text=output[0])
    qtmud.schedule('send', recipient=attacker, text=output[1])
    return True
qtmud.subscriptions.add(attack)

def death(departed):
    output = '{} explodes, leaving behind a wreck.\n'.format(departed.name)
    qtmud.schedule('hop', ship=departed, destination=None)
    wreck = qtmud.new_thing()
    wreck.name = 'wreck of {}'.format(departed.name)
    wreck.nouns.update(['wreck'])
    wreck.salvage = [departed.local_system.difficulty,
                     departed.local_system.difficulty]
    departed.local_system.debris.add(wreck)
    if hasattr(departed, 'immortal') and departed.immortal:
        pirate = rat.new_rat(departed.local_system.difficulty)
        output += ('Right after {}\'s explosion, {} warps into the system.\n'
                   ''.format(departed.name, pirate.name))
        qtmud.schedule('hop',
                       ship=pirate,
                       destination=departed.local_system)
    for ship in departed.local_system.ships:
        if hasattr(ship, 'send'):
            qtmud.schedule('send', recipient=ship, text=output)
    return True
qtmud.subscriptions.add(death)