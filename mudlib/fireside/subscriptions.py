import pickle
import random


import qtmud
from mudlib import fireside

def client_disconnect(client):
    qtmud.log.debug('disconnecting {} from Fireside.'.format(client.name))
    for other in qtmud.connected_clients:
        qtmud.schedule('send',
                       recipient=other,
                       text='{} disconnected.'.format(client.name))
    if hasattr(client, 'hand'):
        for card in client.hand:
            qtmud.schedule('undraw', player=client, card=card)
    return True

def undraw(player, card):
    qtmud.log.debug('moving {} from {}\'s hand to the deck.'
                    ''.format(card.name, player.name))
    player.hand.remove(card)
    fireside.DECK.append(card.__class__)
    return


def broadcast(channel, speaker, message):
    if not message:
        qtmud.schedule('send', recipient=speaker,
                       text= 'syntax: {} <message>'.format(channel))
    else:
        for listener in qtmud.active_services['talker'].channels[channel]:
            qtmud.schedule('send',
                           recipient=listener,
                           text='({}) {}: {}'.format(channel,
                                                     speaker.name,
                                                     message))
            qtmud.active_services['talker'].history[
                channel].append('{}: {}'.format(speaker.name, message))
        speaker.word_count += len(message.split(' '))
        if speaker.word_count >= 50:
            speaker.word_count = speaker.word_count - 50
            speaker.mana += 1
            qtmud.schedule('send', recipient=speaker,
                           text='You gain a mana point.')
    return True


def damage(player, amount=0):
    if player.armor > 0:
        player.armor += -amount
        amount = 0
        if player.armor < 0:
            amount = abs(player.armor)
            player.armor = 0
    player.health += -amount
    return True


def draw(player, count=1):
    random.shuffle(fireside.DECK)
    drawn_cards = list()
    for c in range(count):
        try:
            drawn_cards.append(fireside.DECK.pop()())
        except Exception as err:
            qtmud.schedule('send', recipient=player,
                           text='The deck is empty! Wait for someone to play '
                                'a card before drawing something.')
    if drawn_cards:
        for card in drawn_cards:
            player.hand.append(card)
            fireside.player_hands[player.name] = player.hand
        qtmud.schedule('send', recipient=player,
                       text='Drew {} card[s]'.format(', '.join([c.name for c in
                                                                drawn_cards])))
    qtmud.schedule('save_player_hands')
    return True


def score(player, change=1):
    player.score += change
    return True