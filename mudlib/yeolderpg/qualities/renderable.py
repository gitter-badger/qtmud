""" description, sounds, smells

    .. moduleauthor:: emsenn <morgan.sennhauser@gmail.com>

    .. versionadded:: 0.1.0
"""


def apply(thing):
    """ make a thing renderable

        Parameter:
            thing(object):      the instance of :class:`qtmud.Thing` to be made
                                renderable.
        Returns:
            object:             thing, after being made renderable.

        Adds three strings to the thing: one for description, one for sounds,
        and one for smells.
    """
    renderable = thing
    renderable.description = str()
    renderable.sounds = str()
    renderable.smells = str()
    return renderable
