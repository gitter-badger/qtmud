import types

import qtmud
from qtmud.services import parser

def look(objekt):
    scene = 'huh'
    if hasattr(objekt, 'name') and hasattr(objekt, 'description'):
        scene = '- You look at {} -\n{}\n'.format(objekt.name,
                                                  objekt.description)
    if hasattr(objekt, 'exits') and objekt.exits:
        scene += 'exits [ '
        for direction in objekt.exits:
            scene += '{} , '.format(direction)
        scene += ']\n'
    if hasattr(objekt, 'contents') and objekt.contents:
        scene += 'contents: ( '
        for content in objekt.contents:
            if hasattr(content, 'name') and hasattr(content, 'location'):
                scene += '{}, '.format(content.name)
        scene += ')'
    return scene

def look_cmd(looker, line):
    line = parser.parse_line(line)
    scene = 'Whatever you tried to look at, you can\'t.'
    if 'objekt' in line:
        objekt = line['objekt']
    elif len(line) == 1:
        objekt = 'here'
    else:
        objekt = None
    if objekt in ['room', 'here', 'location'] and hasattr(looker, 'location'):
        objekt = looker.location
    elif objekt in ['me', 'self', 'myself']:
        objekt = looker
    else:
        print(line)
        matches = qtmud.search_by_line(looker, **line)
        if len(matches) == 1:
            objekt = matches[0]
        elif len(matches) > 1:
            scene = ('More than one match, try using the full name of what '
                     'you want:\n')
            for match in matches:
                if hasattr(match, 'name') and hasattr(match, 'description'):
                    scene += ('{}\n'.format(match.name))
    if hasattr(objekt, 'name'):
        scene = look(objekt)
    qtmud.schedule('send', recipient=looker, text=scene)
    return True


def apply(thing):
    if hasattr(thing, 'commands'):
        thing.commands['look'] = types.MethodType(look_cmd, thing)
    return thing
