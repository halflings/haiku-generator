import nltk
import random
import itertools
from pos_tagger import POSTagger
from collections import Counter

class GrammarTree:
    def __init__(self, tagged_dataset):
        self._root, self._grammar_tree = self.__get_grammar_tree(tagged_dataset)
        self._word_tree = POSTagger.get_tagged_word_tree(tagged_dataset)

    def get_successors(self, tags):
        """
        Return a list of tags succeeding to the tags=(tag1, tag2) given
        """
        return self._grammar_tree[tags]

    def generate_haiku(self):
        # TODO: Implement syllables constraint
        tags = GrammarTree.random_pick(self._root)
        word1 = GrammarTree.random_pick(self._word_tree[tags[0]])
        word2 = GrammarTree.random_pick(self._word_tree[tags[1]])

        haiku = word1 + ' '

        for i in xrange(9):
            if word2 == POSTagger.POSSESSIVE or word in POSTagger.PUNCTUATION:
                haiku = haiku[0:-1]
            haiku += word2 + ' '
            tags = (tags[1], GrammarTree.random_pick(self._grammar_tree[tags]))
            word2 = GrammarTree.random_pick(self._word_tree[tags[1]])

        haiku += word2 + ' '
        return haiku

    def generate_word(self, tag):
        """
        Return a random word from the dataset which has the specified POS-tag
        """
        return GrammarTree.random_pick(self._word_tree[tag])

    @staticmethod
    def random_pick(plist):
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
        gt = GrammarTree.__build_trigrams_dictionary(GrammarTree.__compute_trigrams(tagged_dataset))

        return root, gt

    @staticmethod
    def __compute_trigrams(tagged_dataset):
        """
        Return a list of trigrams (list of 2 successive words and their tag)
        which can then be used to generate a grammar tree
        """
        return list(itertools.chain(*[list(nltk.ngrams(haiku, 3)) for key in tagged_dataset.keys() for haiku in tagged_dataset[key]]))

    @staticmethod
    def __build_trigrams_dictionary(tagged_trigrams):
        """
        Return a dictionary:
        - key: tag1, tag2
        - value: list of (tag, probability) following the key in the corpus
                 ordered by descending probability
        """
        dictionary = {}

        # Build dictionary
        for t1, t2, t3 in tagged_trigrams:
            key = (t1[1], t2[1])
            if not key in dictionary:
                dictionary[key] = {}

            if t3[1] in dictionary[key]:
                dictionary[key][t3[1]] = dictionary[key][t3[1]] + 1
            else:
                dictionary[key][t3[1]] = 1

        # Calculate probabilities
        for key in dictionary:
            sorted_tags = sorted(dictionary[key].items(), key=lambda tuple: tuple[1], reverse=True)
            sum_tags = sum(n for (tag, n) in sorted_tags)
            dictionary[key] = map(lambda (tag, n): (tag, float(n)/sum_tags), sorted_tags)

        return dictionary

    @staticmethod
    def __build_root_probability(tagged_dataset):
        counter = Counter([(haiku[0][1], haiku[1][1]) for key in tagged_dataset.keys() for haiku in tagged_dataset[key]])
        sorted_tags = sorted(counter.items(), key=lambda tuple: tuple[1], reverse=True)
        sum_tags = sum(counter.values())
        return map(lambda (tag, n): (tag, float(n)/sum_tags), sorted_tags)
