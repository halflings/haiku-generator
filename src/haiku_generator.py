import json
import nltk
import random
#import heuristic
from collections import Counter
from wan import WAN
from bigrams import Bigrams
from grammar_tree import GrammarTree
from pos_tagger import POSTagger

class HaikuGenerator:
    def __init__(self, haikus_file='haikus.json'):
        self._dataset = HaikuGenerator.__parse_dataset(haikus_file)
        self._tagged_dataset = POSTagger.get_pos_tagged_dataset(self._dataset)
        self._bigrams = Bigrams(self._dataset)
        self._reversed_bigrams = Bigrams(self._dataset, reverse=True)
        self._grammar_tree = GrammarTree(self._tagged_dataset)

    def generate_bigrams(self, syllables=True):
        # WARNING: NotImplementedException may occur if we cannot get the
        # required number of syllables or if we cannot find a word successor
        return self._bigrams.generate_haiku(syllables)

    def generate_grammar_tree(self):
        return self._grammar_tree.generate_haiku()

    def generate_tagged_word(self, tag):
        return self._grammar_tree.generate_word(tag)

    def generate_tagged_bigram(self, word, tag, successor=True):
        """
        Return a random word which is successor or predecessor of the given word in the
        dataset and has the specified tag, or None
        If successor=True, the successor is returned, else the predecessor
        """
        if successor:
            successors = self._bigrams.get_successors(word)
        else:
            successors = self._reversed_bigrams.get_successors(word)
        tagged_words = nltk.pos_tag(successors)
        candidates = [(w, t) for (w, t) in tagged_words if t == tag]

        if len(candidates) == 0:
            return None

        return candidates[random.randint(0, len(candidates)-1)][0]

    def get_bigrams(self, word, tagged=False, successor=True):
        """
        Return a counter containing a list of predecessors or successors for the given word
        """
        if successor:
            bigrams = self._bigrams.get_successors(word)
        else:
            bigrams = self._reversed_bigrams.get_successors(word)

        if tagged:
            bigrams = nltk.pos_tag(bigrams)

        return Counter(bigrams)


    @staticmethod
    def __parse_dataset(haikus_file):
        """
        Return the dataset as a dictionary
        """
        json_data = open(haikus_file)
        dataset = json.load(json_data)
        json_data.close()

        return dataset


if __name__ == '__main__':
    generator = HaikuGenerator()
    #print generator.generate_bigrams(True)
    #print generator.generate_grammar_tree()
 #   for x in xrange(1,10):
#        heuristic.ghaiku(generator._grammar_tree, WAN())
    # print generator.generate_tagged_word('NN')

    # print generator.generate_tagged_bigram('lake', 'DT', successor=True)
    # print generator.generate_tagged_bigram('lake', 'DT', successor=False)
    # print generator.get_bigrams('water', tagged=True, successor=True)
    # print generator.get_bigrams('water', tagged=False, successor=False)
