import qtmud


def move(thing, destination):
    if thing.location:
        thing.location.remove(thing)
    thing.location = destination
    thing.location.add(thing)
    return True
