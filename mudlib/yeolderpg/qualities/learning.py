import types

import qtmud
from qtmud.services import parser


def apply(thing):
    learner = thing
    if hasattr(learner, 'commands'):
        learner.commands['learn'] = types.MethodType(learn_cmd, learner)
    return learner


def learn_cmd(learner, line):
    # TODO break this into learn() method
    line = parser.parse_line(line)
    qtmud.schedule('send',
                   recipient=learner,
                   text='Not a real command right now.')
    return True
