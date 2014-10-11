import nltk
import random
import itertools
from collections import Counter

class GrammarTree:
    def __init__(self, tagged_dataset):
        self._root, self._grammar_tree = self.__get_grammar_tree(tagged_dataset)

    def generate_haiku(self, word_tree):
        # TODO: Implement syllables constraint
        tag = GrammarTree.__random_pick(self._root)
        word = GrammarTree.__random_pick(word_tree[tag])

        haiku = []
        for i in xrange(10):
            haiku.append(word)
            tag = GrammarTree.__random_pick(self._grammar_tree[tag])
            word = GrammarTree.__random_pick(word_tree[tag])

        haiku.append(word)
        return ' '.join(haiku)

    @staticmethod
    def __random_pick(plist):
        summed = 0
        r = random.random()
        for (e, p) in plist:
            summed += p
            if summed >= r:
                return e
        return plist[-1][0]

    def __get_grammar_tree(self, tagged_dataset):
        """
        Return a tuple containing the root probability and the grammar tree
        - root probability: list of (tag, probability) ordered by descending probability
        - grammar tree: dictionary
            - key: tag
            - value: list of (tag, probability) following the key in the corpus
                     ordered by descending probability
        """
        print "Building grammar tree..."
        root = GrammarTree.__build_root_probability(tagged_dataset)
        gt = GrammarTree.__build_bigrams_dictionary(GrammarTree.__compute_bigrams(tagged_dataset))

        return root, gt

    @staticmethod
    def __compute_bigrams(tagged_dataset):
        """
        Return a list of bigrams (list of 2 successive words and their tag)
        which can then be used to generate a grammar tree
        """
        return list(itertools.chain(*[list(nltk.ngrams(haiku, 2)) for key in tagged_dataset.keys() for haiku in tagged_dataset[key]]))

    @staticmethod
    def __build_bigrams_dictionary(tagged_bigrams):
        """
        Return a dictionary:
        - key: tag
        - value: list of (tag, probability) following the key in the corpus
                 ordered by descending probability
        """
        dictionary = {}

        # Build dictionary
        for t1, t2 in tagged_bigrams:
            key = t1[1]
            if not key in dictionary:
                dictionary[key] = {}

            if t2[1] in dictionary[key]:
                dictionary[key][t2[1]] = dictionary[key][t2[1]] + 1
            else:
                dictionary[key][t2[1]] = 1

        # Calculate probabilities
        for key in dictionary:
            sorted_tags = sorted(dictionary[key].items(), key=lambda tuple: tuple[1], reverse=True)
            sum_tags = sum(n for (tag, n) in sorted_tags)
            dictionary[key] = map(lambda (tag, n): (tag, float(n)/sum_tags), sorted_tags)

        return dictionary

    @staticmethod
    def __build_root_probability(tagged_dataset):
        counter = Counter([haiku[0][1] for key in tagged_dataset.keys() for haiku in tagged_dataset[key]])
        sorted_tags = sorted(counter.items(), key=lambda tuple: tuple[1], reverse=True)
        sum_tags = sum(counter.values())
        return map(lambda (tag, n): (tag, float(n)/sum_tags), sorted_tags)
