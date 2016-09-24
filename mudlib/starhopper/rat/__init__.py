import random


import qtmud


RAT_NAMES = ['Anicetus', 'Demetrius', 'Dionysius', 'Gan', 'Genthus',
             'Glauketas', 'Sextus Pompeius', 'Giorgio Adorno', 'James Alday',
             'William Aleyn', 'Jean Ango', 'Aruj', 'Awilda', 'Hayreddin',
             'Baldassare', 'Pier Gerlofs Donia', 'Eric', 'Eustace',
             'Alv', 'Jean Florin', 'Magnus', 'Klein', 'Wijerd',]

RAT_SUFFIXES = ['the Mean']


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
qtmud.subscriptions.add(alert)


def new_rat(difficulty=1):
    rat = qtmud.new_thing()
    rat.nouns.update(['ship', 'pirate', 'rat', 'scum', 'mob'])
    rat.local_system = None
    rat.name = random.choice(RAT_NAMES)
    if random.choice([True, False]) is True:
        old_name = rat.name
        rat.name += ' {}'.format(random.choice(RAT_SUFFIXES))
        for name in old_name.split(' '):
            rat.nouns.add(''.join(name.lower()))
    rat.attack= [difficulty, difficulty]
    rat.defense = difficulty
    rat.battery=[difficulty, difficulty]
    rat.damage= [0, difficulty]
    rat.salvage = [random.randrange(difficulty), difficulty]
    rat.aggressive = True
    rat.immortal = True
    return rat