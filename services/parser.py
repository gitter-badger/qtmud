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
        line = TextBlob('I will ' + line)
        parsed_line = line.parse().split(' ')[2:]
        phrase_starts = []
        chunked_phrases = []
        payload = {}
        adjectives = []
        for word in parsed_line:
            parsed_line[parsed_line.index(word)] = word.split('/')
        for word in parsed_line:
            if word[3] in ['O', 'B-PNP']:
                phrase_starts.append(parsed_line.index(word))
        for phrase in phrase_starts:
            if phrase is not phrase_starts[-1]:
                chunked_phrases.append(parsed_line[phrase:phrase_starts[phrase_starts.index(phrase) + 1]])
            if phrase is phrase_starts[-1]:
                chunked_phrases.append(parsed_line[phrase:])
        for phrase in chunked_phrases:
            if phrase[0][3] == 'O' and \
                            len(chunked_phrases[chunked_phrases.index(phrase)]) is 1:
                if phrase[0][1] == 'JJ':
                    adjectives.append(phrase[0][0])
                if phrase[0][1] == 'VB':
                    # verb = 'take'
                    payload['verb'] = phrase[0][0]
                elif phrase[0][1] in ['NN', 'PRP']:
                    # object = 'apple'
                    if adjectives != []:
                        payload['adjectives'] = adjectives
                    payload['subject'] = phrase[0][0]
                    adjectives = []
            elif phrase[0][3] == 'B-PNP':
                if phrase[0][1] == 'IN':
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
        if not 'subject' in payload and 'pnp_clauses' in payload:
            payload['subject'] = payload['pnp_clauses'][0][2]
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
        if events == []:
            return False
        for event, payload in events: #pylint: disable=unused-variable
            commander = payload['commander']
            line = payload['line']
            command = line.split(' ')[0]
            if hasattr(commander, 'commands') and command in commander.commands:
                commander.commands[command](line)
            else:
                self.manager.schedule('render', client=commander, scene='invalid command')
        return True
