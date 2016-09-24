import random

import qtmud
from mudlib.starhopper import builders, txt


def alert(rat, ship):
    if hasattr(rat, 'aggressive') and rat.aggressive:
        qtmud.schedule('send', recipient=ship,
                       text=('{} is alerted to your presence!\n'
                             ''.format(rat.name)))
        if random.choice([True, False]) is True:
            qtmud.schedule('send', recipient=ship,
                           text=('{} decides to attack you!\n'
                                 ''.format(rat.name)))
            qtmud.schedule('attack', attacker=rat, defender=ship)
        else:
            qtmud.schedule('send', recipient=ship,
                           text='{} leaves you alone.\n'.format(rat.name))
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
        pirate = builders.build_rat(departed.local_system.difficulty)
        output += ('Right after {}\'s explosion, {} warps into the system.\n'
                   ''.format(departed.name, pirate.name))
        qtmud.schedule('hop',
                       ship=pirate,
                       destination=departed.local_system)
    for local_ship in departed.local_system.ships:
        if hasattr(local_ship, 'send'):
            qtmud.schedule('send', recipient=local_ship, text=output)
    return True


def hop(ship, destination):
    if ship.local_system:
        try:
            ship.local_system.ships.remove(ship)
        except KeyError:
            qtmud.log.debug('tried to remove {} from {}\'s ships but they '
                            'weren\'t there.'.format(ship.name,
                                                     ship.local_system.name))
    if not destination:
        return True
    ship.local_system = destination
    ship.local_system.ships.add(ship)
    for nearby_ship in ship.local_system.ships:
        qtmud.schedule('alert',
                       rat=nearby_ship,
                       ship=ship)
    ascii_name = ('{{0: <{}}}'
                  ''.format((15-len(destination.name))).format(
                     destination.name))
    qtmud.schedule('send',
                   recipient=ship,
                   text=(txt.ASCII_HOP.format(ascii_name)))
    qtmud.schedule('scan_system',
                   scanner=ship,
                   system=destination)
    return True


def salvage(salvager, wreck):
    output = ''
    space = abs(salvager.salvage[0] - salvager.salvage[1])
    if space >= wreck.salvage[0]:
        salvager.salvage[0] += wreck.salvage[0]
        wreck.salvage[0] = 0
        output += 'You salvage the {}.\n'.format(wreck.name)
    else:
        salvager.salvage[0] += space
        wreck.salvage[0] += -(space)
        output += 'Your ship is almost full, but you salvage what you can\n'
    if wreck.salvage[0] == 0:
        salvager.local_system.debris.remove(wreck)
        output +=  ('As the last of the salvage is collected from {}, '
                    'its magnetic signature fades.\n'.format(wreck.name))
    qtmud.schedule('send', recipient=salvager, text=output)
    return True

def scan_planet(scanner, planet):
    output = '    {}'.format(planet.identity)
    output += '... scanning the surface of {} ...\n'.format(planet.name)
    output += '{} is a {} klass planet.'.format(planet.name,
                                                planet.klass)
    output += '    {}'.format(planet.identity)
    qtmud.schedule('send', recipient=scanner, text=output)
    return True


def scan_ship(scanner, ship):
    output = '...scanning {}...\n'.format(ship.name)
    ascii_name = '{{0: <{}}}'.format(20-len(ship.name)).format(ship.name)
    output += txt.ASCII_SHIP.format(ascii_name)
    output += '{}\n'.format(ship.nouns)
    output += 'BATTERY: {} out of {}.\n'.format(ship.battery[0],
                                                ship.battery[1])
    output += 'DAMAGE: {}, can tolerate {}.\n'.format(ship.damage[0],
                                                      ship.damage[1])
    output += 'SALVAGE: {}, can hold {}.\n'.format(ship.salvage[0],
                                                   ship.salvage[1])
    output += 'ATTACK: {} (cost: {})\n'.format(ship.attack[0], ship.attack[1])
    output += 'DEFENSE: {}\n'.format(ship.defense)
    qtmud.schedule('send', recipient=scanner, text=output)
    return output


def scan_star(scanner, star):
    output = '    {}\n'.format(star.identity)
    output += '{} Stellar Scan\n'.format(star.name)
    output += '{} is a {} klass star.\n'.format(star.name,
                                                star.klass)
    output += '    {}\n'.format(star.identity)
    qtmud.schedule('send', recipient=scanner, text=output)
    return True


def scan_system(scanner, system):
    output = ('    {}\n'
              '... scanning {}...\n'
              '...difficulty? {}\n'
              '  *  klass {} sun\n'
              '     - {} orbiting bodies\n'
              '---')
    output + '... risk'
    if hasattr(system, 'difficulty'):
        output += 'This is a {} difficulty system.\n'.format(system.difficulty)
    if hasattr(system, 'sun'):
        output += 'It has a {} class sun\n'.format(system.sun.klass)
    if hasattr(system, 'planets'):
        output += ('There are {} planets in orbit around it.\n'
                   ''.format(len(system.planets)))
    if hasattr(system, 'ships'):
        output += ('Your scanner picks up {} ships.\n'
                   ''.format(len(system.ships)))
        for ship in system.ships:
            output += '    {}\n'.format(ship.name)
    if hasattr(system, 'station'):
        output += ('There\'s a station here! You can "shop" for upgrades.\n')
    if hasattr(system, 'adjacent'):
        directions = len(system.adjacent.keys())
        if directions == 0:
            output += ('You\'re at the start of the universe!\n'
                       '"hop forward" into the unknown!\n')
        elif directions == 1:
            output += ('You\'re at the end of the universe!\n'
                       '"hop backward" to go to safer space -or-\n'
                       '"hop forward" into the unknown!\n')
        else:
            output += 'Here\'s where you can hop:\n'
            for direction in system.adjacent:
                output += '     {}\n'.format(direction)
    if hasattr(system, 'debris'):
        debris = system.debris
        if len(debris) > 0:
            output += 'There\'s some wrecks here:\n'
            for wreck in debris:
                output += '{}\n'.format(wreck.name)

    output += '    {}\n'.format(system.identity)
    qtmud.schedule('send', recipient=scanner, text=output)
    return True


def scan_wreck(scanner, wreck):
    output = '...scanning {}...\n'.format(wreck.name)
    output += '{}\n'.format(wreck.nouns)
    output += 'SALVAGE: {}, can hold {}.\n'.format(wreck.salvage[0],
                                                   wreck.salvage[1])
    qtmud.schedule('send',recipient=scanner, text=output)
    return True


def upgrade(ship, upgrade):
    type = upgrade[0]
    if type == 'charge':
        ship.battery[0] += upgrade[2]
        if ship.battery[0] > ship.battery[1]:
            ship.battery[0] = ship.battery[1]
    if type == 'battery':
        ship.battery[1] += upgrade[2]
    if type == 'attack':
        ship.attack = [upgrade[2], upgrade[3]]
    if type == 'defense':
        ship.defense = upgrade[2]
    if hasattr(ship, 'send'):
        qtmud.schedule('send', recipient=ship, text='You upgrade!')
    return True