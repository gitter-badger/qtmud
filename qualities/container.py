""" A Container has contents that can be added to or removed from

    .. versionadded:: 0.0.1-features/parser

    From an abstract standpoint, many different things could be a 
    Container. A cardboard box would obviously be a Container, but 
    so would an office. The difference is that a box would also be 
    :class:`Physical <qtmud.qualities.physical.Physical>`, while an 
    office is more of an abstract thing, so would lack that particular 
    Quality.

    All a container really does is give a :class:`thing <qtmud.Thing>` 
    the ability to have an inventory - referred to in the game as the 
    thing's :attr:`contents <qtmud.qualities.container.Container.contents>`. 
    These contentsmight be manipulated in a lot of ways - the 
    :class:`Mover <qtmud.services.mover.Mover>` uses it to, well, move 
    things, and Sight frequently means looking at a things inventory.
"""


import types


class Container(object):
    """ Containers gain contents and methods for handling that.

        .. versionadded:: 0.0.1-feature/parser
        .. versionchanged:: 0.0.2-feature/renderer
        .. versionchanged:: 0.0.2-feature/inventory
            Added inventory() function and matching command.
 
        Attributes:
            contents(list):         The contents of the :class:`Thing 
                                    <qtmud.Thing>` has been applied to.
                                    Meant to have other things 
                                    :func:`added 
                                    <qtmud.qualities.container.Container.add>`
                                    to it.
    """
    def __init__(self):
        """
            .. versionadded:: 0.0.1-feature/parser
        """
        self.contents = []
        return
    
    @staticmethod
    def add(container, *things):
        """ Adds thing to the contianer's contents if thing isn't there.

            .. versionadded:: 0.0.1-feature/parser
            .. versionchanged:: 0.0.2-feature/inventory
                Added proper returns
            .. versionchanged:: 0.0.2-feature/textblob
                changed to static method
            
            Parameter:
                container(object):      The :class:`thing <qtmud.Thing>`
                                        that will have somethinng added to
                                        it.
                thing(object):          The :class:`thing <qtmud.Thing>`
                                        that will be added to the container.
            Return:
                bool:                   True if ``thing`` is successfully
                                        added to to the ``contents`` of
                                        the ``container``.
        """
        for thing in things:
            if thing not in container.contents:
                container.contents.append(thing)
        return True
    
    @staticmethod
    def contains(container, thing):
        """ Check if thing is in the contents of container.
        
            .. versionadded:: 0.0.1-feature/parser
            .. versionchanged:: 0.0.2-feature/textblob
                changed to static method
            
            Parameter:
                container(object):      The :class:`thing <qtmud.Thing>`
                                        that'll have its contents searched.
                thing(object):          The :class:`thing <qtmud.Thing>`
                                        that will be added to the container.
            Return:
                bool:                   True if ``thing`` is in ``container``'s
                                        ``contents``.
        """
        return thing in container.contents
    
    @staticmethod
    def remove(container, thing):
        """ removes a thing from another thing
        
            .. versionadded:: 0.0.1-feature/parser
            .. versionchanged:: 0.0.2-feature/inventory
                Proper returns added.
            .. versionchanged:: 0.0.2-feature/textblob
                changed to static method
            
            Parameters:
                container(object):      the container from which thing 
                                        will be removed.
                thing(object):          the thing to be removed from the 
                                        container.
            
            Returns:
                bool:                   True if ``thing`` is successfully
                                        removed from the ``container``.
        """
        if thing in container.contents:
            return container.contents.remove(thing)
        return False
    
    @staticmethod
    def inventory(searcher, line=''):
        """ 
            .. versionadded:: 0.0.2-feature/inventory
            .. versionchanged:: 0.0.2-feature/nametags
                Removed unnecessary container argument and replaced it with 
                more standard ``trailing``
            .. versionchanged:: 0.0.2-feature/textblob
                changed to static method

            Parameters:
                searcher(object):   The thing which is trying to check 
                                    the container's inventory.
                line(str):          Unused, for now.
            Returns:
                list:               the ``contents`` of the ``searcher``

            ``inventory()`` is essentially an alias for ``searcher.contents``,
            but will also schedule a rendering of the ``searcher``'s contents 
            if the ``searcher`` has a :func:`send 
            <qtmud.qualities.client.Client.send>` function.

            Examples:
                From the backend:
                
                    >>> satchel = manager.new_thing(Container)
                    >>> oodil = manager.new_thing(Physical)
                    >>> manager.schedule('move',
                    >>>                  thing=oodil
                    >>>                  destination=satchel)
                    >>> satchel.inventory(satchel)
                    [<qtmud.Thing object at 0xb69c7ad0>]                    
                
                From in-game:
                    
                    >>> inventory
                    You're holding:
                    ( apple pie, sword )
        """
        if hasattr(searcher, 'send'):
            # TODO: add "inventory desk in corner" checks
            if hasattr(searcher, 'contents'):
                scene = 'You\'re holding:\n('
                for content in searcher.contents:
                    if hasattr(content, 'name'):
                        scene += (content.name+', ')
                scene += ')'
            else:
                scene = 'You can\'t hold things!'
            searcher.manager.schedule('send', thing=searcher, scene=scene)
        return searcher.contents

    def apply(self, thing):
        """ Adds contents and supporting functions.
        
            .. versionadded:: 0.0.1-feature/parser
            .. versionchanged:: 0.0.2-feature/inventory
                Now applies ``inventory`` function and if ``thing`` is
                commandable, the ``inventory`` command.
        
            Parameters:
                thing(object):  The thing that is being turned into a
                                container.
            
            Returns:
                object:         The thing, after it's turned into a
                                container.
        """
        if not hasattr(thing, 'contents'):
            thing.contents = []
        if not hasattr(thing, 'add'): 
            thing.add = types.MethodType(self.add, thing)
        if not hasattr(thing, 'contains'):
            thing.contains = types.MethodType(self.contains, thing)
        if not hasattr(thing, 'inventory'):
            thing.inventory = types.MethodType(self.inventory, thing)
        if not hasattr(thing, 'remove'):
            thing.remove = types.MethodType(self.remove, thing)
        if hasattr(thing, 'commands'):
            thing.commands['inventory'] = types.MethodType(self.inventory,
                                                           thing)
        return thing
