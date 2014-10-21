#!/usr/bin/env python
# -*- coding: utf-8 -*-

from collections import Counter
import json
import random

from haikutagger import tokenize_dataset, pick_random_structure
from wan import WAN

import pattern.en

FILLERS = {
    'DT': {'the'},
    'CC': {'and'},
    'PRP$': {'its'},
    'PRP': {'me'},
    'IN': {'at'},
    'TO': {'to'},
    'RP': {'not'},
    'POS': {"'s"},
    'MD': {'can'},
    'WRB': {'who'},
    'WP': {'what'},
}
VOWELS = set('aeiou')
NUM_HAIKUS = 100
with open('haikus.json') as haikus_file:
    dataset = json.load(haikus_file)
pos_counter = tokenize_dataset(dataset, haikus_limit=NUM_HAIKUS, fillers=FILLERS)

INSPIRATIONS = ['love', 'sadness', 'water', 'nature', 'city', 'computer', 'mafia']

wan = WAN()

def generate_haiku(inspirations=INSPIRATIONS):
    popular_long_pos = Counter(dict((p, c) for (p, c) in pos_counter.most_common(15) if len(p) > 2))
    popular_short_pos = Counter(dict((p, c) for (p, c) in pos_counter.most_common(15) if len(p) < 3))
    pos_tags = [pick_random_structure(popular_long_pos),
                pick_random_structure(popular_short_pos),
                pick_random_structure(popular_long_pos)]

    lines = [generate_line(line_tags, inspirations=inspirations) for line_tags in pos_tags]

    # "Decorating" the haiku
    lines[0][0] = lines[0][0].title()
    lines[0][-1] = lines[0][-1] + u'—'
    lines[-1][-1] = lines[-1][-1] + '.'
    return '\n'.join(' '.join(w for w in line) for line in lines)

def generate_line(pos_tags, inspirations):
    words = []
    for tag in pos_tags:
        word = generate_word(tag, pos_tags, words, inspirations)
        words.append(word)
    return words

def generate_word(tag, pos_tags, words, inspirations):
    # WAN does not take some pos tags into account, so we pick random values
    if tag in FILLERS:
        return random.choice(tuple(FILLERS[tag]))

    # Picking a 'clean tag' to be used with WAN
    clean_tag = tag
    for t in {'NN', 'VB', 'RB', 'JJ'}:
        if tag.startswith(t) and tag != t:
            clean_tag = t
            break

    # Picking the last meaningful word as an inspiration (or a random value from 'inspirations' otherwise)
    inspiration = random.choice(inspirations)
    meaningful_words = [w for i, w in enumerate(words)
                          if any(pos_tags[i].startswith(t) for t in {'NN', 'JJ'})]
    if meaningful_words:
        inspiration = meaningful_words[-1]
    word = wan.associate(inspiration, clean_tag)

    # If no association is found, we pick a random word
    if word is None:
        word = wan.random_word(clean_tag)

    # Making nouns plural and conjugating verbs
    if tag == 'NNS' or tag == 'NNPS':
        word = pattern.en.pluralize(word)
    elif tag.startswith('VB'):
        word = pattern.en.conjugate(word, tag)

    # Special case for "a"/"an"
    if words and ((words[-1] == 'an' and word[0] not in VOWELS) or (words[-1] == 'a' and word[0] in VOWELS)):
        word = generate_word(tag, pos_tags, words, inspirations)

    # Avoid repeating words
    if word in words:
        word = generate_word(tag, pos_tags, words, inspirations)

    return word