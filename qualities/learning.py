""" Gives the ability to listen to learn new qualities

    .. moduleauthor:: emsenn <morgan.sennhauser@gmail.com>

    .. versionadded:: 0.0.3-feature/learning
"""


import types
from qtmud.services import Parser


class Learning(object):
    """ Adds hearing to a thing it is applied to.

        .. versionadded:: 0.0.3-feature/learning
    """

    def __init__(self):
        """
            .. versionadded:: 0.0.3-feature/learning
        """
        return

    def learn(self, learner, line):
        """ Render sounds of the subject in line from listener's perspective.

            .. versionadded:: 0.0.3-feature/learning
        """
        line = Parser.parse_line(learner, line)
        if 'subject' not in line:
            learner.manager.schedule('send',thing=learner,
                                     scene = ('syntax: learn <quality> '
                                              'from <thing>'))
            return False
        if len(line['pnp_clauses']) == 1 and line['pnp_clauses'][0][0] in [
            'from']:
            teachers = learner.search(line['pnp_clauses'][0][2])
            if teachers and len(teachers) == 1:
                if hasattr(teachers[0], 'teach'):
                    teachers[0].teach(learner, line['subject'])
        return True

    def apply(self, thing):
        """
            .. versionadded:: 0.0.3-feature/learning
        """
        if not hasattr(thing, 'learn'):
            thing.listen = types.MethodType(self.learn, thing)
        if hasattr(thing, 'commands'):
            thing.commands['learn'] = types.MethodType(self.learn, thing)
        return thing
