""" Yeolde RPG World

    .. moduleauthor:: emsenn <morgan.sennhauser@gmail.com>

    .. versionadded:: 0.0.3-feature/diceroller

    The world a player moves around in.
"""

# library imports
from qtmud.lib.yeolderpg.qualities import Place
from qtmud.lib.yeolderpg.npcs import AngusButtermew, RappScallion


class MoleInTheWall(object):
    def __init__(self):
        return

    def apply(self, thing):
        tavern = thing.manager.add_qualities(thing, [Place])
        tavern.name = ('Mole in the Wall')
        tavern.nametags = {'tavern'}
        tavern.description = ('The Mole in the Wall is perhaps the most '
                              'famous tavern in the places. Its location at a '
                              'strategic intersection has led to it becoming '
                              'the starting point for a great number of '
                              'stories.\n'
                              'The tavern lives in a mortared stone building, '
                              'which traps most of the heat from the sunken '
                              'hearth in the center of the room. Around the '
                              'hearth are an assortment of tables, '
                              'with frankly too many stools crammed up '
                              'against these. Sitting in these chairs are the '
                              'characters you\'d expect in any tavern. '
                              'Together, their activity maintains a '
                              'background level of noise that puts the room '
                              'well into \"cozy\" territory. Opposite the '
                              'doorway there\'s a counter stretched across '
                              'the room, serving as a bar. Behind the bar is '
                              'a closed door. Inconveniently adjacent to the '
                              'door is a dart board.')
        tavern.sounds = ('The overlapping chatter makes it impossible to focus '
                         'on what anyone is saying.')
        tavern.noises = {'listen': ['Something rattles in the ceiling.',
                                    'Someone\'s laugh picks up noticeably.',
                                    'An argument builds, before suddenly '
                                    'faltering.',
                                    'Someone shouts from the other room.'],
                         'look': ['The fireplace flares up for a moment.',
                                  'The chef bursts from the kitchen and '
                                  'delivers a plate to a table, leaving '
                                  'before you\'d have a chance to place an '
                                  'order.']}
        #####
        # put darts on bar
        # throw darts at dartboard
        # critical failure = you almost hit Rapp
        angus = tavern.manager.new_thing(AngusButtermew)
        tavern.add(angus)
        tavern.exits = {'kitchen': MoleKitchen}
        return tavern

class MoleKitchen(object):
    def __init__(self):
        return

    def apply(self, thing):
        kitchen = thing.manager.add_qualities(thing, [Place])
        kitchen.name = 'Mole in the Wall Kitchen'
        kitchen.description = ('The kitchen of the mall in the wall is in '
                               'stark contrast to the Mole in the Wall '
                               'itself. Gas lanterns brightly and evenly '
                               'light the room, with a gas stove set up '
                               'against one wall.')
        kitchen.noises = {'look': ['The burners on the stove seem to turn '
                                   'themselves on.']}
        rapp = kitchen.manager.new_thing(RappScallion)
        kitchen.add(rapp)
        return kitchen