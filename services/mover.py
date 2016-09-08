""" moves things from one location to another

    .. module:: qtmud.services.mover
        :synopsis: moves things from one location to another
    
    .. moduleauthor: Morgan Sennhauser <morgan.sennhauser@gmail.com>
    .. version added:: 0.0.1
    
    Mover just moves things from one location to another. To be honest, 
    this might not even work how I think it does, there's no test case for 
    it right now.
"""

from qtmud.services import Service

class Mover(Service):
    """ The movement service.
        Subscribed to 'move' events.
        
        Expecting thing, destination in payload.
    """
    def __init__(self, manager, **kw):
        """ subscribe to the 'move' event.
        """
        super(Mover, self).__init__(manager, **kw)
        self.subscriptions.append('move')
        
    def tick(self, events=False):
        """ Move things out of their old locations, if applicable, then 
            move them into their new location.
        """
        if events is False:
            return False
        for event, payload in events: #pylint: disable=unused-variable
            thing = payload['thing']
            destination = payload['destination']
            try:
                thing.location.contents.remove(thing)
            # XXX Rewrite this exception to properly handle things
            except AttributeError:
                self.manager.log.debug('tried to remove %s from a location '
                                       'but %s was not in that location', 
                                       thing.identity, thing.identity)
            except Exception as err:
                self.manager.log.warning('unexpected exception caught '
                                         'when trying to remove %s '
                                         'from their location:\n\n%s', 
                                         thing.identity, err.__class__)
            if destination is None:
                pass
            else:
                # XXX Expecting object, need to account for other possibilities,
                # how to load rooms.
                thing.location = destination
                thing.location.add(thing)
        return True
