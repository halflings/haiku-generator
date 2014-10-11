import nltk
import itertools

from pos_tagger import POSTagger


class GrammarTree:
    @staticmethod
    def get_grammar_tree(haiku_file='haikus.json'):
        tagged_dataset = POSTagger.get_pos_tagged_dataset(haiku_file)
        print "Building grammar tree..."
        return GrammarTree.__build_bigrams_dictionary(GrammarTree.__compute_bigrams(tagged_dataset))

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



if __name__ == '__main__':
    gt = GrammarTree.get_grammar_tree()
