import types


import qtmud
from mudlib import starhopper


ASCII_SHIP = """
                     `. ___
                    __,' __`.                _..----....____
        __...--.'``;.   ,.   ;``--..__     .'    ,-._    _.-'
  _..-''-------'   `'   `'   `'     O ``-''._   (,;') _,'
,'________________                          \`-._`-','
 `._              ```````````------...___   '-.._'-:
    ```--.._      ,.                     ````--...__\-.
            `.--. `-` {}     ____    |  |`
              `. `.                       ,'`````.  ;  ;`
                `._`.        __________   `.      \\'__/`
                   `-:._____/______/___/____`.     \  `
                               |       `._    `.    \\
                               `._________`-.   `.   `.___
                                                  `------'`

"""

ASCII_HOP = """
  *  .  . *       *    .        .    `   .   *     *
 .    *    `   . You hop  .      .        .
    *.   *           .     * to {}.
        *   *    .  *      .        .  *   ..  *      .
"""

def engage_cmd(attacker, line):
    line = line.split(' ')[-1]
    matches = []
    output = ''
    for ship in attacker.local_system.ships:
        if ship.name == line or line in ship.nouns:
            matches.append(ship)
    if len(matches) == 1:
        output += '... target found, engaging...'
        qtmud.schedule('attack', attacker=attacker, defender=matches[0])
    elif len(matches) > 1:
        output += 'multiple targets found try being more specific'
    else:
        output += 'command failed yeah'
    qtmud.schedule('send', recipient=attacker, text=output)
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
                   text=(ASCII_HOP.format(ascii_name)))
    qtmud.schedule('send',
                   recipient=ship,
                   text=scan_system(destination))
    return True
qtmud.subscriptions.add(hop)


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
qtmud.subscriptions.add(salvage)

def hop_cmd(ship, line):
    line = line.split(' ')[-1]
    if not line:
        line = 'forward'
    if ship.local_system:
        if line in ship.local_system.adjacent:
            destination = ship.local_system.adjacent[line]
            qtmud.schedule('send',
                           recipient=ship,
                           text='You hop to {}'.format(destination.name))
            qtmud.schedule('hop',
                           ship=ship,
                           destination=destination)
        else:
            if line in ['forward']:
                qtmud.schedule('send',
                               recipient=ship,
                               text='You hop forward into the unknown')
                new_difficulty = ship.local_system.difficulty+1
                destination = \
                    starhopper.starsystem.generate_system(new_difficulty)
                destination.adjacent['backward'] = ship.local_system
                ship.local_system.adjacent['forward'] = destination
                qtmud.schedule('hop',
                               ship=ship,
                               destination=destination)
    return True


def scan_cmd(scanner, line):
    line = ' '.join(line.split(' ')[1:])
    output = None
    matches = []
    if not line:
        line = 'system'
    if line in ['here', 'system', scanner.local_system.name.lower()]:
        output = scan_system(scanner.local_system)
    if line in ['me', 'myself', scanner.name.lower()]:
        output = scan_ship(scanner)
    if line in ['star', 'sun']:
        output = scan_star(scanner.local_system.sun)
    for ship in scanner.local_system.ships:
        if ship.name.lower() == line:
            output = scan_ship(ship)
            matches.append(ship)
        else:
            if line.split(' ')[-1] in ship.nouns:
                output = scan_ship(ship)
                matches.append(ship)
    for planet in scanner.local_system.planets:
        if planet.name.lower() == line:
            output = scan_planet(planet)
            matches.append(planet)
        else:
            for noun in planet.nouns:
                if noun == line.split(' ')[-1]:
                    matches.append(planet)
    for wreck in scanner.local_system.debris:
        if wreck.name.lower() == line:
            output = scan_wreck(wreck)
            matches.append(wreck)
        else:
            if line.split(' ')[-1] in wreck.nouns:
                output = scan_wreck(wreck)
                matches.append(wreck)
    if len(matches) > 1:
        output = 'More than one match:\n'
        for match in matches:
            output += '{}\n'.format(match.name)
    elif output is None:
        output = 'You cannot detect that.'
    qtmud.schedule('send',
                   recipient=scanner,
                   text=output)
    return True


def scan_planet(planet):
    output = '    {}'.format(planet.identity)
    output += '... scanning the surface of {} ...\n'.format(planet.name)
    output += '{} is a {} klass planet.'.format(planet.name,
                                                planet.klass)
    output += '    {}'.format(planet.identity)
    return output


def scan_star(star):
    output = '    {}\n'.format(star.identity)
    output += '{} Stellar Scan\n'.format(star.name)
    output += '{} is a {} klass star.\n'.format(star.name,
                                                star.klass)
    output += '    {}\n'.format(star.identity)
    return output


def scan_system(system):
    output = '    {}\n'.format(system.identity)
    output += '... scanning {} system ...\n'.format(system.name)
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
    return output


def scan_ship(ship):
    output = '...scanning {}...\n'.format(ship.name)
    ascii_name = '{{0: <{}}}'.format(20-len(ship.name)).format(ship.name)
    output += ASCII_SHIP.format(ascii_name)
    output += '{}\n'.format(ship.nouns)
    output += 'BATTERY: {} out of {}.\n'.format(ship.battery[0],
                                                ship.battery[1])
    output += 'DAMAGE: {}, can tolerate {}.\n'.format(ship.damage[0],
                                                      ship.damage[1])
    output += 'SALVAGE: {}, can hold {}.\n'.format(ship.salvage[0],
                                                   ship.salvage[1])
    output += 'ATTACK: {} (cost: {})\n'.format(ship.attack[0], ship.attack[1])
    output += 'DEFENSE: {}\n'.format(ship.defense)
    return output


def scan_wreck(wreck):
    output = '...scanning {}...\n'.format(wreck.name)
    output += '{}\n'.format(wreck.nouns)
    output += 'SALVAGE: {}, can hold {}.\n'.format(wreck.salvage[0],
                                                   wreck.salvage[1])
    return output

def status_cmd(ship, line):
    qtmud.schedule('send', recipient=ship, text=scan_ship(ship))
    return True


def buy_cmd(shopper, line):
    line = ' '.join(line.split(' ')[1:])
    output = ''
    if hasattr(shopper.local_system, 'station'):
        station = shopper.local_system.station
        if not line:
            if station.inventory:
                output = 'Following things for sale: \n'
                output += 'type         | cost          | bonuses\n'
                for upgrade in station.inventory:
                    output += ('{}       {}           {}\n'
                               ''.format(upgrade[0], upgrade[1], upgrade[2:]))
            else:
                output = 'That station is out of stock.\n'
        else:
            for upgrade in station.inventory:
                print(upgrade)
                if upgrade[0] == line:
                    if upgrade[1] <= shopper.salvage[0]:
                        shopper.salvage[0] += -(upgrade[1])
                        qtmud.schedule('upgrade',
                                       ship=shopper,
                                       upgrade=upgrade)
                        output = 'You buy the {} upgrade'.format(upgrade[0])
                    else:
                        output = 'You cannot afford that upgrade.'
                elif not output:
                    output = 'Cannot find that upgrade.'
    else:
        output = 'No station here, try "hop"ping somewhere else.\n'
    qtmud.schedule('send', recipient=shopper, text=output)
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
        qtmud.schedule('send',recipient=ship,text='You upgrade!')
    return True
qtmud.subscriptions.add(upgrade)

def salvage_cmd(ship, line):
    line = ' '.join(line.split(' ')[1:])
    output = None
    matches = []
    print(ship.local_system.debris)
    if not line:
        line = 'wreck'
    for wreck in ship.local_system.debris:
        print(wreck.name)
        print(line)
        print(line.split(' ')[-1])
        print(wreck.nouns)
        if wreck.name.lower() == line:
            matches.append(ship)
        else:
            if line.split(' ')[-1] in wreck.nouns:
                matches.append(wreck)
    print(matches)
    if len(matches) == 1:
        wreck = matches[0]
        qtmud.schedule('salvage',
                       salvager=ship,
                       wreck=wreck)
        output = 'You salvage the {}'.format(wreck.name)
    if len(matches) > 1:
        output = 'More than one match:\n'
        for match in matches:
            output += '{}\n'.format(match.name)
    elif output is None:
        output = 'You cannot salvage that.'
    qtmud.schedule('send',
                   recipient=ship,
                   text=output)


def make_ship(client):
    ship = client
    ship.local_system = None
    ship.battery = [10, 10]
    ship.damage = [0, 10]
    ship.salvage = [0, 10]
    ship.attack = [6, 2]
    ship.defense = 2
    ship.commands['engage'] = types.MethodType(engage_cmd, ship)
    ship.commands['hop'] = types.MethodType(hop_cmd, ship)
    ship.commands['scan'] = types.MethodType(scan_cmd, ship)
    ship.commands['buy'] = types.MethodType(buy_cmd, ship)
    ship.commands['status'] = types.MethodType(status_cmd, ship)
    ship.commands['salvage'] = types.MethodType(salvage_cmd, ship)
    return ship
