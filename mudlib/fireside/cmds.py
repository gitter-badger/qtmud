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

        in-game syntax: play <card> [at <target>]
    """
    output = ''
    card_line = line
    target_line = ''
    target = None
    valid = False
    if 'at' in line.split(' ') and len(line.split(' ')) > 2:
        card_line = ' '.join(line.split(' ')[0:((line.split(' ').index('at')))])
        target_line = ' '.join(line.split(' ')[((line.split(' ').index('at')) +
                                             1):])
    matches = fireside.search_hand(player, card_line)
    if len(matches) == 1:
        valid = True
        card = matches[0]
        output += 'Attempting to play the {} card... '.format(card.name)
        if target_line in ['me', 'self']:
            target = [player]
        else:
            target = fireside.search_connected_players_by_name(target_line)
        if hasattr(card, 'needs_target') and len(target) <= 0:
            output += '...need a target, didn\'t get one... '
            valid = False
        if hasattr(card, 'needs_singular_target'):
            if len(target) == 1:
                target = target[0]
            else:
                output += '...need a single target...'
                valid = False
        if valid is True and player.mana <= card.cost:
            valid = False
            output += ('...you need {} to play this but only have {}... '
                       ''.format(card.cost, player.mana))
    elif len(matches) == 0:
        output += 'Couldn\'t find that card in your hand.'
    elif len(matches) > 1:
        output += 'More than one match for that card.'
    if not output:
        output = 'Play failed for some reason.'
    if valid is True:
        player.mana += -card.cost
        output += ('...took {} mana, now you have {} mana... '
                   ''.format(card.cost, player.mana))
        output += ('shuffling {} back into the deck... '.format(card.name))
        player.hand.remove(card)
        fireside.DECK.append(card)
        player.history.append(card.name)
    qtmud.schedule('send', recipient=player, text=output)
    if valid is True:
        card.play(player=player, target=target)
    return True


def info(player, line):
    output = ''
    matches = fireside.search_hand(player, line)
    if len(matches) == 1:
        card = matches[0]
        output += ('--- {card.name} ---\n'
                   'NAME .....  {card.cost:.>5}\n'
                   'RARITY....  {card.rarity:.>5}\n'.format(**locals()))
        if hasattr(card, 'stats'):
            for stat in card.stats:
                  output += ('{:.<10}  {:.>5}\n'.format(stat.upper(),
                                                 card.stats[stat]))
        if hasattr(card, 'ability'):
            output += card.ability+'\n'
    if not output:
        output = 'Can\'t get that cards info for some reason.'
    qtmud.schedule('send', recipient=player, text=output)
    return True


def discard(client, line):
    qtmud.schedule('send', recipient=client,
                   text='Discard function goes here.')
    return True


def draw(player, line):
    output = ''
    if len(player.hand) >= player.max_hand:
        output += 'Can\'t draw any more cards, "play" or "discard" one.'
    else:
        qtmud.schedule('draw', player=player, count=1)
    qtmud.schedule('send', recipient=player, text=output)
    return True