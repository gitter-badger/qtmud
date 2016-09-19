""" Lets a thing randomly send messages to its environment.

    .. moduleauthor:: emsenn <morgan.sennhauser@gmail.com>

    .. versionadded:: 0.0.3-feature/noise
"""


import types
from qtmud.services.noisemaker import Noisemaker


class Noisy(object):
    """ Adds noises to a thing it is applied to.

        .. versionadded:: 0.0.3-feature/noise
    """

    def __init__(self):
        """
            .. versionadded:: 0.0.3-feature/noise

            noises = { 'look' : ['you see someone trip on the curb',
                                 'a balloon drifts overhead'],
                       'listen' : ['you hear someone fall']}
        """
        self.noises = dict()
        return

    def apply(self, thing):
        """
            .. versionadded:: 0.0.3-feature/learning
        """
        if not hasattr(thing, 'noises'):
            thing.noises = self.noises
        thing.manager.services[Noisemaker].add(thing)
        return thing
