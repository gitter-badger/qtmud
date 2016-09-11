""" Game library
    
    .. moduleauthor: emsenn <morgan.sennhauser@gmail.com>
    
    .. versionadded:: 0.0.1
    .. versionchanged:: 0.0.1-feature/environments
        added Tavern, Village
    .. versionchanged:: 0.0.1-feature/parser
        added a Field
    .. versionchanged:: 0.0.2-feature/neverforgetholidayupdate
        added NineElevenMemorial ;_;7
    
    Testing for potential game library - don't expect good documentation here.
"""

from qtmud.qualities import Physical, Container, Room, Renderable

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
    
        .. versionadded:: 0.0.1-feature/parser
    """
    def __init__(self, **kw):
        super(Field, self).__init__(**kw)
        return
    
    def apply(self, thing):
        field = thing.manager.add_qualities(thing, [Room,
                                                    Container,
                                                    Renderable])
        field.name = 'Empty Field'
        field.description = ('This small field has a variety of short '
                             'grasses growing in it. Near the center, a '
                             'memorial sits. There is also a nearby village.')
        memorial = thing.manager.new_thing(NineElevenMemorial)
        field.add(memorial)
        field.exits = { 'village' : Village }
        return field


class NineElevenMemorial(object):
    """ A memorial to 9/11, a part of the Never Forget Holiday Update
    
        .. versionadded:: 0.0.2-feature/neverforgetholidayupdate
    """
    
    def __init__(self):
        """
            .. versionadded:: 0.0.2-feature/neverforgetholidayupdate
        """
        return

    def apply(self, thing):
        """
            .. versionadded:: 0.0.2-feature/neverforgetholidayupdate
        """
        memorial = thing.manager.add_qualities(thing, [Renderable])
        memorial.name = 'memorial'
        memorial.description = ('Two solid copper blocks rise up from the '
                                'ground. Wide bands of verdigris marble '
                                'their surface.')
        return memorial
