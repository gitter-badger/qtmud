import types

from qtmud.qualities.client import Client

class Speaking(object):
    def __init__(self, **kw):
        super(Speaking, self).__init__(**kw)
        return
    
    def say(self, thing, data):
        if not hasattr(thing, 'location'):
            thing.send('You cannot speak, for you have no environment.')
        for recipient in thing.location.contents:
                    if recipient in thing.manager.qualities[Client]:
                    # XXX change this to use the scheduler
                        recipient.send('{0} says: {1}'
                                       ''.format(thing.name, data))
    
    def apply(self, thing):
        try:
            thing.commands['say'] = types.MethodType(self.say, thing)
        except Exception as err:
            thing.manager.log.warning(err)
        return thing  
