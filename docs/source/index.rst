.. qtmud documentation master file, created by
   sphinx-quickstart on Sun Sep 25 05:25:08 2016.
   You can adapt this file completely to your liking, but it should at least
   contain the root `toctree` directive.

qtmud
#####

qtmud is a Python package for managing a multi-user dimension, or MUD, written
by emsenn and released under the WTF license.

Players receive verbose text descriptions of their environments and the
activity around them, and interact by typing out commands for what they wish
to do, such as ``survey planet`` or ``fight dragon``.

**Know what you're doing?**
If you want to dive into qtmud's code, here's an overview, with links to the
relevant source code:
    :func:`qtmud.tick` iterates through :mod:`subscriptions
    <qtmud.subscriptions>`
    and :mod:`services <qtmud.services>`, sending any :attr:`events
    <qtmud.events>` to the relevant subscriber. Most subscribers and services
    handle the interaction of of :class:`things <qtmud.Thing>` which
    :mod:`builders <qtmud.builders>` have built into game objects.

MUD libaries (or mudlibs) are built around this framework. :doc:`Starhopper
<starhopper>` is the first mudlib built for qtmud, and it demonstrates how
one might use qtmud to develop your own game.


Get qtmud
=========

The best way to get qtmud is to `clone the repository
<https://help.github.com/articles/cloning-a-repository/>`_ that we host on
`GitHub <https://github.com/emsenn/qtmud>`_.


Configure qtmud
===============


Run qtmud
=========


Login
=====

Once qtmud is up and running, you can login through your favorite MUD client.
I recommend tinyfugue. Or, simply `telnet localhost 5787`.


Module Index
============

* :ref:`modindex`
