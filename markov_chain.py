import json
import nltk
import itertools
import random
import hyphen

# Constants
HAIKU_LINES = 3
HAIKU_SYLLABLES = [5, 7, 5]

hyphenator = hyphen.Hyphenator('en_US')

def parse_dataset():
    """
    Return the dataset as a dictionary
    """
    json_data = open('haikus.json')
    dataset = json.load(json_data)
    json_data.close()

    return dataset


def build_tagged_corpus(dataset):
    """
    Return a list of list of tagged word
    """
    # The following code allows the sentence tokenization of a text (useless here)
    # sent_detector = nltk.data.load('tokenizers/punkt/english.pickle')
    # sentences = sent_detector.tokenize(dataset['SUMMER Terrestrial'][0].strip()))

    return [nltk.pos_tag(nltk.word_tokenize(haiku)) for key in dataset.keys() for haiku in dataset[key]]

    # Can also be done using the following instructions
    # corpus = []
    # for key in dataset.keys():
    #     for haiku in dataset[key]:
    #         words = nltk.word_tokenize(haiku)
    #         tagged_words = nltk.pos_tag(words)
    #         corpus.append(tagged_words)

    # return corpus


def compute_bigrams(dataset):
    """
    Return a list of bigrams (list of 2 words according to the haiku word order)
    which can then be used to generate sentences according to word order
    probability. So that, a third word can easily be generated based on the two
    previous ones
    """
    # TODO: remove punctuaton and apostrophes (and possessive ? => 's)
    tokenizer = nltk.tokenize.RegexpTokenizer(r'\w+|[^\w\s]+')

    return list(itertools.chain(*[list(nltk.ngrams(tokenizer.tokenize(haiku), 2)) for key in dataset.keys() for haiku in dataset[key]]))


def build_bigrams_dictionary(bigrams):
    """
    Return a dictionary:
    - key: tuple of two consecutive words from the corpus
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


def count_syllables(word):
    syllables = len(hyphenator.syllables(word))
    if syllables == 0:
        return 1
    return syllables


def generate_haiku(bigrams_dict):
    haiku = ''

    # Start with a random word
    words = [bigrams_dict.keys()[random.randint(0, len(bigrams_dict.keys()) - 1)]]

    # Generate each line
    for i in range(HAIKU_LINES):
        remaining_syllables = HAIKU_SYLLABLES[i]

        # Append word until the syllable number has been reached
        while remaining_syllables > 0:
            random.shuffle(words)

            # Count the number of syllables for each successor
            for word in words:
                tmpSyllables = count_syllables(word)

                # If a word has the perfect number of syllables to complete the
                # line, we select it
                if tmpSyllables == remaining_syllables:
                    remaining_syllables = 0
                    haiku += word + ' '
                    break
                # Remove word which have too many syllables
                elif tmpSyllables > remaining_syllables:
                    words.remove(word)

            # Pick a word randomly if we could not find a proper word
            # to end the line
            if remaining_syllables != 0:
                word = random.choice(words)
                remaining_syllables -= count_syllables(word)
                haiku += word + ' '
                try:
                    words = bigrams_dict[word]
                except:
                    # No successor for the selected word
                    raise NotImplementedError()

            # Line cannot be ended with the right number of syllables
            elif len(words) == 0:
                raise NotImplementedError()


        # End of line
        haiku += '\r\n'

    return haiku


if __name__ == '__main__':
    dataset = parse_dataset()

    bigrams = compute_bigrams(dataset)
    print "{} bigrams generated".format(len(bigrams))

    bigrams_dict = build_bigrams_dictionary(bigrams)
    print "bigrams dictionary contains {} entries\n".format(len(bigrams_dict.keys()))

    print generate_haiku(bigrams_dict)
