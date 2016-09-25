""" methods related to text processing

    .. versionadded:: 0.0.4
"""

from textblob import TextBlob

import qtmud
import mudlib


def parse_line(line):
    """ interpret phrase relation and parts of speech from line

        Parameters:
            line(str):          line to be parsed
        Return:
            payload(dict):      phrases by role

        Check inline comments for technical explanation.
    """
    # TODO: change clause to phrase
    line = TextBlob('I will ' + line)
    parsed_line = line.parse().split(' ')[2:]
    for word in parsed_line:
        parsed_line[parsed_line.index(word)] = word.split('/')
    phrase_starts = []
    chunked_phrases = []
    payload = {}
    adjectives = []
    for place, word in enumerate(parsed_line):
        if word[3] in ['O', 'B-PNP']:
            phrase_starts.append(place)
    for phrase in phrase_starts:
        if phrase is not phrase_starts[-1]:
            chunked_phrases.append(parsed_line[phrase:phrase_starts[
                phrase_starts.index(phrase) + 1]])
        if phrase is phrase_starts[-1]:
            chunked_phrases.append(parsed_line[phrase:])
    for phrase in chunked_phrases:
        if phrase[0][3] == 'O' and \
                        len(chunked_phrases[
                                chunked_phrases.index(phrase)]) is 1:
            if phrase[0][1] == 'JJ':
                if 'adjectives' in payload:
                    payload['adjectives'].append(phrase[0][0])
                else:
                    payload['adjectives'] = [phrase[0][0]]
                adjectives.append(phrase[0][0])
            if phrase[0][1] == 'VB':
                payload['verb'] = phrase[0][0]
            elif phrase[0][1] in ['NN', 'NNS', 'PRP']:
                payload['objekt'] = phrase[0][0]
        elif phrase[0][3] == 'B-PNP':
            if phrase[0][1] in ['IN', 'TO']:
                preposition = phrase[0][0]
                for word in phrase:
                    if word[1] in ['NN', 'PRP']:
                        noun = word[0]
                    if word[1] == 'JJ':
                        adjectives.append(word[0])
            pnp = [preposition, adjectives, noun]
            if 'pnp_clauses' not in payload:
                payload['pnp_clauses'] = []
            payload['pnp_clauses'].append(pnp)
        adjectives = []
    return payload


def search_by_line(searcher, verb=None, objekt=None, adjectives=None,
                   pnp_clauses=None):
    """ search for thing by parsed line

        Parameters:
            searcher(object):
            objekt(str):
            adjectives(list):
            pnp_clauses(list):
            verb(str):
        Return:
            list:               matched things.
    """
    matches = []
    reference = searcher
    if objekt is not None:
        if pnp_clauses is not None:
            pnp_clauses.reverse()
            for clause in pnp_clauses:
                if clause[0] in ['from', 'in', 'on']:
                    references = mudlib.search_environment(reference,
                                                          clause[1],
                                                          clause[2])
                    if len(references) != 1:
                        return references
                    reference = references[0]
        matches = qtmud.search_by_noun(reference,
                                       adjectives,
                                       objekt)
    return matches
