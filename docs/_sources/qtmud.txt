qtmud package
=============

qtmud is an early-alpha :term:`MUD` engine. Using an event subscription
model, qtmud handles the interactions between :class:`Things <qtmud.Thing>`
which been built using :mod:`builders <qtmud.builders>` to create arbitrarily
complex game objects.

Right now that doesn't mean very much - Things are relatively simple, and the
only real quality that qtmud can apply is to turn a generic thing into a
client. This basic framework is used by :term:`mudlibs <mudlib>` to create
full games, however. Check out :doc:`Starhopper <starhopper>` for one example.


Module contents
---------------

.. automodule:: qtmud
    :members:
    :undoc-members:
    :show-inheritance:


Submodules
----------

qtmud's submodules have been broken up into a few rough groups:

* Builders make or modify game objects
* Cmds are player-entered commands
* Parser isn't currently used, but houses NLTK functions
* services are constantly-running game services
* Subscriptions are events qtmud.tick() fires to


qtmud.builders module
---------------------

.. automodule:: qtmud.builders
    :members:
    :undoc-members:
    :show-inheritance:

qtmud.cmds module
-----------------

.. automodule:: qtmud.cmds
    :members:
    :undoc-members:
    :show-inheritance:

qtmud.parser module
-------------------

.. automodule:: qtmud.parser
    :members:
    :undoc-members:
    :show-inheritance:

qtmud.services module
---------------------

.. automodule:: qtmud.services
    :members:
    :undoc-members:
    :show-inheritance:

qtmud.subscriptions module
--------------------------

.. automodule:: qtmud.subscriptions
    :members:
    :undoc-members:
    :show-inheritance:

qtmud.txt module
----------------

.. automodule:: qtmud.txt
    :members:
    :undoc-members:
    :show-inheritance:


Glossary
--------

These are the terms which have a specific meaning under qtmud

.. glossary::
    MUD
        Multi-User Dimension. A more historic term for MMORPG, MUDs were some
        of the earliest multiplayer games. `Wikipedia
        <https://www.wikiwand.com/en/MUD>`_ has a pretty comprehensive
        article on them.
    MUD client
        A specialized client for playing MUDs. (duh)
    MUD engine
        Also known as drivers, MUD engines are game engines meant for
        presenting :term:`MUDs <MUD>`. There have traditionally been two main
        classes of MUD engine: DIKU and LPC. DIKU MUDs came first, and used
        database-driven logic to present a simplistic hack-and-slash
        environment to the player. LPC MUDs used object-oriented programming
        techniques to render more detailed game worlds to the player. qtmud
        follows in the tradition of the latter.
    mudlib
        short for Multi-User Dimension Library, a mudlib is a game written
        for a :term:`MUD engine` to run. From qtmud's perspective, a mudlib
        is a Python package which is heavily reliant on the :mod:`qtmud` module.