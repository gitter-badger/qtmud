from qtmud.qualities import Teaching

from qtmud.lib.yeolderpg.qualities import NPC

class AngusButtermew(object):
    def __init__(self):
        return

    def apply(self, thing):
        angus = thing.manager.add_qualities(thing, [NPC])
        angus.name = 'Angus Buttermew'
        angus.nametags = {'angus', 'bartender', 'barkeep'}
        angus.description = ('Angus Buttermew is the bartender at the Mole in '
                             'the Wall, and looks the part.')
        angus.noises = {'listen': ['Angus laughs in response to a customer.'],
                        'look': ['Angus moves from one end of the bar to the '
                                 'other.']}
        return angus

class RappScallion(object):
    def __init__(self):
        return

    def apply(self, thing):
        rapp = thing.manager.add_qualities(thing, [NPC, Teaching])
        rapp.name = 'Rapp Scallion'
        rapp.nametags = {'rapp'}
        rapp.description = ('Rapp Scallion is a gaunt, tall man. Dressed in '
                            'orange, with a yellowed and stained apron over '
                            'his street clothes. The only part of his outfit '
                            'which isn\'t stained is his chef hat, '
                            'which sits, bright white, on his bald head.')
        rapp.noises = {'listen': ['Rapp murmurs, "Friend once told me, '
                                  '\'Happinness is a warm manatee.\'"',
                                  '"Kiss me; I\'ve got scurvy! Ahaha," Rapp '
                                  'laughs.',
                                  '"Violets are blue, roses are red, We\'re '
                                  'coming aboard, prepare to eat lead!" Rapp '
                                  'says, sing-song.'],
                       'look': ['Rapp moves from one side of the kitchen to '
                                'another, preparing the next meal.']}
        return rapp