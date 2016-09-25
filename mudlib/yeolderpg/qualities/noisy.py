from mudlib.yeolderpg.services import noisemaker


def apply(thing):
    spammer = thing
    noisemaker.noisy_things.add(spammer)
    spammer.noises = dict()
    return spammer
