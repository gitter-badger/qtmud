from textblob import TextBlob


def parse_line(line):
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
