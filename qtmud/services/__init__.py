""" core qtmud methods

    .. versionadded:: 0.0.4
"""

import qtmud


loaded = list()


def send(recipient, text):
    """ send text to recipient

        Parameters:
            recipient(object):      thing to whom text will be sent
            text(str):              text to send to thing
        Return:
            bool:                   True

        If recipient has a send() method (i.e. is a client, send them text.
    """
    if hasattr(recipient, 'send'):
        recipient.send(text)
    return True
qtmud.subscriptions.add(send)


def tick():
    """ main game ticker

        Return:
            bool:           True

        Sends events out to the methods subscribed to them and ticks services.
    """
    if qtmud.events:
        current_events = qtmud.events
        qtmud.events = dict()
        for event in current_events:
            for call in current_events[event]:
                event(**call)
    for service in loaded:
        service.tick()
    return True
