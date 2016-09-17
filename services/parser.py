""" handles the input from clients

    .. module:: qtmud.services.parser
        :synopsis: handles the input from clients
    
    .. moduleauthor: Morgan Sennhauser <morgan.sennhauser@gmail.com>
    .. version added:: 0.0.1
    .. version changed:: 0.0.1-feature/organizing
        Added `look` and `go` commands
    .. version changed:: 0.0.1-feature/parser
        moved commands into their associated qualities
    
    Parser is subscribed to 'parse' events. It expects these events to have:
    
    * client - the object the client is associated with
    * cmd - the first word (split by space) of the client's line
    * trailing - everything after the first word.
    
    The code for how it works is pretty straightforward, and bad, at this 
    point, so I'm not going to bother thoroughly commenting it.
"""
from textblob import TextBlob

class Parser(object):
    """ To listen for client input, Parser subscribes to 'parse' events
        
        .. versionadded:: 0.0.1-features/parser 
        
    """
    
    def __init__(self, manager):
        """
            .. versionadded:: 0.0.1-feature/parser
            .. versionchanged:: 0.0.2-feature/renderer
                removed unnecessary dependency on :class:`Service 
                <qtmud.services.Service>`
        """
        self.subscriptions = ['parse']
        self.manager = manager
        self.manager.subscribe(self, 'parse')

    def parse_line(self, line):
        """ Take a line and do some parts of speech tagging to it

            .. versionadded:: 0.0.2-feature/adjectives
            .. versionchanged:: 0.0.2-feature/textblob
                added documentation, cleaned up some bugs.
        """
        # NOTE: in these comments I say Object a lot. I'm referencing the
        # syntactic concept, not the Pythonic datatype.
        # Put "I will" before incoming commannds, so they read more like
        # sentences, i.e.
        # "I will" take the second red apple from my leather backpack on the
        # desk
        line = TextBlob('I will ' + line)
        # Parts of Speech tag (parse()) the line, split it on space, and
        # remove "I will"
        parsed_line = line.parse().split(' ')[2:]
        # organize those PoS tags.
        for word in parsed_line:
            parsed_line[parsed_line.index(word)] = word.split('/')
        # declare some empty lists/dicts for mucking about through processing
        # list of ints marking the 1st word of verb, adjective+subject, and
        # prepositional noun phrases
        phrase_starts = []
        # phrases all joined together as a list.
        chunked_phrases = []
        # the finished parsed sentence
        payload = {}
        # adjectives for the nouns in either adj+sub phrase or any PNP
        # (prepositional noun phrases)
        adjectives = []
        # if the word is an Object or Beginning-of-a-Prepositional-Noun-Phrase,
        # add it to phrase_starts
        for place, word in enumerate(parsed_line):
            if word[3] in ['O', 'B-PNP']:
                phrase_starts.append(place)
        # Based on our phrase_starts, create "chunks", like "second red apple"
        # or "in the big backpack"
        for phrase in phrase_starts:
            if phrase is not phrase_starts[-1]:
                chunked_phrases.append(parsed_line[phrase:phrase_starts[phrase_starts.index(phrase) + 1]])
            if phrase is phrase_starts[-1]:
                chunked_phrases.append(parsed_line[phrase:])
        for phrase in chunked_phrases:
            if phrase[0][3] == 'O' and \
                            len(chunked_phrases[chunked_phrases.index(phrase)]) is 1:
                if phrase[0][1] == 'JJ':
                    if 'adjectives' in payload:
                        payload['adjectives'].append(phrase[0][0])
                    else:
                        payload['adjectives'] = [phrase[0][0]]
                    adjectives.append(phrase[0][0])
                if phrase[0][1] == 'VB':
                    # verb = 'take'
                    payload['verb'] = phrase[0][0]
                elif phrase[0][1] in ['NN', 'NNS', 'PRP']:
                    # object = 'apple'
                    payload['subject'] = phrase[0][0]
            elif phrase[0][3] == 'B-PNP':
                if phrase[0][1] in ['IN', 'TO']:
                    preposition = phrase[0][0]
                    for word in phrase:
                        if word[1] in ['NN', 'PRP']:
                            noun = word[0]
                        if word[1] == 'JJ':
                            adjectives.append(word[0])
                pnp = [preposition, adjectives, noun]
                if not 'pnp_clauses' in payload:
                    payload['pnp_clauses'] = []
                payload['pnp_clauses'].append(pnp)
            adjectives = []
        return payload



    def tick(self, events=False):
        """ Handle commands from the last tick.
        
            .. versionadded:: 0.0.1-feature/parser
            .. versionchanged:: 0.0.2-feature/nametags
                Added better failure control.
            
            Parameters:
                events(list):       set to False by default, expected to 
                                    be a list of tuples in the format of 
                                    ``[('render', {payload})]``
                
            Returns:
                bool:               True if there were events to process,
                                    otherwise False.
            
            The ``payload`` of each event is expected to have:
                
                * ``client`` - represents the client who is trying to have 
                  their command parsed.
                * ``cmd`` - a single word that represent's the command 
                  ``client`` is trying to execute.
                * ``trailing`` - this one is optional, and is any text that 
                  came after the ``cmd`` in the player's input.

            If the Bob inputs ``say hello there skippy``, ``client`` would 
            be the object that represent's Bob's avatar, ``cmd`` would be 
            ``say``, and ``trailing`` would be ``hello there skippy``.
            
            If ``cmd`` (in this case ``say``) is in the client's list of 
            :attr:`commands <qtmud.qualities.client.Client.commands>`,
            then the method that command points to will be called, with 
            ``trailing`` as an argument. In our example, ``bob.say('hello 
            there skippy')``.
        """
        if not events:
            return False
        for event, payload in events: #pylint: disable=unused-variable
            print('foo')
            commander = payload['commander']
            line = payload['line']
            command = line.split(' ')[0]
            if hasattr(commander, 'commands') and command in commander.commands:
                commander.commands[command](line)
            else:
                self.manager.schedule('send',
                                      thing=commander,
                                      scene='invalid command')
        return True
