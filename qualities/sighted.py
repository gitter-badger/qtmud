import types

class Sighted(object):
    def __init__(self, **kw):
        super(Sighted, self).__init__(**kw)
        return
    
    def look(self, thing, target):
        render = ('- {0} -\n'
                  '{1}\n'
                  '[ '.format(thing.location.name,
                               thing.location.description))
        for exit in thing.location.exits:
            render += (exit+', ')
        render += ' ]\n( '
        for content in thing.location.contents:
            render += (content.name+', ')
        render += ' )'
        thing.send(render)
        
    
    def apply(self, thing):
        try:
            thing.commands['look'] = types.MethodType(self.look, thing)
        except Exception as err:
            thing.manager.log.warning(err)
        return thing
