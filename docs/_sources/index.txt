.. qtmud documentation master file, created by
   sphinx-quickstart on Fri Sep  9 01:09:30 2016.
   You can adapt this file completely to your liking, but it should at least
   contain the root `toctree` directive.

    *This documentation is meant to be read as built by Sphinx. While it is 
    human-readable, there is a lot of markup that is used to cross-reference 
    the source code.*

qtmud documentation
###################

qtmud is an early alpha multiplayer text-based real-time virtual world simulator.

Clients (players) receive verbose descriptions of environments, objects, other 
players, and actions performed in qtmud's simulated world. In order to interact 
with the game engine, clients then type out things they want to do, such as 
``move outside`` or ``fight dragon``.

**Know what you're doing?**
If you want to dive on in, here's an overview of game mechanics with links 
to the relevant source code:
    In :mod:`qtmud`, a :class:`manager <qtmud.Manager>` controls 
    :mod:`services <qtmud.services>` which 
    :func:`subscribe <qtmud.Manager.subscribe>` to 
    :attr:`events <qtmud.Manager.events>`. When an event is 
    :func:`scheduled <qtmud.Manager.schedule>`, the 
    :class:`manager <qtmud.Manager>` calls it the next 
    :func:`tick <qtmud.Manager.tick>`. These 
    :attr:`events <qtmud.Manager.events>` act upon 
    :class:`things <qtmud.Thing>` which have had 
    :mod:`qualities <qtmud.qualities>` 
    :func:`applied <qtmud.qualities.Quality.apply>` to them.

**Less informed?**
Don't worry - one of the main focuses of qtmud is that it be easy to 
understand from just the documentation. If you read through the rest 
of this document, you'll end up with a good understanding of what happens 
when you run qtmud, and what's happening when players log in and do things.

But first, it might help to show you what gameplay in qtmud looks like, 
since you may not be familiar with `MUDs <https://www.wikiwand.com/en/MUD>`_.


Current Gameplay
================

.. image:: img/current_gameplay.png

[insert explanation of screenshot here]


Running qtmud
=============

Running qtmud is pretty simple. I'm going to assume any reader is on a 
*nix-type system and is able to do simple tasks like open a terminal.

Download & Configure
--------------------

The best way to get a copy of qtmud is to `clone the repository 
<https://help.github.com/articles/cloning-a-repository/>`_.

Once you've done that, you might want to edit the constants in the main
:mod:`qtmud` module, which is the ``__init__.py`` file in qtmud's main 
directory.

The four constants you might want to change right away are:

* :attr:`NAME <qtmud.NAME>` - the name that your MUD will go by
* :attr:`VERSION <qtmud.VERSION>` - the version of your MUD. Check 
  out :doc:`versioning` for more information.
* :attr:`HOST <qtmud.HOST>` - the hostname your MUD will serve over.
* :attr:`MUD_PORT <qtmud.MUD_PORT>` - the port your MUD will serve over.

Once you've got those set up, you're ready to start your MUD.

Starting qtmud
--------------

After you've set that up, use python3.5 to run execute ``./run.py``. You 
should see some output that looks similar to this:
::     
    instancing Manager()
    qtmud        INFO     Manager() instanced @ qtmud.manager
    qtmud        INFO     instancing services
    qtmud        INFO     instancing qtmud.manager.back_room

The first line, ``instancing Manager()``, creates an instance of 
:class:`qtmud.Manager`, a class which acts as the main game engine. If 
this were *Dungeons & Dragons*, :class:`qtmud.Manager` would be the 
Dungeon Master. Each moment of the game is divided into 
:func:`ticks <qtmud.Manager.tick>`, and each :func:`tick 
<qtmud.Manager.tick>`, :class:`qtmud.Manager` handles telling everything 
what it should be doing.

After ./run.py sets up :class:`qtmud.Manager`, it instances core game 
:mod:`services <qtmud.services>`. The current services are 
:class:`MUDSocket <qtmud.services.MUDSocket>` (for handling the sending and 
receiving of data from clients through a socket connection),
:class:`Mover <qtmud.services.Mover>` (for handling things moving between 
rooms), and :class:`Parser <qtmud.services.Parser>` (for handling input 
from clients.)

While each of these services handle very different parts of the game, they 
all work in much the same way, through three functions that 
:class:`qtmud.Manager` has:

* :func:`qtmud.manager.schedule` tells the manager to schedule 
  the `command` for next tick. For example, when a client logs in, 
  :class:`MUDSocket <qtmud.services.MUDSocket>` calls
  :func:`self.manager.schedule('move', thing=client, destination=Village) 
  <qtmud.Manager.schedule>` 
* :func:`qtmud.manager.subscribe` tells the manager that a 
  :mod:`service <qtmud.services>` wants to be informed about any relevant 
  :attr:`events <qtmud.Manager.events>`. For example, the 
  :class:`Parser <qtmud.services.Parser>` service does
  :func:`qtmud.subscribe(self, 'parse') <qtmud.Manager.subscribe>` when 
  it is instanced.
* :func:`qtmud.Manager.tick` relies on :func:`schedule 
  <qtmud.Manager.schedule>` and :func:`subscribe <qtmud.Manager.schedule>`. 
  For every service subscribed to an event, :func:`tick <qtmud.Manager.tick>` 
  sends every relevant event to that service. For example, on the tick after 
  the :class:`MUDSocket <qtmud.services.MUDSocket>` schedules the client to 
  be moved into the :class:`Village <qtmud.lib.Village>`, 
  :func:`tick <qtmud.Manager.tick>` tells the 
  :class:`Mover <qtmud.services.Mover>` to handle the actual movement.

After these services are instanced and their subscriptions properly set up, 
:class:`qtmud.Manager` sets up what is (inappropriately) being called the 
:attr:`qtmud.back_room`. The back room is simply the first room clients are 
put in when they log in. Instancing it now gives us an excuse to talk about how 
objects within qtmud work.

When you call :func:`qtmud.Manager.new_thing`, a few things happen. First, an object is instanced and given a unique identifier (available through 
thing.identity) and the capacity to have Qualities. Then, any qualities 
you list as an argument are applied to the thing.

In the case of the back room, we're making a new thing with the 
:class:`Village <qtmud.lib.Village>` quality. If you look at that class, 
you'll see when applied to a thing, it applies the 
:class:`Room <qtmud.qualities.Room>` and 
:class:`Renderable <qtmud.qualities.Renderable>` qualities.

* :class:`Room <qtmud.qualities.Room>` - Gives a village 
  :attr:`exits <qtmud.qualities.Room.exits>`, such as 
  ``{ 'inside' : Tavern }``, where Tavern is a quality to be applied to a 
  thing.
* :class:`Renderable <qtmud.qualities.Renderable>` - Gives the village 
  a :attr:`name <qtmud.qualities.Renderable.name>` and 
  :attr:`description <qtmud.qualities.Renderable.description>`.

Once the village has all the attributes it needs, it has them set to the 
specific values for that thing.

Logging In
----------

Now qtmud has instanced the manager, added services, and added the 
back_room, you can connect to your MUD. Open up your favorite MUD client 
(or just a terminal) and connect to your server. If you're using telnet, 
it'd be ``telnet://HOST:MUD_PORT``. (If you didn't change HOST or MUD_PORT 
earlier, the terminal command would be ``telnet localhost 5787``.

When the :class:`MUDSocket <qtmud.services.MUDSocket>` receives a new 
connection, like it did when you just telnet'd, it runs the following:
::
    client = self.manager.new_thing(Client, 
                                    Physical, 
                                    Renderable, 
                                    Container, 
                                    Sighted, 
                                    Speaking)

To learn specifically how the :func:`new_thing <qtmud.Manager.new_thing>` 
function works, read its source documentation. For now, it's enough to 
know it instances a new :class:`thing <qtmud.Thing>` and applies the listed 
:mod:`qualities <qtmud.qualities>` to it. Each quality listed is a class, 
imported from (in this case) :mod:`qtmud.qualities`. Each quality has an 
:func:`apply <qtmud.qualities.Quality.apply>` function, which adds attributes 
to the :class:`thing <qtmud.Thing>` that :func:`new_thing 
<qtmud.Manager.new_thing>` created.

We assigned a lot of qualities to our incoming client, let's see what they 
all do:

* :class:`Commandable <qtmud.qualities.Commandable>` lets future qualities 
  add :attr:`commands <qtmud.qualities.Commandable.commands>` to this 
  thing.
* :class:`Client <qtmud.qualities.Client>` tells the 
  :class:`MUDSocket <qtmud.services.MUDSocket>` what socket connection 
  the client is associated with, and because the client is 
  :class:`Commandable <qtmud.qualities.Commandable>`, give it the 
  :func:`echo <qtmud.qualities.Client.echo>`,
  :func:`whoami <qtmud.qualities.Client.whoami>`, and
  :func:`set <qtmud.qualities.Client.set>` commands.
* :class:`Physical <qtmud.qualities.Physical>` gives the client a 
  :attr:`location <qtmud.qualities.Physical.location>`, and because it's 
  :class:`commandable <qtmud.qualities.Commandable>`, the
  :func:`whereami <qtmud.qualities.Physical.whereami>` and 
  :func:`move <qtmud.qualities.Physical.move>` commands.
* :class:`Renderable <qtmud.qualities.Renderable>` gives the client a 
  :attr:`name <qtmud.qualities.Renderable.name>` and 
  :attr:`description <qtmud.qualities.Renderable.description>`.
* :class:`Container <qtmud.qualities.Container>` gives the client
  :attr:`contents <qtmud.qualities.Container.contents>` and the 
  :func:`inventory <qtmud.qualities.Container.inventory>` command.
* :class:`Sighted <qtmud.qualities.Sighted>` gives the client the 
  :func:`look <qtmud.qualities.Sighted.look>` command.
* :class:`Speaking <qtmud.qualities.Speaking>` gives the client the 
  :func:`say <qtmud.qualities.Speaking.say>` command.

The client started as a :class:`thing <qtmud.Thing>` with only an 
:attr:`identity <qtmud.Thing.identity>`, but by the end of 
:func:`new_thing <qtmud.Manager.new_thing>`, it has all the attributes a 
client needs to interact with the MUD. :class:`qtmud.Manager` also has recorded 
in :attr:`qtmud.Manager.qualities` that the keys for each Quality applied 
now have our client's thing as a value.
Clients, through their thing, can :func:`move 
<qtmud.qualities.Physical.move>` and :func:`say 
<qtmud.qualities.Speaking.say>` and :func:`look 
<qtmud.qualities.Sighted.look>` and all that other good stuff. Now that 
the client has all the proper :mod:`qualities <qtmud.qualities>`, 
:class:`MUDSocket <qtmud.services.MUDSocket>` can properly handle receiving data from and sending data to the client. Let's bring it back to services, by walking through what happens when you enter a command, such as ``say hello``.

Entering Commands
-----------------

Each event is broken up into two parts: the `event` and its `payload.` The 
`event` is what subscribers are set to look for. The `payload` is all the 
other data associated with the event.

When a client hits enter (letting :class:`MUDSocket 
<qtmud.services.MUDSocket>` know there's been a command entered,) 
:class:`MUDSocket <qtmud.services.MUDSocket>` does some basic parsing, 
breaking the command into its first word (``cmd``) and the rest of the 
line (``trailing``). Then, :class:`MUDSocket <qtmud.services.MUDSocket>` 
does:
:: 
        qtmud.manager.schedule('parse', # the event that will be scheduled
                               client=self.clients[conn],  # payload
                               cmd=cmd,                    # payload
                               trailing=trailing)          # payload

This means that on the next :func:`tick <qtmud.Manager.tick>`, 
:class:`qtmud.Manager` will tell every :mod:`service <qtmud.services>` 
who has :func:`subscribed <qtmud.Manager.subscribe>` to the ``parse`` event
everything in the ``payload``, through that service's own 
:func:`tick <qtmud.services.Service.tick>`. In this case, that means the 
:class:`Parser <qtmud.services.Parser>` will get told the ``client`` who 
issued the command, the ``cmd`` itself, and any ``trailing`` arguments the
``cmd`` might have.

So if the client enters the command ``say hello``, :class:`MUDSocket 
<qtmud.services.MUDSocket>` turns that input into
::
        qtmud.manager.schedule('parse',
                               client=self.clients[conn],
                               cmd='say'
                               trailing='hello)

On the next :func:`tick <qtmud.Manager.tick>`, :class:`qtmud.Manager` tells 
every :mod:`service <qtmud.services>` subscribed to ``'parse'`` about that event. Right now, the only service subscribed to ``'parse'`` is the 
:class:`Parser <qtmud.services.Parser>` service.

The :class:`Parser <qtmud.services.Parser>` service, like every other 
service, has its own :func:`tick <qtmud.services.Parser.tick>` function, 
which can be given a dict of `events`. If last tick 
:class:`MUDSocket <qtmud.services.MUDSocket>` scheduled the parse event for 
the client's ``say hello``, this tick the manager would pass :attr:`events 
<qtmud.Manager.events>` to the :class:`Parser <qtmud.services.Parser>`, 
looking something like this:
::
        [('parse', {'cmd': 'say',
                     'client': <qtmud.Thing object at 0x7f4dcd0e3a58>,
                     'trailing': 'say'}
        )]

From a Python perspective, `events` is a list of tuples, where the first 
element is the `event` and the second element is the `payload`.

What each service does with the events it receives is based on what the 
service accomplishes. The :class:`Mover <qtmud.services.Mover>` service 
uses the payload it receives to handle :func:`moving 
<qtmud.Qualities.Physical.move>` things in and out of :attr:`locations 
<qtmud.Qualities.Physical.location>`. The Parser service uses the payload 
to determine whether what the client input was a valid command, and if so, 
passes the rest of the payload off to that command. (If you remember from 
logging in, commands are added to the client by the qualities 
:class:`MUDSocket <qtmud.services.MUDSocket>` 
passed to :func:`new_thing <qtmud.Manager.new_thing>` when we logged in.) 

In the case of ``say hello``, the ``say`` command is added by the 
:class:`Speaking <qtmud.qualities.Speaking>` quality, which also added 
the :func:`say <qtmud.qualities.Speaking.say>` function, to be called when 
the command is used. :func:`say ,qtmud.qualities.Speaking.say>` is pretty 
simple - :func:`schedule <qtmud.Manager.schedule> an event with the 
:class:`Render <qtmud.services.Render>` service so every client in our 
:attr:`location <qtmud.qualities.Physical.location>` will have our message 
:func:`rendered <qtmud.services.Render.render>` during the next 
:func:`tick <qtmud.Manager.tick>`

Other commands work in much the same way. The ``move`` command is added by 
the :class:`Physical <qtmud.qualities.Physical>` quality, which has the 
func:`move <qtmud.qualities.Physical.move>` function. The ``look`` 
command is added by the :class:`Sighted <qtmud.qualities.Sighted>` quality, 
which has the :func:`look <qtmud.qualities.Sighted.look>` function.

Messing Around
--------------

Walking through what happens when you start qtmud and log in and 'say hello', 
we've touched on most of the core functions of the game. I'd suggest looking 
through the ./quality/ and ./services/ directories to see how more of qtmud's 
core features work. In the next section, we'll look in the ./lib/ directory, 
and explain how writing content for qtmud works.

Development
===========

There are two main ways to add content to qtmud. You can build services to 
respond to the events beings scheduled by things and other services, or 
you can build qualities to apply to things.

The latter, creating qualities, is probably a better starting point for 
learning how to work with qtmud. 

*there's no more explanation, come back later*

Dogma
-----

* every action should be scheduled and tick()ed - no intrafunction changes.


Versioning
----------

qtmud uses semantic versioning. check :doc:`versioning` for more.

Debugging
---------

By default, only INFO, WARNING and ERROR messages will show up on the console. 
A complete log, featuring every DEBUG message, is written to 
[debug.log](debug.log) (*Note: debug.log is overwritten at each boot.)

Contents:
 
.. toctree::
   :maxdepth: 2
 
Indices and tables
==================
 
* :ref:`genindex`
* :ref:`modindex`
* :ref:`search`

