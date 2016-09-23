import types


def teach(teacher, learner, skill):
    if skill in teacher.teachable_qualities:
        learner.manager.add_qualities(learner,
                                      [teacher.teachable_qualities[skill]])
    return True


def apply(thing):
    if not hasattr(thing, 'teachable_qualities'):
        thing.teachable_qualities = dict()
    if not hasattr(thing, 'teach'):
        thing.teach = types.MethodType(teach, thing)
    return thing
