""" Gives the ability to listen to teach qualities to another thing

    .. moduleauthor:: emsenn <morgan.sennhauser@gmail.com>

    .. versionadded:: 0.0.3-feature/learning
"""


import types
from qtmud.services import Parser


class Teaching(object):
    """ Adds hearing to a thing it is applied to.

        .. versionadded:: 0.0.3-feature/learning
    """

    def __init__(self):
        """
            .. versionadded:: 0.0.3-feature/learning
        """
        return

    def teach(self, teacher, learner, line):
        """ Render sounds of the subject in line from listener's perspective.

            .. versionadded:: 0.0.3-feature/learning
        """
        if len(line.split(' ')) != 1:
            return False
        if line in teacher.teachable_qualities:
            learner.manager.add_qualities(learner,
                                          [teacher.teachable_qualities[line]])
        return True

    def apply(self, thing):
        """
            .. versionadded:: 0.0.3-feature/learning
        """
        if not hasattr(thing, 'teachable_qualities'):
            thing.teachable_qualities = dict()
        if not hasattr(thing, 'teach'):
            thing.teach = types.MethodType(self.teach, thing)
        if hasattr(thing, 'commands'):
            thing.commands['teach'] = types.MethodType(self.teach, thing)
        return thing
