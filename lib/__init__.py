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

        .. versionadded:: 0.0.1-feature/environments
        .. versionchanged:: 0.0.2-feature/parser
            added explicit use of the Container quality.
        .. versionchanged:: 0.0.2-feature/nametags
            added some Renderables.        
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
        tavern = thing.manager.new_thing(Renderable)
        tavern.name = 'Ye Olde Tavern'
        tavern.description = ('The Ye Olde Tavern is indeed quite olde - I '
                              'mean old. In fact, it is the oldest thing '
                              'in existence. Yet somehow, the pine logs '
                              'its walls are built with still look '
                              'fresh-hewn. There\'s a door in the facade, '
                              'so you could \'move inside\'.')
        logs = thing.manager.new_thing(Renderable)
        logs.name = 'fresh hewn pine logs'
        logs.description = ('The walls of the Ye Olde Tavern are made from '
                            'pine, so freshly cut they look sticky to the '
                            'touch.')
        door = thing.manager.new_thing(Renderable)
        door.name = 'open door'
        door.description = ('The door to Ye Olde Tavern is wide open, making '
                            'it seem like an inviting place.')
        village.add(tavern, logs, door)
        village.exits = { 'inside' : Tavern,
                          'field' : Field }
        return village

class Field(object):
    """ An empty field.
    
        .. versionadded:: 0.0.2-feature/parser
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
