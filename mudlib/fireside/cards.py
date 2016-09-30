import random

import qtmud

# todo: player accounts
# search_by_connceted_player
# serach by player accounts
#
class Card(object):
    def __init__(self):
        self.name = 'Basic Card'
        self.owner = None
        self.rarity = 0
        self.cost = 0

    def play(self, player, target):
        return True


class ClockworkWeasel(Card):
    def __init__(self):
        super(ClockworkWeasel, self).__init__()
        self.name = 'Clockwork Weasel'
        self.owner = None
        self.rarity = 4
        self.cost = 3
        self.needs_singular_target = True
        self.ability = ('Tells you the cards an opponent has in their hands - '
                        'and the opponent will be none the wiser!')

    def play(self, player, target):
        output = ''
        if len(target) == 1:
            target = target[0]
            spied_hand = '\n'.join([c.name for c in target.hand])
            output += ('You send your clockwork weasel scurrying toward {} '
                       'and after a moment, the weasel tells you cards they '
                       'have in their hand:\n{}'.format(target.name,
                                                        spied_hand))

        qtmud.schedule('send', recipient=player, text=output)


class HamfistedOgre(Card):
    def __init__(self):
        super(HamfistedOgre, self).__init__()
        self.name = 'Hamfisted Ogre'
        self.owner = None
        self.rarity = 3
        self.cost = 6
        self.stats = {'damage' : 6 }
        self.ability = ('Does {} to whoever its played against, but in its '
                        'eagerness to cause damage, does {} to whoever played '
                        'it.'.format(self.stats['damage'],
                                     int(self.stats['damage']/2)))

    def play(self, player, target):
        damage = self.stats['damage']
        qtmud.schedule('damage', player=target, amount=damage)
        qtmud.schedule('send', recipient=player,
                       text= ('Your Hamfisted Ogre does {} damage to {}, '
                              'but also does {} damage to you.'
                              ''.format(damage, target.name, int(damage/2))))
        qtmud.schedule('damage', player=player, amount=int(self.damage/2))
        qtmud.schedule('send', recipient=player,
                       text=('{}\'s Hamfisted Ogre does {} damage to you.'
                             ''.format(player.name, damage)))


class RecklessEngineer(Card):
    def __init__(self):
        super(RecklessEngineer, self).__init__()
        self.name = 'Reckless Engineer'
        self.owner = None
        self.rarity = 4
        self.cost = 4
        self.stats = {'repair': 4,
                      'damage': 2}
        self.ability = ('Adds {} to your (or a target\'s) armor, but does {} '
                        'damage to you/them as well. (The armor comes first.)'
                        ''.format(self.stats['repair'], self.stats['damage']))

    def play(self, player, target=None):
        if not target:
            target = player
        repair = self.stats['repair']
        damage = self.stats['damage']
        qtmud.schedule('armor', player=target, amount=repair)
        qtmud.schedule('damage', player=target, amount=damage)
        qtmud.schedule('send', recipient=target,
                       text=('{}\'s RecklessEngineer repairs you for {} '
                             'armor, but then hurts you for {} damage.'
                             ''.format(player.name, repair, damage)))


class Spam(Card):
    def __init__(self):
        super(Spam, self).__init__()
        self.name = 'Spam'
        self.rarity = 2
        self.cost = 7
        self.stats = {'armor' : 1}
        self.ability = ('Sends a spammy message to every player, and you gain '
                        '{} for every player it hits.'
                        ''.format(self.stats['armor']))

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
        player.armor += target_count * self.stats['armor']
        qtmud.schedule('send', recipient=player,
                       text=('Hit {} players with your SPAM, so you\'ve '
                             'gained that much armor'.format(target_count)))


class Ork(Card):
    def __init__(self):
        super(Ork, self).__init__()
        self.name = 'Ork'
        self.owner = None
        self.rarity = 4
        self.cost = 1
        self.stats = {'damage': 2}
        self.ability = {'Does 2 damage to a random player - possibly the one '
                        'who played it!'}

    def play(self, player, target):
        victim = random.choice(qtmud.connected_clients)
        qtmud.schedule('damage', player=victim, amount=self.stats['damage'])
        qtmud.schedule('send',
                       recipient=player,
                       text='You attack {}'.format(victim.name))
        qtmud.schedule('send',
                       recipient=victim,
                       text='{}\'s Ork attacks you.'.format(player.name))



class Grunt(Card):
    def __init__(self):
        super(Grunt, self).__init__()
        self.name = 'Grunt'
        self.owner = None
        self.rarity = 5
        self.cost = 3
        self.stats = {'armor': 2}
        self.ability = ('Boosts the player\'s armor by {}'
                        ''.format(self.stats['armor']))

    def play(self, player, target):
        player.armor += self.stats['armor']
        qtmud.schedule('send', recipient=player,
                       text=('Your Grunt boosts your armor by {}'
                             ''.format(self.stats['armor'])))


class Neckbeard(Card):
    def __init__(self):
        super(Neckbeard, self).__init__()
        self.name = 'Neckbeard'
        self.owner = None
        self.rarity = 0
        self.cost = 3
        self.ability = ('Shows how much mana every player has.')

    def play(self, player, target):
        qtmud.schedule('send', recipient=player,
                       text=('This card doesn\'t do anything yet!'))

class Pablo():
    """ Pablo costs 7 mana, and adds 2 points to every player's armor -
    except one. That unfortunate player (can't be the person who played
    Pablo) loses all of their armor. """
    def __init__(self):
        self.name = 'Pablo'
        self.owner = None
        self.rarity = 0
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


class PetulantChild():
    """ Does 10 damage to a player. Normally costs 20, but costs 1 less for
    each health less than 20 you have."""
    def __init__(self):
        self.name = 'Petulant Child'
        self.owner = None
        self.rarity = 0
        self.cost = 20

    def play(self, player, target):
        refund = self.cost - (20-player.health)
        player.health += refund


class MysticGiant(Card):
    """ Cost: 35, costs 1 less for each card you've played. Does some
    ridiculous thing."""
    def __init__(self):
        super(MysticGiant, self).__init__()
        self.name = 'Mystic Giant'
        self.rarity = 0
        self._cost = 35
        self.stats = {'hum' : 2}
        return

    @property
    def cost(self):
        return self._cost - len(self.owner.history)

    @cost.setter
    def cost(self, value):
        self._cost = value


    def play(self, player, target):
        qtmud.schedule('send', recipient=player,
                       text='This card is owned by {}'.format(player.name))
        return True
