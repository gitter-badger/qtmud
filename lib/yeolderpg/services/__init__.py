"""

    .. moduleauthor: Morgan Sennhauser <morgan.sennhauser@gmail.com>

    .. versionadded:: 0.0.3-feature/diceroller
"""

import random

from qtmud.qualities import Container, Physical, Renderable


class Death(object):
    def __init__(self, manager):
        """
            .. versionadded:: 0.0.3-feature/diceroller
        """
        self.manager = manager
        self.subscriptions = ['death']

    def tick(self, events=False):
        """
            .. versionadded:: 0.0.03-feature/diceroller
        """
        if events is False:
            return False
        for event, payload in events: #pylint: disable=unused-variable
            departed = payload['departed']
            # TODO: split this into Corpse quality
            corpse = departed.manager.new_thing(Container)
            #loot = corpse.manager.new_thing(Loot)
            #corpse.add(loot)
            if hasattr(departed, 'name'):
                corpse.manager.add_qualities(corpse, [Renderable])
                corpse.name = ('corpse of {}'.format(departed.name))
                corpse.description = ('This is the corpse of {}, may they '
                                      'rest in peace.'.format(departed.name))
            if hasattr(departed, 'location'):
                corpse.manager.add_qualities(corpse, [Physical])
                corpse.manager.schedule('move', thing=corpse,
                                        destination=departed.location)
                departed.manager.schedule('move', thing=departed,
                                          destination=None)
        return True

class Diceroller(object):
    def __init__(self):
        return

    @staticmethod
    def roll(dice_pool):
        roll = 0
        for dice in range(dice_pool):
            roll += random.choice([-1, 0, 1])
        return roll

    def tick(self, events=False):
        return True