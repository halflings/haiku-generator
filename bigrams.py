import nltk
import itertools
import random
import hyphen

class Bigrams:
    # Constants
    HAIKU_LINES = 3
    HAIKU_SYLLABLES = [5, 7, 5]

    def __init__(self, dataset, locale='en_US'):
        self._hyphenator = hyphen.Hyphenator(locale)
        self._bigrams_dict = self.__build__bigrams_dictionary(self.__compute_bigrams(dataset))

    def generate_haiku(self, syllables=True):
        if not syllables:
            word = self._bigrams_dict.keys()[random.randint(0, len(self._bigrams_dict.keys()) - 1)]
            haiku = []

            # Do a while checking syllabus
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
                            haiku += word + ' '
                            try:
                                words = self._bigrams_dict[word]
                            except:
                                # No successor for the selected word
                                raise NotImplementedError()
                            break
                        # Remove word which have too many syllables
                        elif tmpSyllables > remaining_syllables:
                            words.remove(word)

                    # Pick a word randomly if we could not find a proper word
                    # to end the line
                    if remaining_syllables != 0:
                        word = random.choice(words)
                        remaining_syllables -= self.__count_syllables(word)
                        haiku += word + ' '
                        try:
                            words = self._bigrams_dict[word]
                        except:
                            # No successor for the selected word
                            raise NotImplementedError()

                    # Line cannot be ended with the right number of syllables
                    elif len(words) == 0:
                        raise NotImplementedError()


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
        # TODO: get rid of possesive form
        tokenizer = nltk.tokenize.RegexpTokenizer(r'\w+')

        return list(itertools.chain(*[list(nltk.ngrams(tokenizer.tokenize(haiku), 2)) for key in dataset.keys() for haiku in dataset[key]]))

    def __build__bigrams_dictionary(self, bigrams):
        """
        Return a dictionary:
        - key: word from the corpus
        - value: list of independant words following the key in the corpus
        Note: the value list does not contain unique words, so that we can
        randomly pick a word according to the probability distribution
        """
        dictionary = {}

        for w1, w2 in bigrams:
            key = w1
            if key in dictionary:
                dictionary[key].append(w2)
            else:
                dictionary[key] = [w2]

        return dictionary

    def __count_syllables(self, word):
        syllables = len(self._hyphenator.syllables(word))
        if syllables == 0:
            return 1
        return syllables
