""" Game library
    
    .. moduleauthor: emsenn <morgan.sennhauser@gmail.com>
    
    .. versionadded:: 0.0.1
    .. versionchanged:: 0.0.1-feature/environments
        added Tavern, Village
    .. versionchanged:: 0.0.1-features/parser
        added a Field
    
    Testing for potential game library - don't expect good documentation here.
"""

from qtmud.qualities import Container, Room, Renderable

class Tavern(object):
    """ Ye Olde Tavern
    
        .. versionadded:: 0.0.1-feature/environments
    """
    def __init__(self):
        return
    
    def apply(self, thing):
        """ turn a thing into a Tavern
        
            .. versionadded:: 0.0.1-features/environments
            .. versionchanged:: 0.0.2-features/parser
                Added explicit use of Container quality.
        """
        tavern = thing.manager.add_qualities(thing, [Room, 
                                                     Container,
                                                     Renderable])
        tavern.name = 'Ye Olde Tavern'
        tavern.description = 'A tavern so normal, it requires no description.'
        tavern.exits = { 'outside' : Village }
        return tavern
        
class Village(object):
    """ A little village.

        .. versionadded:: 0.0.1-features/environments
        
    """
    def __init__(self, **kw):
        super(Village, self).__init__(**kw)
        return
    
    def apply(self, thing):
        village = thing.manager.add_qualities(thing, [Room,
                                                      Container,
                                                      Renderable])
        village.name = 'Village Center'
        village.description = ('The center of a small village. Really just '
                               'a tavern in a field, for now.')
        village.exits = { 'inside' : Tavern,
                          'field' : Field }
        return village

class Field(object):
    """ An empty field.
    
        .. versionadded:: 0.0.1-features/parser
    """
    def __init__(self, **kw):
        super(Field, self).__init__(**kw)
        return
    
    def apply(self, thing):
        field = thing.manager.add_qualities(thing, [Room,
                                                    Container,
                                                    Renderable])
        field.name = 'Empty Field'
        field.description = ('A variety of grasses are growing in this '
                             'unused field. You can see a village a short '
                             'way off.')
        field.exits = { 'village' : Village }
        return field
