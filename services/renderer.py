""" renders client output

    .. moduleauthor: Morgan Sennhauser <morgan.sennhauser@gmail.com>

    .. version added:: 0.0.2-feature/renderer
    
    The Renderer service is :func:`subscribed <qtmud.Manager.subscribe>` to 
    ``'render'`` events. Each event's payload should contain:
    
    * ``client`` - who the rendered frame is being sent to.
    * ``scene`` - the thing to be rendered.
    
    .. note:: Frames are rendered in the order they were :func:`scheduled 
              <qtmud.Manager.schedule>`.
    
    The ``scene`` is expected to be a string, and is formatted and sent to 
    the client.
"""

class Renderer(object):
    """ The service for rendering frames for clients.
    
        .. versionadded:: 0.0.2-feature/renderer
        
        Parameters:
            manager(object):        automatically passed by 
                                    :func:`add_services()  
                                    <qtmud.Manager.add_services>`, the 
                                    :class:`manager <qtmud.Manager>`

        Attributes:
            manager(object):        The same as the manager above.
            subscriptions(list):    The Renderer service is subscribed to 
                                    ``'render'`` :attr:`events 
                                    <qtmud.Manager.events>`.
    """
    
    def __init__(self, manager):
        """
            .. versionadded:: 0.0.2-feature/renderer
        """
        self.manager = manager
        self.subscriptions = ['render']
        manager.subscribe(self, 'render')
    
    def tick(self, events=False):
        """ Renders each frame in events for the respective client.
        
            .. versionadded:: 0.0.2-feature/renderer
        
            Paramters:
                events(list):       set to False by default, expected to 
                                    be a list of tuples in the format of 
                                    ``[('render', {payload})]``
                
                Returns:
                    bool:           False if the tick() fails or passes, 
                                    otherwise true.
                
                The ``payload`` of each event is expected to have:
                
                * ``client`` - representing the client the frame will be 
                  :func:`sent <qtmud.qualities.client.Client.send>` to.
                * ``scene`` - the text to be rendered and sent to the client.
                
                At the moment, this simply passes scene as an argument to 
                the client's :func:`send <qtmud.qualities.client.Client.send>`
                function. While this might seem a roundabout way of sending 
                information to clients, using 
                ``manager.schedule('render', client=client, scene=scene)
                instead of
                ``client.send(scene)``
                guarantees that clients won't be getting their output 
                out-of-sync with what's actually happened.
        """
        if not events:
            return False
        for event, payload in events:
            client = payload['client']
            scene = payload['scene']
            client.send(scene+'\nWhat will you do?\nI will > ')
        return True
