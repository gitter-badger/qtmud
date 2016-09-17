# TODO

Roughly split up by the domain they're for:

* [Manager](#manager)
* [Things](#things)
* [Services](#services)
* [Qualities](#qualities)
* [Library](#library)
* [Documentation](#documentation)

## MANAGER


## THINGS

* add use of \_\_slots\_\_


## SERVICES


### MUDSocket

* things that disconnect aren't removed from the game!

### Parser

* deal with not direct <verb> <subject> commands


### Noise

* Random messages that appear every so often from different things. A 
  crowded street might have a noise of 
  "The people push in on you from all sides," a vendor might have a 
  noise of "Buy your beets here, fresh beets!"
  
* How to organize these within the object - should it just be a part of 
  the Renderable quality? That probably makes the most sense.

* How to determine when to fire them off? Service that has a list of all
  the tickables? Probably the easiest, if not the most logical.

## QUALITIES

### Client

* prompt attribute, set what to be sent after scenes are send()'d


### Commandable

* split commandable in its own quality from clients.
* aliases


### Persistence 

* if a thing is a \_\_slot\_\_'d attribute, it is persistent. what does 


## LIBRARY


## DOCUMENTATION

* add a glossary