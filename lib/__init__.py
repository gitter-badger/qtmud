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
    def __init__(self):
        return
    
    def apply(self, thing):
        village = thing.manager.add_qualities(thing, [Room,
                                                      Container,
                                                      Renderable])
        village.name = 'Center of Ye Olde Village'
        village.description = ('The center of a small village. Really just '
                               'a tavern in a field, for now.')
        tavern = thing.manager.new_thing(Renderable)
        tavern.update({'name': 'Ye Olde Tavern',
                       'description': 'Despite the name, Ye Olde Tavern '
                                      'appears to have been built quite '
                                      'recently. Its facade is built of pine '
                                      'logs, and the door is wide open, so '
                                      'one could just "move inside".'})
        logs = thing.manager.new_thing(Renderable)
        logs.update({'name': 'fresh hewn pine logs',
                     'description': 'The walls of the Ye Olde Tavern are '
                                    'made from pine, so freshly cut they '
                                    'look sticky to the touch.'})
        door = thing.manager.new_thing(Renderable)
        door.update({'name': 'open door',
                     'description': 'The door to Ye Olde Tavern is wide open, '
                                    'making it seem like an inviting place.'})
        village.add(tavern, logs, door)
        village.exits = { 'inside' : Tavern,
                          'field' : Field }
        return village

class Field(object):
    """ An empty field.
    
        .. versionadded:: 0.0.2-feature/parser
    """
    def __init__(self):
        return
    
    def apply(self, thing):
        field = thing.manager.add_qualities(thing, [Room,
                                                    Container,
                                                    Renderable])
        field.update({'name': 'Memorial Field',
                      'description': 'This field is just outside Ye Olde '
                                     'Village. There are two copper pillars '
                                     'erected (hehe) here.'})
        memorial = thing.manager.new_thing(Renderable)
        memorial.update({'name': '9/11 Memorial',
                         'nametags': {'pillars'},
                         'adjectives': {'copper', 'solid', 'marbled'},
                         'description': 'Two solid copper blocks rise up from '
                                        'the ground. Wide bands of verdigris '
                                        'marble their surface.'})
        field.add(memorial)
        field.exits = { 'village' : Village }
        return field
