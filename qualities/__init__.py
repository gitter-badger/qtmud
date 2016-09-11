""" Qualities are applied to things to create complex
    game objects.

    .. moduleauthor:: emsenn <morgan.sennhauser@gmail.com>

    .. versionadded:: 0.0.1
    .. versionchanged:: 0.0.1-feature/environments
        Added the Renderable quality
    .. versionchanged:: 0.0.1-feature/parser
        Moved qualities into separate files and import them to this one, so
        they can all be imported from :mod:`qtmud.qualities`.

    Every object the client interacts with, including the client itself, is
    a :class:`thing <qtmud.Thing>`. What differentiates the client from a
    spaceship from a ham sandwich are its qualities.

    Qualities are classes with an :func:`apply <qtmud.qualities.Quality.apply>`
    function that adds attributes to a thing. (The :func:`apply
    <qtmud.qualities.Quality.apply>` function is meant to be called through
    :func:`qtmud.Manager.add_qualities`, frequently through :func:`new_thing()
    <qtmud.Manager.new_thing>`.

    The different submodules of this package contain the qualities which
    qtmud uses. The :class:`Quality <qtmud.qualities.Quality>` class outlined
    below is for reference/documentation purposes, and isn't meant to be
    inherited or used in any way.

    By adding several qualities to a :class:`thing <qtmud.Thing>`, it's
    possible to quickly make complex objects. The thing instanced when a
    client logs in currently has 7 qualities applied to it, adding a
    variety of commands. The client's avatar is still just an instance of
    :class:`qtmud.Thing`, but now with attributes for handling command parsing
    and movement and so on.

    The game world is intended to be put together by creating :func:`new
    things <qtmud.Manager.new_thing>` and :func:`adding qualities
    <qtmud.Manager.add_qualities>` to them to make them unique game objects.
    For examples of these qualities, check out :mod:`the library <qtmud.lib>`.

    The rest of this file is used to demonstrate what a basic Quality
    looks like, so you have something to model your development off.

    .. warning:: Qualities which add commands must be added individually
                 through :func:`qtmud.Manager.add_qualities(thing, [Quality])
                 <qtmud.Manager.add_qualities>`. This is a known bug and
                 will be taken care of soon.
"""


import types


# Save us some typing when referencing these base qualities from the lib
from qtmud.qualities.client import Client
from qtmud.qualities.physical import Physical
from qtmud.qualities.renderable import Renderable
from qtmud.qualities.container import Container
from qtmud.qualities.room import Room
from qtmud.qualities.sighted import Sighted
from qtmud.qualities.speaking import Speaking


class Quality(object):
    """ **This class is for API documentation purposes only. Not to be used.**

        .. versionadded:: 0.0.1-feature/parser

        :class:`qtmud.Manager` expects every Quality object to have at the
        very least an :func:`apply() <qtmud.qualities.Quality.apply>` function.
        This is called by :func:`qtmud.Manager.add_qualities` to add attributes
        to an instanced :class:`thing <qtmud.Thing>`. These attributes might
        be a string representing the thing's :attr:`location
        <qtmud.qualities.physical.Physical.location>`, or a function letting
        the thing :func:`speak <qtmud.qualities.speaking.Speak.say>`.
    """

    def __init__(self):
        """
            .. version added:: 0.0.1-feature/parsing

        """
        return

    def womble(self, thing):
        """ An example of a function within a quality.

            .. versionadded:: 0.0.1-feature/parser

            Parameters:
                thing(object):      the :class:`thing <qtmud.Thing>` this
                                    function is being added to.

            Returns:
                string:     Just returns the thing's identity

            Example:
                >>> thing = manager.new_thing(Quality)
                >>> thing.womble()
                29ea7ec1-3fc1-44a1-bddb-c756330273d4

        """
        return thing.identity


    def apply(self, thing):
        """ Properly applies this quality to the thing.

            .. versionadded:: 0.0.1-feature/parser

            Parameters:
                thing(object):      The :class:`thing <qtmud.Thing>` that
                                    this quality is going to be applied to.

            Returns:
                object:             The thing that was passed as a parameter.

            :class:`qtmud.Manager` expects every Quality to have this
            function. When the manager calls :func:`add_qualities(thing,
            Quality) <qtmud.Manager.add_qualities>`, it looks for (or
            creates) an instance of ``Quality``, and then calls that instance's
            ``apply(thing)``, where thing is the object passed in
            ``add_quality(thing, Quality)``.

            It's important to note that each apply() function has a pretty
            verbose syntax, to prevent this function from overwriting any
            attributes it already has. (such as its identity, or attributes
            added by another Quality.)

            Luckily, the syntax is the same whether your new attribute is
            a string or function or anything else.
            ::
                if not hasattr(thing, womble): thing.womble = self.womble

            If you want a function, in this case :func:`womble()
            <qtmud.qualities.Quality.womble>`, to be accessible through
            a command, set up the following statement:
            ::
                if hasattr(thing, 'commands'):
                    thing.commands['womble'] = types.MethodType(self.womble,
                                                                thing)

            This also means adding the line ``import types`` at the head
            of your Quality file. The more verbose attribute setting we
            use helps make sure things are able to have commands added with
            limited memory waste.
        """
        if not hasattr(thing, 'womble'):
            thing.womble = self.womble
        if hasattr(thing, 'commands'):
            thing.commands['womble'] = types.MethodType(self.womble, thing)
        return thing
