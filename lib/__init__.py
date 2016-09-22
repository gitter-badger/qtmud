""" basic qtmud game libraries

    .. moduleauthor:: emsenn <morgan.sennhauser@gmail.com>

    .. versionadded:: 0.0.1
    .. versionchanged:: 0.0.1-feature/environments
        added Tavern, Village
    .. versionchanged:: 0.0.1-feature/parser
        added a Field
    .. versionchanged:: 0.0.2-feature/neverforgetholidayupdate
        added NineElevenMemorial ;_;7
    .. versionchanged:: 0.0.3-feature/diceroller
        split into yeolderpg library

    .. warning:: these things are in super early development, so should be seen
    more as test suites for the moment.

    These game libraries demonstrate the core qtmud API being used to create
    basic games.

    * :module:`Yeolde RPG <qtmud.lib.yeoldrpg>` is a stereotypical RPG. Think
      Zork.
    * :module:`Starhopper <qtmud.lib.starhopper>` is a space exploration game.
"""

from qtmud.qualities import Container, Renderable, Room
from qtmud.lib.starhopper import StarSystem
from qtmud.lib.yeolderpg.places import MoleInTheWall

class BackRoom(object):
    def __init__(self):
        return

    def apply(self, thing):
        back_room = thing.manager.add_qualities(thing, [Container, Renderable,
                                                    Room])
        back_room.name = 'Library Selection Room'
        back_room.description = 'From here you can enter any of the game ' \
                                'libraries.'
        back_room.exits = {'yeolde': MoleInTheWall,
                           'starhopper': StarSystem}
        return back_room