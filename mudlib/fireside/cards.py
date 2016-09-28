import random

import qtmud


class Spam():
    """ what does this card do """
    def __init__(self):
        self.name = 'Spam'
        self.cost = 5

    def play(self, player, target=None):
        target_count = 0
        for client in qtmud.connected_clients:
            if not client == player:
                qtmud.schedule('send', recipient=client,
                               text= ('{} played the SPAM card!\n'
                                      '       SSSSS  PPPP   AA   M  M  M\n'
                                      '       S      P  P  A  A  MM M MM\n'
                                      '       SSSSS  PPPP  AAAA  M M M M\n'
                                      '           S  P     A  A  M     M\n'
                                      '       SSSSS  P     A  A  M     M '
                                      ''.format(player.name)))
                target_count += 1
        player.armor += target_count
        qtmud.schedule('send', recipient=player,
                       text=('Hit {} players with your SPAM, so you\'ve '
                             'gained that much armor'.format(target_count)))


class Ork():
    """ Randomly attacks another player for 2 damage - Ork might hurt the
    player who plays it, so watch out. """
    def __init__(self):
        self.name = 'Ork'
        self.cost = 3
        self.damage = 2

    def play(self, player, target):
        victim = random.choice(qtmud.connected_clients)
        qtmud.schedule('damage', player=victim, amount=self.damage)
        qtmud.schedule('send',
                       recipient=player,
                       text='You attack {}'.format(victim.name))
        qtmud.schedule('send',
                       recipient=victim,
                       text='{}\'s Ork attacks you.'.format(player.name))



class Grunt():
    """ Boosts your armor by 2 points """
    def __init__(self):
        self.name = 'Grunt'
        self.cost = 3
        self.armor_boost = 2

    def play(self, player, target):
        player.armor += self.armor_boost
        qtmud.schedule('send', recipient=player,
                       text=('{self.name} moves to defend you, giving you '
                             '{self.armor_boost} more armor.'
                             ''.format(**locals())))


class Neckbeard():
    """ what does this card do """
    def __init__(self):
        self.name = 'Neckbeard'
        self.cost = 3

    def play(self, player, target):
        qtmud.schedule('send', recipient=player,
                       text=('This card doesn\'t do anything yet!'))

class Pablo():
    """ what does this card do """
    def __init__(self):
        self.name = 'Pablo'
        self.cost = 3

    def play(self, player, target):
        qtmud.schedule('send', recipient=player,
                       text=('This card doesn\'t do anything yet!'))

