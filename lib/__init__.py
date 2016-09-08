""" Game library

    .. module:: qtmud.lib
        :synopsis: library of game resources.
    
    .. moduleauthor: Morgan Sennhauser <morgan.sennhauser@gmail.com>
    .. version added:: 0.0.1
    
    Testing for potential game library 
"""

from qtmud.qualities import Room, Renderable

class Tavern(object):
    """ Gives a thing the qualities of a Room
    """
    def __init__(self, **kw):
        super(Tavern, self).__init__(**kw)
        return
    
    def apply(self, thing):
        tavern = thing.manager.add_qualities(thing, [Room, Renderable])
        tavern.name = 'Ye Olde Tavern'
        tavern.description = 'A tavern so normal, it requires no description.'
        tavern.exits = { 'outside' : Village }
        return thing
        
class Village(object):
    def __init__(self, **kw):
        super(Village, self).__init__(**kw)
        return
    
    def apply(self, thing):
        village = thing.manager.add_qualities(thing, [Room, Renderable])
        village.name = 'Village Center'
        village.description = ('The center of a small village. Really just '
                               'a tavern in a field, for now.')
        village.exits = { 'inside' : Tavern,
                          'field' : Field }
        return thing

class Field(object):
    def __init__(self, **kw):
        super(Field, self).__init__(**kw)
        return
    
    def apply(self, thing):
        field = thing.manager.add_qualities(thing, [Room, Renderable])
        field.name = 'Empty Field'
        field.description = ('A variety of grasses are growing in this '
                             'unused field. You can see a village a short '
                             'way off.')
        field.exits = { 'village' : Village }
