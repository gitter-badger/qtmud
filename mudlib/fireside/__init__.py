import pickle
import types

from inspect import getmembers, isfunction, isclass


import qtmud
import qtmud.subscriptions
from mudlib.fireside import cards, cmds, services, subscriptions, txt


player_hands = dict()
DECK = dict()


def build_client(client):
    client.hand = list()
    qtmud.schedule('send',recipient=client,text=txt.SPLASH)
    for command, function in [m for m in getmembers(cmds) if isfunction(m[1])]:
        client.commands[command] = types.MethodType(function, client)
    qtmud.active_services['talker'].tune_in(channel='fireside',client=client)
    if not hasattr(client, 'score'):
        client.score = 0
    if not hasattr(client, 'mana'):
        client.mana = 20
    if not hasattr(client, 'health'):
        client.health = 10
    if not hasattr(client, 'armor'):
        client.armor = 0
    if not hasattr(client, 'word_count'):
        client.word_count = 0
    if not client.hand:
        qtmud.schedule('send', recipient=client,
                       text='Looks like you\'re a new player - lets draw you '
                            'some cards.')
        qtmud.schedule('draw', player=client, count=2)
    return client

def search_hand(player, text):
    return True


def load():
    global DECK
    qtmud.log.info('load()ing Fireside')
    qtmud.log.info('adding fireside.subscriptions to qtmud.subscribers')
    for s in getmembers(subscriptions):
        if isfunction(s[1]):
            if not s[1].__name__ in qtmud.subscribers:
                qtmud.subscribers[s[1].__name__] = list()
            qtmud.subscribers[s[1].__name__].append(s[1])
    qtmud.active_services['talker'].new_channel('fireside')
    DECK = [c[1] for c in getmembers(cards) if isclass(c[1])]
    return True