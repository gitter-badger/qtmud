.. qtmud documentation master file, created by
   sphinx-quickstart on Sun Sep 25 05:25:08 2016.
   You can adapt this file completely to your liking, but it should at least
   contain the root `toctree` directive.

qtMUD
#####

qtMUD is a Python package for developing and managing a multi-user dimension,
or :term:`MUD` , written by `emsenn <https://github.com/emsenn/>`_
and released under the `WTFPL <http://www.wtfpl.com>`_.

In MUDs, players receive verbose text descriptions of their environments and
the activity around them, and interact by typing out commands for what they
wish to do, such as ``survey planet`` or ``fight dragon``.

By providing a clearly documented API focused on granular module design,
qtMUD is built to be the non-programmer's way to create and run a MUD.


.. note:: If you're interested in using qtMUD to host a game, skip ahead to the
          :ref:`Mudlibs` section of this document.


A Brief History of MUDs
=======================
or Why qtMUD?
-------------

Thanks to their text-driven format, MUDs are one of the oldest multiplayer
formats on the Internet. You can get a detailed history on `Wikipedia
<https://www.wikiwand.com/en/MUD>`_, but the important takeaway is that MUDs
are old - and not just MUDs as a genre, but many individual MUDs.

This age cultivated the same systemic problems any older project might have.
Documentation is sparse, there are a dozen ways to do a simple task, and so
on. These problems are especially severe for many MUDs, as they recruit
developers from within their player-base, who frequently aren't developers
themselves.

With these problems, it can be exceptionally difficult to develop your own
MUD, or even use another person's as a starting point. There are more modern
MUD engines out there which address many of these problems, however they
still assume the person running the MUD has some sort of familiarity with
programming, or at the least, a connection to the MUD development community.

qtMUD is designed to cater to an unaddressed niche - people who want to run a
MUD but who have no prior programming experience, in general or with MUDs.
Maybe you're a big fan of table-top RPGs, and want to set up a way for your
friends across the world to go through a campaign. Maybe you want a chat
service for friends that also lets you play a card game.


How it Works
============

qtMUD uses a series of :func:`tick()s <qtmud.tick>` to broadcast messages
to :mod:`subscriptions <qtmud.subscriptions>` and :mod:`services
qtmud.services>`. Most subscribers and services handle the interaction of
:class:`things <qtmud.Thing>` which :mod:`builders <qtmud.builders>` have built
into game objects.


Getting Started
===============


Download qtMUD
--------------

The best way to get qtmud is to `clone the repository
<https://help.github.com/articles/cloning-a-repository/>`_ that we host on
`GitHub <https://github.com/emsenn/qtmud>`_.


Run qtMUD
---------

There are two ways to start qtmud:

From the terminal::

    $ ./run.py
    qtmud        INFO     qtmud.load() called
    qtmud        INFO     qtmud load()ed successfully
    qtmud        INFO     qtmud.run()ning

From the Python interpreter:

    >>> import qtmud
    >>> qtmud.load()
    qtmud        INFO     qtmud.load() called
    qtmud        INFO     [... more loading info ...]
    qtmud        INFO     qtmud.load()ed
    >>> qtmud.run()
    qtmud        INFO     qtmud.run()ning

If there are any errors, do your best to handle them, but if you can't, head
over to our `GitHub Issues <https://github.com/emsenn/qtmud/issues>`_ and
search for your problem to see if there's any known solution. If you can't
find an answer, create a new issue and someone should be along to address it
promptly.

 (The most common error is probably that your addresses are set incorrectly -
 check the documentation for :attr:`IPv4 <qtmud.IP4_ADDRESS>` or
 :attr:`IPv6 <qtmud.IP6_ADDRESS>` addresses, depending on which you plan on
 using.)

Once qtMUD is running on your system, connect to it using your
:term:`MUD client` of choice. If you don't have one, go to a command-line and
just use telnet. Once you've connnected, your client should display something
similar to::

    % Trying to connect to qtmud-dev: 127.0.0.1 5787.
    % Connected to qtmud-dev.

    qtmud               0.0.4

    Successfully connected to qtmud, press enter to continue login...

You can go through the client login/registration process, and then once
you're in, enter "commands" to see what all your client has available to you.

Unfortunately, beyond some basic methods for retrieving and manipulating
client account information, qtmud itself doesn't come with too many features.


Developing with qtMUD
=====================

If you plan on developing your own mudlib, or expanding one of ours, you
should read the full :doc:`qtmud` module documentation.


Mudlibs
=======

qtMUD itself only provides the core functionality, that MUD libraries (or
:term:`mudlibs`) use to create their own game. Right now, qtMUD comes bundled
with 3 libraries that you can use to play a game right away.:

* :doc:`Fireside <fireside>` is the most simple, providing an all-versus-all
  perpetual card game where players gain mana by chatting and use that mana
  to play cards various effects.
* :doc:`Starhopper <starhopper>` is an episodic space adventure game, meant to
  be played by small groups in a single session.
* :doc:`Yeolde RPG <yeolderpg>` is a persistent MMORPG. Due to the complexity,
  this mudlib is very buggy, all the time. You've been warned.