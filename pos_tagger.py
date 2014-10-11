import json
import nltk

class POSTagger:
    HAIKU_FILE = 'haikus.json'

    @staticmethod
    def get_pos_tagged_dataset():
        return POSTagger.__build_tagged_corpus(POSTagger.__parse_dataset())

    @staticmethod
    def __parse_dataset():
        """
        Return the dataset as a dictionary
        """
        print "Parsing dataset..."
        json_data = open(POSTagger.HAIKU_FILE)
        dataset = json.load(json_data)
        json_data.close()

        return dataset

    @staticmethod
    def __build_tagged_corpus(dataset):
        """
        Return a list of list of tagged word
        """
        # The following code allows the sentence tokenization of a text (useless here)
        # sent_detector = nltk.data.load('tokenizers/punkt/english.pickle')
        # sentences = sent_detector.tokenize(dataset['SUMMER Terrestrial'][0].strip()))
        print "POS-tagging dataset..."

        return [nltk.pos_tag(nltk.word_tokenize(haiku)) for key in dataset.keys() for haiku in dataset[key]]

        # Can also be done using the following instructions
        # corpus = []
        # for key in dataset.keys():
        #     for haiku in dataset[key]:
        #         words = nltk.word_tokenize(haiku)
        #         tagged_words = nltk.pos_tag(words)
        #         corpus.append(tagged_words)
        #
        # return corpus


if __name__ == '__main__':
    print POSTagger.get_pos_tagged_dataset()
