""" Service for moving things from one location to another.
    
    .. moduleauthor: Morgan Sennhauser <morgan.sennhauser@gmail.com>
    
    .. version added:: 0.0.1
    
    The Mover handles moving :class:`things <qtmud.Thing>` with the 
    :class:`Physical <qtmud.qualities.physical.Physical>` quality from one 
    :attr:`location <qtmud.qualities.physical.Physical.location>` to another.
"""


class Mover(object):
    """ The service for moving Physical things into and out of locations.
    
        .. versionadded:: 0.0.1-features/environments
        
        Parameters:
            manager(object):        automatically passed by 
                                    :func:`add_services()  
                                    <qtmud.Manager.add_services>`, the 
                                    :class:`manager <qtmud.Manager>`
        
        Attributes:
            manager(object):        The same as the manager above.
            subscriptions(list):    The Mover service is subscribed to 
                                    ``'move'`` :attr:`events 
                                    <qtmud.Manager.events>`.
    """
    def __init__(self, manager):
        """ subscribe to the 'move' event.
        """
        self.manager = manager
        self.subscriptions = ['move']
        
    def tick(self, events=False):
        """ Moves Physical things from one location to another.
        
                .. versionadded:: 0.0.1-features/environments
            
                Parameters:
                    events(list):   set to False by default, expected to be 
                                    a list of tuples in the format of 
                                    [('move', {payload})]
            
                Returns:
                    bool:           False if the tick() fails for whatever 
                                    reason, otherwise true.
            
                The ``payload`` of each event is expected to have a few 
                keys: the ``thing`` that will be moved, and its 
                ``destination``. Both ``thing`` and ``destination`` are 
                expected to be objects. First ``thing`` is :func:`removed 
                <qtmud.qualities.container.Container.remove>` 
                from its :attr:`location 
                <qtmud.qualities.physical.Physical.location>`. Then ``thing`` 
                is :func:`added <qtmud.qualities.container.Container.add>`
                to a the :attr:`contents 
                <qtmud.qualities.container.Container.contents>` of the 
                ``destination``.
            """
        if events is False:
            return False
        for event, payload in events: #pylint: disable=unused-variable
            thing = payload['thing']
            destination = payload['destination']
            try:
                thing.location.contents.remove(thing)
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
                self.manager.log.debug('Mover service did not receive '
                                       'destination, leaving %s without '
                                       'a location', thing.identity)
            else:
                thing.location = destination
                thing.location.add(thing)
        return True
