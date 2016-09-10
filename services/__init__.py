""" Services are subscribed to events that they process each tick()

    .. moduleauthor: emsenn <morgan.sennhauser@gmail.com>

    .. versionadded:: 0.0.1
    
    Every action that occurs within :mod:`qtmud` should be handled by a 
    service. These services have tick() functions, which have events passed 
    to them each time the :class:`manager <qtmud.Manager>` :func:`tick()s 
    <qtmud.Manager.tick>`.
    
    Services expect to be instanced through the manager's :func:`add_service() 
    <qtmud.Manager.addservice>` method, which passes itself as an argument 
    to the service's ``__init__`` function.
    
    The rest of this file is used to demonstrate what a basic Service 
    looks like, so you have something to model your development off.
    
"""

from qtmud.services.mover import Mover
from qtmud.services.renderer import Renderer

class Service(object):
    """ **This class is for API documentation only. Not to be used.**
    
        .. versionadded:: 0.0.1
        .. versionchanged:: 0.0.1-features/parser
            Turned into API example
        
        Parameters:
            manager(object):        The instance of :class:`qtmud.Manager` 
                                    that is adding the Service through the 
                                    :func:`add_service() 
                                    <qtmud.Manager.add_service>` function.
        
        Attributes:
            manager(object):        whatever object is passed when instanced.
            subscriptions(list):    events (as strings) that this service 
                                    is subscribed to. In the tuples listed 
                                    in :attr:`qtmud.Manager.events`, these 
                                    would be the first element.
        
        A service registers its subscriptions with the :class:`manager 
        <qtmud.Manager>`, and then matching events are sent to the service's 
        ``tick()`` function.
    """
    def __init__(self, manager):
        """ 
            
            .. versionadded:: 0.0.1
            .. versionchanged:: 0.0.1-features/parsing
                Turned into API documentation.
                
            
        """
        super(Service, self).__init__()
        self.manager = manager
        self.subscriptions = []
        
        def tick(self, events=False):
            """ Handle one tick of gameplay
        
                .. versionadded:: 0.0.1-features/parser
            
                Parameters:
                    events(list):   set to False by default, expected to be 
                                    a list of tuples in the format of 
                                    [('event', {payload})]
            
                Returns:
                    bool:           False if the tick() fails for whatever 
                                    reason, otherwise true.
            
                Every time the qtmud :func:`tick()s <qtmud.Manager.tick>`, it 
                calls the ``tick()`` function of every service that has been 
                instanced through :func:`add_services() 
                <qtmud.Manager.add_services>`. If the event has any 
                :attr:`subscriptions <qtmud.services.Service.subscriptions>`, 
                matching :attr:`events <qtmud.Manager.events>` will be sent 
                as a list of tuples, where the first element is the keyword 
                the service is subscribed to, and the second element is the 
                payload of the event.
            """
            if events is False: return False
            for event, payload in events: #pylint: disable=unused-variable
                pass
            return True
