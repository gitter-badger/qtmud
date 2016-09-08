## run commands through manager always?

calling command functions directly sometimes means the command happens before 
the next tick. whoops.

## physical descriptions
it'd be nice if the description to render it were:
        output = '{name}\n\n{visual_desc}'.format(**locals())
        client.send(output)
or similar - basically, have it be a string where variables are replaced, 
so users can format their own output.
    
## implement __slots__
 
it'd help save on memory in the long term if things used `__slots__` for 
their qualities, but tihs should probably be done before much work is done 
in serializing the data

## persistence

how are user accounts and other necessary things going to be persistent?
        class Persistence:
        
            def set_quality(self, quality, value):
                if quality in self.__slots__:
                    # save function
                else:
                    object.__setattr__(self,quality, value)
            
            def apply(self, thing):
                thing.__setattr_ = self.set_quality
                
(no clue if that would work lol)
It'd be really great if whatever the game saved as was the same format as 
the library, so admin could just use the latest save *as* the library the 
next time the engine started.

## rooms/movement



add syntax exception? (rewrite whole command thing)

## restructure command parser:
put commands inside qualities - Client quality gives you echo and set, 
Sight gives you look, Physical gives you move - if you're a thing with the 
Commandable quality?

        class Commandable
    
        ...
            
            def apply(self, thing):
                ...
                thing.commands = []
                
                
        class Client
        
        ...
        
            def apply(self, thing):
                ...
                if hasattr(thing.commands): thing.commands.append('echo','set')

This would mean that Commandable would have to come first when you're telling
`manager` to new_thing(Qualities). that might be bad for long term design, an 
implicit hierarchy like that, but it's pretty straightforward, qualities are 
applied in the order they're written. Actually could probably have apply() check 
another fuction like add_commands so that you could do something like

        foreach quality in thing.qualities:
            quality.add_commands(thing)
