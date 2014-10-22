#!/usr/bin/env python
# -*- coding: utf-8 -*-

from collections import Counter
import json
import random

from haikutagger import tokenize_dataset, pick_random_structure
from haiku_generator import HaikuGenerator
from wan import WAN
from word_net_util import WordNetUtil

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

INSPIRATIONS = ['autumn','frog','horse','road','valley']

haikugen = HaikuGenerator()

meaning_generator = WordNetUtil()

def generate_haiku(inspirations=INSPIRATIONS):
    popular_long_pos = Counter(dict((p, c) for (p, c) in pos_counter.most_common(15) if len(p) > 2))
    popular_short_pos = Counter(dict((p, c) for (p, c) in pos_counter.most_common(15) if len(p) < 3))
    pos_tags = [pick_random_structure(popular_long_pos),
                pick_random_structure(popular_short_pos),
                pick_random_structure(popular_long_pos)]
    print(pos_tags)
    return haiku_from_pos_tags(pos_tags,random.choice(inspirations))


def generate_safe_haiku():
    safe_pos_tags = [
    #[('VBG', 'DT', 'NN'), ('NNS',), ('JJ','NN', 'NNS')],
    [('VBG', 'NN'), ('NN'), ('VBG','IN', 'DT', 'NN')],
    ]
    return haiku_from_pos_tags(safe_pos_tags[0],random.choice(INSPIRATIONS))


def haiku_from_pos_tags(pos_tags,inspiration):
    lines = [generate_line(line_tags, inspiration=inspiration) for line_tags in pos_tags]

    # "Decorating" the haiku
    lines[0][0] = lines[0][0].title()   
    lines[0][-1] = lines[0][-1] + u'—'
    lines[-1][-1] = lines[-1][-1] + '.'
    return '\n'.join(' '.join(w for w in line) for line in lines)


def generate_line(pos_tags, inspiration):
    words = []
    for tag in pos_tags:
        word = generate_word(tag, pos_tags, words, inspiration)
        words.append(word)
    return words

def generate_word(tag, pos_tags, words, inspiration):
    # WAN does not take some pos tags into account, so we pick random values
    
    if tag == 'IN' and len(words) > 0:
        preposition = haikugen.generate_tagged_bigram(words[-1],'IN')
        if preposition is None:
            return random.choice(tuple(FILLERS['IN']))
        else:
            return preposition
    elif tag in FILLERS:
        return random.choice(tuple(FILLERS[tag]))

    # Picking a 'clean tag' to be used with WAN
    clean_tag = tag
    for t in {'NN', 'VB', 'RB', 'JJ'}:
        if tag.startswith(t) and tag != t:
            clean_tag = t
            break

    word = None
    # getting associated word from inspiration word
    if random.random() < 0.5:
        word = meaning_generator.associate(inspiration, clean_tag)    
    # Otherwise picking the last meaningful word as an inspiration (or a random value from 'inspirations' otherwise)
    if word is None:
        meaningful_words = [w for i, w in enumerate(words)
                              if any(pos_tags[i].startswith(t) for t in {'NN'})]
        if meaningful_words:
            inspiration = meaningful_words[-1]
        word = meaning_generator.associate(inspiration,clean_tag)

    # If still no association is found, we pick a random word
    if word is None:
        word = meaning_generator.random_word(clean_tag)

    # Making nouns plural and conjugating verbs
    if tag == 'NNS' or tag == 'NNPS':
        word = pattern.en.pluralize(word) 
    elif tag.startswith('VB'):
        word = pattern.en.conjugate(word, tag)

    # Special case for "a"/"an"
    if words and ((words[-1] == 'an' and word[0] not in VOWELS) or (words[-1] == 'a' and word[0] in VOWELS) 
        or ((words[-1] =='a' or words[-1] == 'an') and  tag[-1] == 'S')):
        word = generate_word(tag, pos_tags, words, inspiration)

    # Avoid repeating words
    if word in words:
        word = generate_word(tag, pos_tags, words, inspiration)

    return word