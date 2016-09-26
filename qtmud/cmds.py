import qtmud

def finger(fingerer, line):
    qtmud.schedule('finger',
                   fingerer=fingerer,
                   fingeree=line)
    return True


def commands(commander, line):
    qtmud.schedule('send',
                   recipient=commander,
                   text='{}'.format(commander.commands.keys()))
    return True