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

* add use of __slots__


## SERVICES


### Parser

* adjectives aren't working right, if there's a "tiny red firetruck" and 
  a client looks for "tiny blue firetruck", the red one still shows up.


## QUALITIES


### Client

* prompt attribute, set what to be sent after scenes are send()'d


### Commandable

* split commandable in its own quality from clients.
* aliases


### Hearing

* with a listen command - then go change qualities.speaking.say() to make 
  it so things that can otherwise hear the say are listening.


### Persistence 

* if a thing is a __slot__'d attribute, it is persistent. what does 


### Physical

* split move() into move() and remove()


## LIBRARY


## DOCUMENTATION

* add a glossary