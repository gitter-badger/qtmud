""" sends output to client.

    .. moduleauthor: Morgan Sennhauser <morgan.sennhauser@gmail.com>

    .. versionadded:: 0.0.2-feature/textblob

    The Send service is :func:`subscribed <qtmud.Manager.subscribe>` to
    ``'send'`` events. Each event's payload should contain:

    * ``client`` - who the rendered frame is being sent to.
    * ``scene`` - the thing to be rendered.

    .. note:: Frames are rendered in the order they were :func:`scheduled
              <qtmud.Manager.schedule>`.

    The ``scene`` is expected to be a string, and is formatted and sent to
    the client.
"""


class Sender(object):
    """ The service for rendering frames for clients.

        .. versionadded:: 0.0.2-feature/textblob

        Parameters:
            manager(object):        automatically passed by
                                    :func:`add_services()
                                    <qtmud.Manager.add_services>`, the
                                    :class:`manager <qtmud.Manager>`

        Attributes:
            manager(object):        The same as the manager above.
            subscriptions(list):    The Sender service is subscribed to
                                    ``'send'`` :attr:`events
                                    <qtmud.Manager.events>`.
    """

    def __init__(self, manager):
        """
            .. versionadded:: 0.0.2-feature/textblob
        """
        self.manager = manager
        self.subscriptions = ['send']
        manager.subscribe(self, 'send')

    @staticmethod
    def tick(events=False):
        """ Sends a line to a thing, usually a client.

            .. versionadded:: 0.0.2-feature/nametags

            Paramters:
                events(list):       set to False by default, expected to
                                    be a list of tuples in the format of
                                    ``[('send', {payload})]``

                Returns:
                    bool:           False if the tick() fails or passes,
                                    otherwise true.

                The ``payload`` of each event is expected to have:

                * ``thing`` - representing the thing the frame will be
                  :func:`sent <qtmud.qualities.client.Client.send>` to.
                * ``scene`` - the text to be rendered and sent to the client.

                At the moment, this simply passes scene as an argument to
                the client's :func:`send <qtmud.qualities.client.Client.send>`
                function. While this might seem a roundabout way of sending
                information to clients, using
                ``manager.schedule('send', thing=client, scene=scene)
                instead of
                ``client.send(scene)``
                guarantees that clients won't be getting their output
                out-of-sync with what's actually happened.
        """
        if not events:
            return False
        for event, payload in events:
            thing = payload['thing']
            scene = payload['scene']
            if hasattr(thing, 'send'):
                thing.send(scene + '\n')
            else:
                thing.manager.log.warning('Tried to send a line to {} but they '
                                          'have no send() method.'
                                          ''.format(thing.identity))
        return True
