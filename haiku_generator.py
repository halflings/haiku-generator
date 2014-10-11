import json
from bigrams import Bigrams
from grammar_tree import GrammarTree
from pos_tagger import POSTagger

class HaikuGenerator:
    def __init__(self, haikus_file='haikus.json'):
        self._dataset = HaikuGenerator.__parse_dataset(haikus_file)
        self._tagged_dataset = None
        self._bigrams = None
        # Tagged word tree
        self._word_tree = None
        self._grammar_tree = None


    def generate_bigrams(self, syllables=True):
        # WARNING: NotImplementedException may occur if we cannot get the
        # required number of syllables or if we cannot find a word successor
        if not self._bigrams:
            self._bigrams = Bigrams(self._dataset)

        return self._bigrams.generate_haiku(syllables)

    def generate_grammar_tree(self):
        if not self._tagged_dataset:
            self._tagged_dataset = POSTagger.get_pos_tagged_dataset(self._dataset)
        if not self._word_tree:
            self._word_tree = POSTagger.get_tagged_word_tree(self._tagged_dataset)
        if not self._grammar_tree:
            self._grammar_tree = GrammarTree(self._tagged_dataset)

        return self._grammar_tree.generate_haiku(self._word_tree)

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
    print generator.generate_bigrams(True)
    print
    print generator.generate_grammar_tree()
