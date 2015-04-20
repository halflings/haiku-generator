from collections import Counter
import itertools
import json
import nltk
import random

TOKENIZER = nltk.tokenize.RegexpTokenizer(r"\w+|[!,.:;?]|'s")
PUNCTUATION_SET = {'!', ',', '.', ':', ';', '?'}

def tokenize_haiku(haiku, keep_punctuation=False, fillers=None):
    lines = haiku.lower().split('\r\n')
    pos_tags = []
    for line in lines:
        words = TOKENIZER.tokenize(line)
        if not keep_punctuation:
            words = [w for w in words if w not in PUNCTUATION_SET]
        tagged_haiku = nltk.pos_tag(words)

        # Updating fillers
        if fillers is not None:
            for word, tag in tagged_haiku:
                if tag in fillers:
                    fillers[tag].add(word)

        pos_tags.append(tuple([e[1] for e in tagged_haiku]))
    return tuple(pos_tags)

def tokenize_dataset(dataset, haikus_limit, fillers=None):
    bag_of_haikus = [h for s, haikus in dataset.iteritems() for h in haikus]
    random.shuffle(bag_of_haikus)
    haiku_tags = [tokenize_haiku(h, fillers=fillers) for h in bag_of_haikus[:haikus_limit]]
    pos_counter = Counter(line_tags for h_tags in haiku_tags for line_tags in h_tags)
    return pos_counter

def pick_random_structure(pos_counter):
    i = random.randrange(sum(pos_counter.values()))
    return next(itertools.islice(pos_counter.elements(), i, None))

# Maximum number of haikus we will process ; POS tagging takes a long time!
NUM_HAIKUS = 400
if __name__ == '__main__':
    with open('haikus.json') as haikus_file:
        dataset = json.load(haikus_file)
    pos_counter = tokenize_dataset(dataset, haikus_limit=NUM_HAIKUS)
    print pos_counter

    # Example of picking up some random structures
    for i in xrange(10):
        pos_tags = pick_random_structure(pos_counter)
        print pos_tags, pos_counter[pos_tags]