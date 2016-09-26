import random


import qtmud


FREQUENCY = 9500000
noisy_things = set()


def tick():
    for thing in noisy_things:
        if random.randrange(FREQUENCY) == 10 and thing.noises:
            sense = random.choice(list(thing.noises.keys()))
            noise = random.choice(thing.noises[sense])
            if hasattr(thing, 'contents'):
                for content in thing.contents:
                    if hasattr(content, 'send') and hasattr(content, sense):
                        qtmud.schedule('send',
                                       recipient=content,
                                       text=noise)
            for attribute in ['location', 'container']:
                if hasattr(thing, attribute):
                    for content in thing.attribute.contents:
                        if hasattr(content, 'send') and hasattr(content, sense):
                            qtmud.schedule('send',
                                           recipient=content,
                                           text=noise)
    return True
