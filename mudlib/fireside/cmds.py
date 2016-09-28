import qtmud
from mudlib import fireside

def hand(player, line):
    qtmud.schedule('send',
                   recipient=player,
                   text='Cards in your hand:\n'
                        '{}'.format(', '.join([c.name for c in player.hand])))
    return True
def score(player, line):
    qtmud.schedule('send', recipient=player,
                   text=('HEALTH: {player.health}\n'
                         'ARMOR:  {player.armor}\n'
                         'MANA:   {player.mana}\n\n'
                         'SCORE:  {player.score}\n'.format(**locals())))

def deck(player, line):
    qtmud.schedule('send', recipient=player,
                   text='{} cards in the deck.'.format(len(fireside.DECK)))

def play(player, line):
    """ Play a card in your hand.

        in-game syntax: play <card> [[at] <target>]
        Pythonic syntax: play(player, line)
    """
    output = ''
    valid = False
    matches = []
    line = line.split(' ')
    for card in player.hand:
        if line[0] == card.name.lower():
            matches.append(card)
    if len(matches) == 1:
        card = matches[0]
        output += 'Attempting to play the {} card... '.format(card.name)
        if player.mana >= card.cost:
            player.mana += -card.cost
            output += ('took {} mana, now you have {} mana... '
                       ''.format(card.cost, player.mana))
            output += ('shuffling {} back into the deck... '.format(card.name))
            player.hand.remove(card)
            fireside.DECK.append(card.__class__)
            valid = True
        else:
            output += ('you need {} to play this but only have {}... '
                       ''.format(card.cost, player.mana))
    if not output:
        output = 'Play failed for some reason.'
    qtmud.schedule('send', recipient=player, text=output)
    if valid is True:
        card.play(player=player, target=' '.join(line[1:]))
    return True


def info(player, line):
    output = ''
    matches = []
    line = line.split(' ')
    for card in player.hand:
        if line[0] == card.name.lower():
            matches.append(card)
    if len(matches) == 1:
        card = matches[0]
        output += ('--- {card.name} ---\n'
                   'COST:      {card.cost}\n'
                   'INFO:      {card.__doc__}\n'.format(**locals()))
    if not output:
        output = 'Can\'t get that cards info for some reason.'
    qtmud.schedule('send', recipient=player, text=output)
    return True

def draw(player, line):
    output = ''
    if len(player.hand) >= 5:
        output += 'Can\'t draw any more cards, "play" or "discard" one.'
    else:
        qtmud.schedule('draw', player=player, count=1)
    qtmud.schedule('send', recipient=player, text=output)
    return True