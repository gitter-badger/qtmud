import qtmud
from mudlib import starhopper
from mudlib.starhopper import builders


# TODO survey() planets

def status(ship, line):
    qtmud.schedule('send', recipient=ship, text=builders.generate_status(ship))
    return True
def christen(captain, line):
    captain.ship.name = ' '.join(line.split(' ')[1:])
    return True


def scan(scanner, line):
    line = ' '.join(line.split(' ')[1:])
    output = None
    matches = []
    if not line:
        line = 'system'
    if line in ['here', 'system', scanner.ship.local_system.name.lower()]:
        qtmud.schedule('scan_system', scanner=scanner,
                       system=scanner.ship.local_system)
        return True
    if line in ['me', 'myself', scanner.name.lower()]:
        qtmud.schedule('send', recipient=scanner.ship,
                       text=builders.generate_status(scanner.ship))
        return True
    if line in ['star', 'sun']:
        qtmud.schedule('scan_star', scanner=scanner,
                       star=scanner.ship.local_system.sun)
        return True
    for ship in scanner.ship.local_system.ships:
        if ship.name.lower() == line:
            matches.append(ship)
        elif line.split(' ')[-1] in ship.nouns:
            matches.append(ship)
    if len(matches) == 1:
        qtmud.schedule('scan_ship',scanner=scanner, ship=ship)
        return True
    for planet in scanner.ship.local_system.planets:
        if planet.name.lower() == line:
            matches.append(planet)
        elif line.split(' ')[-1] in planet.nouns:
            matches.append(planet)
    if len(matches) == 1:
        qtmud.schedule('survey_planet', scanner=scanner, planet=planet)
        return True
    for wreck in scanner.ship.local_system.debris:
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
    qtmud.schedule('alert',system=scanner.ship.local_system,
                   ship=scanners.ship)
    return True


def hop(hopper, line):
    line = line.split(' ')[-1]
    ship = hopper.ship
    if line in ['hop']:
        line = 'forward'
    if ship.local_system:
        system = ship.local_system
        if line in system.neighbors:
            destination = system.neighbors[line]
            output = 'You hop to {}'.format(destination.name)
        elif line in ['forward']:
            destination = builders.build_system(system.difficulty+1)
            system.neighbors['forward'] = destination
            destination.neighbors['backward'] = system
            output = ('You hop from {system.name} to {destination.name}, '
                      'maintaining a protective warp bubble upon arrival. '
                      '"scan" the system to gain your bearings, or keep '
                      '"hop"ping forward to try and reach your '
                      'ultimate destination.'.format(**locals()))
        else:
            output = 'You cannot hop there.'
            destination = None
        if destination:
            qtmud.schedule('hop', ship=ship, destination=destination)
    qtmud.schedule('send', recipient=hopper, text=output)
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

def salvage(salvager, line):
    ship = salvager.ship
    line = ' '.join(line.split(' ')[1:])
    output = None
    matches = []
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
    qtmud.schedule('send', recipient=ship, text=output)


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