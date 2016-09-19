""" pushes immersive chatter to clients

    .. moduleauthor: Morgan Sennhauser <morgan.sennhauser@gmail.com>

    .. versionadded:: 0.0.3-feature/noisemaker

    Noisemaker is a :class:`service <qtmud.services.Service>` that helps
    qtmud seem a little more alive. It keeps a set of :attr:`noisy_things
    <qtmud.services.noisemaker.Noisemaker.noisy_things>`, which are
    :class:`things <qtmud.Thing>` that have had the :class:`Noisy
    <qtmud.qualities.noisy.Noisy>` :class:`quality <qtmud.qualities>` added
    to them.

    Then, when Noisemaker is :func:`tick()ed
    <qtmud.services.noisemaker.Noisemaker.tick>`, it looks iterates through
    ``noisy_things`` and, based on :attr:`FREQUENCY
    <qtmud.services.noisemaker.FREQUENCY>, has a chance of randomly firing
    off one of the :attr:noises <qtmud.qualities.noisy.Noisy.noises>` in that
    thing.

    Attributes:
        FREQUENCY(int):         There's a 1:FREQUENCY chance of a ``thing``
                                making a noise this tick.
"""


import random


# the bigger it is, the less frequent the noise
# this is a piss-poor way to do this tbh
FREQUENCY = 2500000


class Noisemaker(object):
    """ A service which handles rendering noises from noisy things.

        .. versionadded:: 0.0.3-feature/noise

        Attributes:
            manager(object):        The :class:`manager <qtmud.Manager>` that
                                    is handling this service.
            noisy_things(set):      A set of all the things that have had
                                    this quality applied.
    """

    def __init__(self, manager):
        """
            .. versionadded:: 0.0.3-feature/noise
        """
        self.manager = manager
        self.noisy_things = set()

    def add(self, thing):
        """
            .. versionadded:: 0.0.3-feature/noise

            Parameters:
                thing(object):      The thing to add to Noisemaker's set of
                                    noisy_things
            Returns:
                bool: True if thing is successfully added, otherwise False.
        """
        return self.noisy_things.add(thing)

    def tick(self, events=False):
        """ randomly cause things to make noise

            .. versionadded:: 0.0.3-feature/noise

            When tick()ed by the manager, Noisemaker iterates through its set 
            of noisy_things and, based on FREQUENCY, has a chance of sending 
            a random noise to things near the noisy thing. Noises are split 
            up by the method required to observe them, such as 'look' or 
            'listen'.

            If a noise is triggered, it send()s it to everything in the noisy 
            thing's :attr:`contents 
            <qtmud.qualities.container.Container.contents>`if applicable, 
            and everything in the noisy thing's :attr:`location
            <qtmud.qualities.physical.Physical.location>`.
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
