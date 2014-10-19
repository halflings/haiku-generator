import json
import nltk
import random

from collections import Counter

TOKENIZER = nltk.tokenize.RegexpTokenizer(r"\w+|[!,.:;?]|'s")
PUNCTUATION_SET = {'!', ',', '.', ':', ';', '?'}

def tokenize_haiku(haiku, keep_punctuation=False):
    lines = haiku.split('\r\n')
    pos_tags = []
    for line in lines:
        words = TOKENIZER.tokenize(line)
        if not keep_punctuation:
            words = [w for w in words if w not in PUNCTUATION_SET]
        pos_tags.append(tuple([e[1] for e in nltk.pos_tag(words)]))
    return tuple(pos_tags)

def tokenize_dataset(dataset, haikus_limit):
    bag_of_haikus = [h for s, haikus in dataset.iteritems() for h in haikus]
    random.shuffle(bag_of_haikus)
    haiku_tags = [tokenize_haiku(h) for h in bag_of_haikus[:haikus_limit]]
    pos_counter = Counter(line_tags for h_tags in haiku_tags for line_tags in h_tags)
    return pos_counter

# Maximum number of haikus we will process ; POS tagging takes a long time!
NUM_HAIKUS = 1000
if __name__ == '__main__':
    with open('haikus.json') as haikus_file:
        dataset = json.load(haikus_file)
    print tokenize_dataset(dataset, haikus_limit=NUM_HAIKUS)