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

from nltk.corpus import wordnet as wn


JAPANESE_MASTERS = [
    'Arima (1930)',
    'Asei (d 1752)',
    'Bakusui (1718-1783)',
    'Banzan (1619-1691)',
    'Basho (1644 ~ 1694)',
    'Boncho (d.1714)',
    'Bosha (1897-1941)',
    'Buson (1716-1783)',
    'Choko (d 1731)',
    'Chora (1729-1780)',
    'Dakotsu (1885 - 1962)',
    'Etsujin (1656?–1739)',
    'Gojo',
    'Gokei (d 1769)',
    'Gusai',
    'Gyodai (1732-1793)',
    'Hakujubo (d 1817)',
    'Hokushi (1665-1718)',
    'Kobayashi Issa (1763 - 1827)',
    'Koha (died 1897)',
    'Ikkyu Sojun (1394-1481)',
    'Kanna (d 1744)',
    'Kikaku (1661-1707)',
    'Kito (1741-1789)',
    'Koyo Ozaki (1867-1903)',
    'Kubutsu Otani (1875 - 1943)',
    'Moritake (1472-1549)',
    'Kyorai (1651-1704)',
    'Nandai (d 1817)',
    'Meisetsu (1847-1926)',
    'Soseki Natsume (1867-1916)',
    'Oemura (Oemaru)',
    'Onitsura (1660-1738)',
    'Otsuji Osuga (1881 - 1920)',
    'Ransetsu (1654-1707)',
    'Reikan',
    'Ryokan (1758-1831)',
    'Ryota (d 1717)',
    'Ryoto (1718-1787)',
    'Saigyo (1118-1190)',
    'Saito',
    'Sampu',
    'Santoka (1882-1940)',
    'Shiki (1867-1902)',
    'Shiko (1665-1731)',
    'Shoha (1727-71)',
    'Shohaku (1650-1722)',
    'Sho-u',
    'Socho (1448-1532)',
    'Sogi (1421 - 1502)',
    'Soin (1605-1682)',
    'Sojo (1901-56)',
    'Takahama (1874 ~ 1959)',
    'Taigi Sumi',
    'Teitoku',
    'Togyu (1889-1990)',
    'Ki no Tsurayuki (872–945)',
    'Zaishiki (1642 - 1719)',
]

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

INSPIRATIONS = ['autumn','summer','winter','frog','love','moon','city']

haikugen = HaikuGenerator()


def generate_haiku(inspirations=INSPIRATIONS,meaning_generator=WAN()):
    popular_long_pos = Counter(dict((p, c) for (p, c) in pos_counter.most_common(15) if len(p) > 2))
    popular_short_pos = Counter(dict((p, c) for (p, c) in pos_counter.most_common(15) if len(p) < 3))
    pos_tags = [pick_random_structure(popular_long_pos),
                pick_random_structure(popular_short_pos),
                pick_random_structure(popular_long_pos)]
    print(pos_tags)
    return haiku_from_pos_tags(pos_tags,random.choice(inspirations))


def generate8haikus():
    wan = WAN()
    wnet = WordNetUtil()
    for inspiration in ['summer','winter','city','love']:
        print("---------------------")
        print(generate_safe_haiku(inspiration,wan))
        print("--"+random.choice(JAPANESE_MASTERS))
        print("---------------------")
        print(generate_safe_haiku(inspiration,wnet))
        print("--"+random.choice(JAPANESE_MASTERS))


def generate_safe_haiku(inspiration,meaning_generator):
    safe_pos_tags = [
    [('VBG', 'DT', 'NN'), ('NNS',), ('JJ','NN', 'NNS')],
    [('VBG', 'NN'), ('NN',), ('VBG','IN', 'DT', 'NN')],
    ]
    return haiku_from_pos_tags(random.choice(safe_pos_tags),inspiration,meaning_generator)


def haiku_from_pos_tags(pos_tags,inspiration,meaning_generator):
    word_dump = []
    lines = [generate_line(line_tags,word_dump, inspiration,meaning_generator) for line_tags in pos_tags]
    # "Decorating" the haiku
    lines[0][0] = lines[0][0].title()   
    lines[0][-1] = lines[0][-1] + u'—'
    lines[-1][-1] = lines[-1][-1] + '.'
    return '\n'.join(' '.join(w for w in line) for line in lines)

def generate_line(pos_tags,word_dump, inspiration,meaning_generator):
    words = []
    for tag in pos_tags:
        word = generate_word(tag, pos_tags,words, word_dump, inspiration,meaning_generator)
        words.append(word)
        word_dump.append(wn.morphy(word))
    return words

def generate_word(tag, pos_tags, words,word_dump, inspiration,meaning_generator):
    #print(pos_tags)
    # WAN does not take some pos tags into account, so we pick random values
    if tag == 'IN' and len(words) > 0:
        # let's use bigrams for finding suitable following preposition
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
    # getting associated word from inspiration word at 50% probability
    if random.random() < 0.5:
        word = meaning_generator.associate(inspiration, clean_tag)    
    # Otherwise pick the last meaningful word as inspiration 
    if word is None:
        meaningful_words = [w for i, w in enumerate(words)
                              if any(pos_tags[i].startswith(t) for t in ['NN','VB'])]
        if meaningful_words:
            inspiration = meaningful_words[-1]
        word = meaning_generator.associate(inspiration,clean_tag)

    # If still no association is found, we pick a random word
    if word is None or random.random() < 0.01: # to break out of infinite loops
        word = meaning_generator.random_word(clean_tag)

    # Making nouns plural and conjugating verbs
    if tag == 'NNS' or tag == 'NNPS':
        word = pattern.en.pluralize(word) 
    elif tag.startswith('VB'):
        word = pattern.en.conjugate(word, tag)

    # Special case for "a"/"an", both vowel handling and some pluralization handling
    if words and ((words[-1] == 'an' and word[0] not in VOWELS) or (words[-1] == 'a' and word[0] in VOWELS) 
        or ((words[-1] =='a' or words[-1] == 'an') and  tag[-1] == 'S')):
        word = generate_word(tag, pos_tags, words,word_dump, inspiration,meaning_generator)

    # Avoid repeating words
    if wn.morphy(word) in word_dump:
        word = generate_word(tag, pos_tags, words,word_dump, inspiration,meaning_generator)

    return word