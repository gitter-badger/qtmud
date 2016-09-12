## split commandable into its own quality

## create hearing quality, revise say to match

## client aliases

## thing.search('string') that looks for a thing with the matching nametag?

## add glossary to documentation

## split movement into remove and add

## how to handle the assumed uniqueness of rooms?
best i think would be to replace the Class that's set to a direction's
value with the oject (thing) it actually wants, once it's cloned. That way 
there's no weird "this thing is unique" code spaghetting around - don't 
assume anything is going to be unique.

it'd clean up the main folder a bit, which might be nice since there 
will end up being lots of config files there.

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
