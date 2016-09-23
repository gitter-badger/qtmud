import types


def apply(thing):
    container = thing
    container.contents = set()
    container.add = types.MethodType(add, container)
    container.contains = types.MethodType(contains, container)
    container.remove = types.MethodType(remove, container)
    return container


def add(container, *things):
    for thing in things:
        container.contents.add(thing)
        thing.location = container
    return True


def contains(container, thing):
    return thing in container.contents


def remove(container, thing):
    if thing in container.contents:
        return container.contents.remove(thing)
    return False