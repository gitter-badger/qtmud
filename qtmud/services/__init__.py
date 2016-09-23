import qtmud


loaded = list()


def send(recipient, text):
    if hasattr(recipient, 'send'):
        recipient.send(text)
    return True

def tick():
    if qtmud.events:
        current_events = qtmud.events
        qtmud.events = dict()
        for event in current_events:
            for call in current_events[event]:
                event(**call)
    for service in loaded:
        service.tick()
    return True