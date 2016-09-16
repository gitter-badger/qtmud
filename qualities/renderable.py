""" Adds a name and description to a thing.

    .. moduleauthor:: emsenn <morgan.sennhauser@gmail.com>

    .. versionadded:: 0.0.2-feature/parser
        was a part of qtmud.qualities

"""


class Renderable(object):
    """ For applying the Renderable quality to a thing.

        .. versionadded:: 0.0.1-feature/environments
        .. versionchanged:: 0.0.2-feature/nametags
            added adjectives

        Attributes:
            name(str):          The name of the thing. Set to its identity by
                                default.
            adjectives(list):   A list of adjectives that might be used with 
                                the :class:`thing <qtmud.Thing>`'s 
                                :attr:`nametags <qtmud.Thing.nametags>`.
            description(str):   The thing's description.
    """
    def __init__(self):
        """
            .. version added:: 0.0.1-feature/environments

        """
        self.name = ''
        self.description = ''
        return

    @staticmethod
    def set_name(thing, name):
        """
            .. versionadded:: 0.0.2-feature/nametags
            .. versionchanged:: 0.0.2-feature/textblob
                changed to static method
        """
        if type(name) is str and name != '':
            if hasattr(thing, 'name') and thing.name != '':
                old_shortname = thing.name.split()[-1].lower()
                if old_shortname in thing.nametags:
                    thing.nametags.remove(old_shortname)
            thing.__dict__['name'] = name
            thing.nametags.add(name.split()[-1].lower())
            if len(name.split()) > 1:
                for adjective in name.split()[0:-1]:
                    thing.adjectives.add(adjective.lower())
        return

    def apply(self, thing):
        """ Applies the Renderable quality to a thing

            .. version added:: 0.0.1-feature/environments
        """
        if not hasattr(thing, 'name'):
            thing.name = str(thing.identity)
        if not hasattr(thing, 'description'):
            thing.description = self.description
        thing.set_name = self.set_name
        return thing
