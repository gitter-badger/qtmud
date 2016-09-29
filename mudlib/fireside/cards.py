import random

import qtmud

# TODO cards for checking a player's score

class HamfistedOgre():
    """ The Hamfisted Ogre will do 8 damage to your target, and 4 damage to
    you. Costs 6 mana. """
    def __init__(self):
        self.name = 'Hamfisted Ogre'
        self.cost = 6
        self.damage = 6

    def play(self, player, target=None):
        qtmud.schedule('damage', player=target, amount=self.damage)
        qtmud.schedule('damage', player=player, amount=int(self.damage/2))
        qtmud.schedule('broadcast', channel='fireside', speaker=self,
                       message=('{player.name} plays his {self.name} against '
                                '{target.name}, doing {self.damage}. '
                                'Unfortunately, the Hamfisted Ogre also '
                                'attacked {player.name} for half damage.'
                                ''.format(**locals())))

class RecklessEngineer():
    def __init__(self):
        self.name = 'Reckless Engineer'
        self.cost = 4
        self.repair = 4

    def play(self, player, target=None):
        qtmud.schedule('armor', player=target, amount=self.repair)
        qtmud.schedule('broadcast', channel='fireside', speaker=self,
                       message=('Adding {self.repair} to {player.name'
                                ''.format(**locals())))


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
    """ Pablo costs 7 mana, and adds 2 points to every player's armor -
    except one. That unfortunate player (can't be the person who played
    Pablo) loses all of their armor. """
    def __init__(self):
        self.name = 'Pablo'
        self.cost = 7

    def play(self, player, target):
        players = qtmud.connected_clients
        if len(players) == 1:
            qtmud.schedule('send', recipient=player,
                           text=('You\'re the only player, so Pablo chills '
                                 'with you for a bit. You gain 8 mana.'))
            player.mana += 8
            return True
        random.shuffle(players)
        victim = players.pop()
        if victim == player:
            while victim == player:
                players.append(victim)
                random.shuffle(players)
                victim = players.pop()
        victim.armor = 0
        qtmud.schedule('send', recipient=victim,
                       text=('{player} plays {card.name}, and it destroys all '
                             'your armor!'))
        for p in players:
            p.armor += 2
            qtmud.schedule('send',recipient=p,
                       text=('{player} played {card.name}, so you '
                             'gained 2 armor.'.format(**locals())))
        return True