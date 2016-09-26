import random
import hashlib
import pickle

import qtmud

from qtmud.services import MUDSocket
from mudlib import starhopper
from mudlib.starhopper import builders, txt


def alert(system, ship):
    output = ['', 'You were briefly out of warp.']
    # TODO replace with skill check
    for alerted in system.ships:
        if not alerted == ship:
            if random.choice([True, False]):
                output[0] += 'You notice {} enter the system'.format(ship.name)
                if hasattr(alerted, 'aggressive') and ship.aggressive:
                    output[1] += '{} notices your presence.\n'.format(ship.name)
                    if random.choice([True, False, False]):
                        output[1] += 'They decide to attack!'
                        qtmud.schedule('attack', attacker=ship, defender=ship)
                    else:
                        output[1] += 'They leave you alone.'
    if output[0]:
        qtmud.schedule('send', recipient=alerted,text=output[0])
    if output[1]:
        qtmud.schedule('send', recipient=ship, text=output[1])
    return True


def score(ship, points=1):
    ship.score += points
    if ship.name in starhopper.accounts.keys():
        starhopper.accounts[ship.name]['score'] = ship.score
        qtmud.schedule('save')
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
            qtmud.schedule('score', ship=attacker)
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


def client_disconnect(client):
    qtmud.log.debug('disconnecting %s from starhopper', client.name)
    starhopper.players.remove(client)
    qtmud.schedule('death', departed=client, wreck=False)
    return True


def client_login(client, line):
    output = ''
    if not hasattr(client, 'login_stage'):
        client.login_stage = 0
        output = txt.SPLASH
    elif client.login_stage == 0:
        if line in starhopper.accounts.keys():
            output = 'returning player. password?'
            client.captain_name = line
            client.login_stage = 2
        # TODO better name validity checks
        elif line:
            output = 'new player. password?'
            client.captain_name = line
            client.login_stage = 1
        else:
            output = 'your name can\'t be blank, input [desired] captain name'
    elif client.login_stage == 1:
        starhopper.accounts[client.captain_name] = {'password' : line,
                                                    'score' : 0}
        output = 'press enter to complete login'
        client.login_stage = 9
    elif client.login_stage == 2:
        password = starhopper.accounts[client.captain_name]['password']
        if line == password:
            client.login_stage = 9
            output = 'press enter to complete login'
        else:
            client.login_stage = 0
            output = 'wrong password. input [desired] captain name.'
    elif client.login_stage == 9:
        qtmud.log.info('Captain %s has logged in and is controlling %s',
                       client.captain_name,
                       client.name)
        captain = builders.build_captain(client)
        captain.ship = builders.build_ship()
        captain.backstory = builders.generate_backstory(captain.ship)
        starhopper.players.append(captain)
        qtmud.active_services[MUDSocket].logging_in.remove(client)
        qtmud.schedule('save')
        output = txt.PLAYER_LOGIN.format(**locals())
        qtmud.schedule('hop', ship=captain.ship,
                       destination=starhopper.START_SYSTEM)
    if output:
        qtmud.schedule('send', recipient=client, text=output)
    return True


def death(departed, wreck=random.choice([True, False, False])):
    output = ['COMPLETE SYSTEM FAILURE!\n',
              '{} suffers system failure.\n'.format(departed.name)]
    output[0] += 'Your ship suddenly falls out of warp.\n'
    output[1] += 'Their magnetic signature suddenly fades away.   ;_;7\n'
    qtmud.schedule('hop', ship=departed, destination=None)
    if wreck:
        departed.local_system.debris.add(builders.build_wreck(departed))
        output[1] += 'Your scanners detect {} '.format(departed.name)
    qtmud.schedule('send', recipient=departed, text=output[0])
    for local_ship in departed.local_system.ships:
        qtmud.schedule('send', recipient=local_ship, text=output[1])
    return True


def hop(ship, destination=None):
    if ship.local_system:
        try:
            ship.local_system.ships.remove(ship)
        except KeyError:
            qtmud.log.debug('{} not in their local_system.ships'
                            ''.format(ship.name))
    if not destination:
        return True
    ship.local_system = destination
    destination.ships.add(ship)
    for nearby_ship in destination.ships:
        if nearby_ship != ship:
            qtmud.schedule('alert', ship=nearby_ship, incoming=ship)
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
        wreck.salvage[0] -= space
        output += 'Your ship is almost full, but you salvage what you can\n'
    if wreck.salvage[0] == 0:
        salvager.local_system.debris.remove(wreck)
        output += ('As the last of the salvage is collected from {}, '
                   'its magnetic signature fades.\n'.format(wreck.name))
    qtmud.schedule('send', recipient=salvager, text=output)
    return True

def save():
    pickle.dump(starhopper.accounts,
                open("./data/starhopper_accounts.p", 'wb'))
    qtmud.log.debug('saving starhopper player_accounts')
    return True

def survey_planet(scanner, planet):
    output = 'You break from warp, doing a fly-by survey of {planet.name}]\n'
    #qtmud.schedule('alert', system=scanner.local_system, ship=scanner)
    qtmud.schedule('send', recipient=scanner,
                   text=(output.format(**locals()) +
                         builders.generate_survey(planet)))
    return True


def scan_ship(scanner, ship):
    if scanner == ship:
        qtmud.schedule('status', )
    output = '...scanning {}...\n'.format(ship.name)
    output += '{}\n'.format(ship.score)
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
    planet_count = len(system.planets)
    ship_count = len(system.ships)
    exit_count = len(system.neighbors)
    if exit_count == 1 and 'backward' in system.neighbors:
        exit_text = ('You\re at the edge of charted space. Hop backward to '
                     'safety, or hop forward into the unknown. ')
    elif exit_count == 2:
        exit_text = 'You can hop backward or hop forward from here. '
    else:
        exit_text = ('You\'re at the start of your journey, and can only hop '
                     'forward from here. ')
    output = ('Breaking warp bubble for system scan...\n'
              'This is the {system.identity} system, or {system.name}. It has '
              'a {system.star.klass[0]}{system.star.klass[1]} klass sun and '
              '{planet_count} planets in orbit around it. {exit_text}'
              'There are {ship_count} ship(s) flying around.'
              ''.format(**locals()))
    qtmud.schedule('send', recipient=scanner, text=output)
    qtmud.schedule('alert', system=system, ship=scanner)
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