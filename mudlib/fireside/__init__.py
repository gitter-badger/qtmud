import pickle
import types

from inspect import getmembers, isfunction, isclass


import qtmud
import qtmud.subscriptions
from mudlib.fireside import cards, cmds, services, subscriptions, txt

connected_players = list()
player_hands = dict()
""" All the hands currently held by different players, in the format of
``{ player : [ list, of, cards ] }``"""
DECK = list()
""" built from the classes in :mod:`fireside.cards` when :func:`load` is
called. """




def build_client(client):
    """ Expecting to be passed an instance of :class:`qtmud.Thing`,
    this method turns a client into a Fireside player.

    That means giving the client several attributes:

    +------------+------+------------------------------------------------------+
    | attribute  | type | use                                                  |
    +============+======+======================================================+
    | hand       | list | the cards the player holds. mirrored in              |
    |            |      | :attr:`player_hands`.                                |
    +------------+------+------------------------------------------------------+
    | mana       | int  | increased by talking, decreased by playing cards.    |
    +------------+------+------------------------------------------------------+
    | health     | int  | if this reaches 0, the player                        |
    |            |      | :func:`dies <fireside.subscriptions.death>`.         |
    +------------+------+------------------------------------------------------+
    | armor      | int  | additional protection from damage.                   |
    +------------+------+------------------------------------------------------+
    | word_count | int  | additional protection from damage.                   |
    +------------+------+------------------------------------------------------+
    """
    connected_players.append(client)
    qtmud.schedule('send',recipient=client,text=txt.SPLASH)
    for command, function in [m for m in getmembers(cmds) if isfunction(m[1])]:
        client.commands[command] = types.MethodType(function, client)
    qtmud.active_services['talker'].tune_in(channel='fireside',client=client)
    client.max_hand = 7
    client.max_health = 20
    client.history = list()
    client.hand = list()
    client.mana = 10
    client.health = 20
    client.armor = 0
    client.word_count = 0
    return client


def search_connected_players_by_name(name):
    return [p for p in connected_players if p.name.lower() == name.lower()]


def search_hand(player, text):
    """ Searches player's hands for any cards whose name matches text,
    or whose name has one word matching with text if text is one word.
    """
    matches = list()
    digit = None
    if text[-1].isdigit():
        digit = text.split(' ')[-1]
        text = ' '.join(text.split(' ')[0:-1])
        print(digit)
        print(text)
    for card in player.hand:
        if text == card.name.lower() or \
                (len(text.split(' ')) == 1 and
                         text == card.name.split(' ')[-1].lower()):
            matches.append(card)
    if matches and digit:
        matches = [matches[int(digit)]]
    return matches


def load():
    """ Adds Fireside :mod:`subscriptions <fireside.subscriptions>` to
    :attr:`qtmud.active_subscribers` and builds :attr:`DECK` from the classes
    in :mod:`fireside.cards`.
    """
    global DECK
    qtmud.log.info('load()ing Fireside')
    qtmud.log.info('adding fireside.subscriptions to qtmud.subscribers')
    for s in getmembers(subscriptions):
        if isfunction(s[1]):
            if not s[1].__name__ in qtmud.subscribers:
                qtmud.subscribers[s[1].__name__] = list()
            qtmud.subscribers[s[1].__name__].append(s[1])
    qtmud.active_services['talker'].new_channel('fireside')
    for card in [c[1]() for c in getmembers(cards) if isclass(c[1])]:
        for _ in range(card.rarity):
            DECK.append(card.__class__())
    qtmud.log.info('Built the Fireside deck - {} cards total.'
                   ''.format(len(DECK)))
    return True


def start():
    return True

