""" A basic service

    .. module:: qtmud.service
        :synopsis: handles the input from clients
    
    .. moduleauthor: Morgan Sennhauser <morgan.sennhauser@gmail.com>
    .. version added:: 0.0.1
    
    Your most basic service has two things: the manager it's associated with 
    and subscriptions, events that it's looking out for. This gives an object 
    both of those things.
"""

class Service(object):
    """ Most basic service. Does nothing itself.
    """
    def __init__(self, manager, **kw):
        """ add manager and subscriptions variables to the service.
        """
        super(Service, self).__init__(**kw)
        self.manager = manager
        self.subscriptions = []
