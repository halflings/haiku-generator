import nltk
import itertools
import random
import hyphen
from pos_tagger import POSTagger

class Bigrams:
    # Constants
    HAIKU_LINES = 3
    HAIKU_SYLLABLES = [5, 7, 5]

    def __init__(self, dataset, locale='en_US', reverse=False):
        self._hyphenator = hyphen.Hyphenator(locale)
        self._bigrams_dict = self.__build__bigrams_dictionary(self.__compute_bigrams(dataset), reverse)

    def get_successors(self, word):
        """"
        Return a list of word successors of the word given
        """
        if not word in self._bigrams_dict:
            return []
        return self._bigrams_dict[word]

    def generate_haiku(self, syllables=True):
        """
        If syllables is true, the haiku returned will be divided in 3 lines
        and will respect the syllables constraint
        """
        if not syllables:
            word = self._bigrams_dict.keys()[random.randint(0, len(self._bigrams_dict.keys()) - 1)]
            haiku = []

            for i in xrange(10):
                haiku.append(word)
                word = random.choice(self._bigrams_dict[word])

            haiku.append(word)
            return ' '.join(haiku)

        else:
            haiku = ''

            # Start with a random word
            words = [self._bigrams_dict.keys()[random.randint(0, len(self._bigrams_dict.keys()) - 1)]]

            # Generate each line
            for i in range(Bigrams.HAIKU_LINES):
                remaining_syllables = Bigrams.HAIKU_SYLLABLES[i]

                # Append word until the syllable number has been reached
                while remaining_syllables > 0:
                    random.shuffle(words)

                    # Count the number of syllables for each successor
                    for word in words:
                        tmpSyllables = self.__count_syllables(word)

                        # If a word has the perfect number of syllables to complete the
                        # line, we select it
                        if tmpSyllables == remaining_syllables:
                            remaining_syllables = 0
                            if word == POSTagger.POSSESSIVE or word in POSTagger.PUNCTUATION:
                                haiku = haiku[0:-1]
                            haiku += word + ' '
                            try:
                                words = self._bigrams_dict[word]
                            except:
                                # No successor for the selected word
                                raise NotImplementedError("The selected word has no successor")
                            break
                        # Remove word which have too many syllables
                        elif tmpSyllables > remaining_syllables:
                            words.remove(word)

                    # Pick a word randomly if we could not find a proper word
                    # to end the line
                    if remaining_syllables != 0:
                        word = random.choice(words)
                        remaining_syllables -= self.__count_syllables(word)
                        if word == POSTagger.POSSESSIVE or word in POSTagger.PUNCTUATION:
                                haiku = haiku[0:-1]
                        haiku += word + ' '
                        try:
                            words = self._bigrams_dict[word]
                        except:
                            # No successor for the selected word
                            raise NotImplementedError("The selected word has no successor")

                    # Line cannot be ended with the right number of syllables
                    elif len(words) == 0:
                        raise NotImplementedError("Syllables constraint cannot be respected")


                if i < Bigrams.HAIKU_LINES -1:
                    # End of line
                    haiku += '\r\n'

            return haiku

    def __compute_bigrams(self, dataset):
        """
        Return a list of bigrams (list of 2 words according to the haiku word order)
        which can then be used to generate sentences according to word order
        probability. So that, a third word can easily be generated based on the two
        previous ones
        """
        return list(itertools.chain(*[list(nltk.ngrams(POSTagger.tokenizer.tokenize(haiku), 2)) for key in dataset.keys() for haiku in dataset[key]]))

    def __build__bigrams_dictionary(self, bigrams, reverse):
        """
        Return a dictionary:
        - key: word from the corpus
        - value: list of independant words following (or preceeding if reverse)
                 the key in the corpus
        Note: the value list does not contain unique words, so that we can
        randomly pick a word according to the probability distribution
        """
        dictionary = {}

        for w1, w2 in bigrams:
            if reverse:
                key, value = w2, w1
            else:
                key, value = w1, w2

            if key in dictionary:
                dictionary[key].append(value)
            else:
                dictionary[key] = [value]

        return dictionary

    def __count_syllables(self, word):
        syllables = len(self._hyphenator.syllables(word))
        if syllables == 0:
            return 1
        return syllables
