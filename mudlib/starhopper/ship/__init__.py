import types

import qtmud
from qtmud.services import parser


def warp(ship, destination):
    ship.local_system = destination
    return True
qtmud.subscriptions.add(warp)


def scan(scanee):
    output = 'You scan {}...\n'.format(scanee.name)
    if hasattr(scanee, 'sun'):
        output += 'It has a {} class sun\n'.format(scanee.sun.klass)
    if hasattr(scanee, 'planets'):
        output += ('There are {} planets in orbit around it.'
                   ''.format(len(scanee.planets)))
    return output


def scan_cmd(scanner, line):
    line = parser.parse_line(line)
    scene = 'Your scanner failed to detect that.'
    print(line)
    if 'objekt' in line and line['objekt'] not in ['scan']:
        objekt = line['objekt']
    elif len(line) == 1:
        objekt = 'here'
    else:
        objekt = None
    if objekt in ['room', 'here', 'location', 'local', 'system']:
        objekt = scanner.local_system
    elif objekt in ['me', 'self', 'myself']:
        objekt = scanner
    else:
        print(line)
        matches = parser.search_by_line(scanner, **line)
        if len(matches) == 1:
            objekt = matches[0]
        elif len(matches) > 1:
            scene = ('More than one match, try using the full name of what '
                     'you want:\n')
            for match in matches:
                scene += '{}\n'.format(match.name)
    if hasattr(objekt, 'name'):
        scene = scan(objekt)
    qtmud.schedule('send', recipient=scanner, text=scene)


def apply(thing):
    ship = thing
    ship.local_system = None
    ship.commands['scan'] = types.MethodType(scan_cmd, ship)
    return ship