""" sends output to client.

    .. moduleauthor: Morgan Sennhauser <morgan.sennhauser@gmail.com>

    .. versionadded:: 0.0.3-feature/noisemaker
"""

import random

# the bigger it is, the less frequent the noise
FREQUENCY = 2500000

class Noisemaker(object):
    """

        .. versionadded:: 0.0.3-feature/noise
    """

    def __init__(self, manager):
        """
            .. versionadded:: 0.0.3-feature/noise
        """
        self.manager = manager
        self.noisy_things = set()

    def add(self, thing):
        return self.noisy_things.add(thing)

    def tick(self, events=False):
        """ Sends a line to a thing, usually a client.

            .. versionadded:: 0.0.3-feature/noise

            noises = { 'look' : ['you see someone trip on the curb',
                                 'a balloon drifts overhead'],
                       'listen' : ['you hear someone fall']}
        """
        for thing in self.noisy_things:
            if random.randrange(FREQUENCY) == 10:
                sense = random.choice(list(thing.noises.keys()))
                noise = random.choice(thing.noises[sense])
                if hasattr(thing, 'contents'):
                    for content in thing.contents:
                        if hasattr(content, 'send') and hasattr(content, sense):
                            content.manager.schedule('send',
                                                     thing=content,
                                                     scene=noise)
                if hasattr(thing, 'location') and thing.location:
                    if hasattr(thing.location, 'contents'):
                        for content in thing.location.contents:
                            if hasattr(content, 'send') and hasattr(content,
                                                                    sense):
                                content.manager.schedule('send',
                                                         thing = content,
                                                         scene = noise)
        return True
