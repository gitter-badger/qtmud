import qtmud
from mudlib import starhopper
from mudlib.starhopper import builders


def status(ship, line):
    qtmud.schedule('scan_ship',scanner=ship, ship=ship)
    return True

def scan(scanner, line):
    line = ' '.join(line.split(' ')[1:])
    output = None
    matches = []
    if not line:
        line = 'system'
    if line in ['here', 'system', scanner.local_system.name.lower()]:
        qtmud.schedule('scan_system', scanner=scanner,
                       system=scanner.local_system)
        return True
    if line in ['me', 'myself', scanner.name.lower()]:
        qtmud.schedule('scan_ship', scanner=scanner, ship=scanner)
        return True
    if line in ['star', 'sun']:
        qtmud.schedule('scan_star', scanner=scanner,
                       star=scanner.local_system.sun)
        return True
    for ship in scanner.local_system.ships:
        if ship.name.lower() == line:
            matches.append(ship)
        elif line.split(' ')[-1] in ship.nouns:
            matches.append(ship)
    if len(matches) == 1:
        qtmud.schedule('scan_ship',scanner=scanner, ship=ship)
        return True
    for planet in scanner.local_system.planets:
        if planet.name.lower() == line:
            matches.append(planet)
        elif line.split(' ')[-1] in planet.nouns:
            matches.append(planet)
    if len(matches) == 1:
        qtmud.schedule('scan_planet', scanner=scanner, planet=planet)
        return True
    for wreck in scanner.local_system.debris:
        if wreck.name.lower() == line:
            matches.append(wreck)
        elif line.split(' ')[-1] in wreck.nouns:
            matches.append(wreck)
    if len(matches) == 1:
        qtmud.schedule('scan_wreck', scanner=scanner, wreck=wreck)
        return True
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


def hop(ship, line):
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
                    builders.build_system(new_difficulty)
                destination.adjacent['backward'] = ship.local_system
                ship.local_system.adjacent['forward'] = destination
                qtmud.schedule('hop',
                               ship=ship,
                               destination=destination)
    return True


def engage(attacker, line):
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


def radio(speaker, line):
    message = ' '.join(line.split(' ')[1:])
    output = '\n{0} wisps: {1}'.format(speaker.name, message)
    for recipient in starhopper.players:
        qtmud.schedule('send', recipient=recipient, text=output)

def salvage(ship, line):
    line = ' '.join(line.split(' ')[1:])
    output = None
    matches = []
    print(ship.local_system.debris)
    if not line:
        line = 'wreck'
    for wreck in ship.local_system.debris:
        if wreck.name.lower() == line:
            matches.append(ship)
        else:
            if line.split(' ')[-1] in wreck.nouns:
                matches.append(wreck)
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


def buy(shopper, line):
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