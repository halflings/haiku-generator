import json
import nltk

class POSTagger:
    @staticmethod
    def get_pos_tagged_dataset(haiku_file='haikus.json'):
        return POSTagger.__build_tagged_corpus(POSTagger.__parse_dataset(haiku_file))

    @staticmethod
    def __parse_dataset(haiku_file):
        """
        Return the dataset as a dictionary
        """
        print "Parsing dataset..."
        json_data = open(haiku_file)
        dataset = json.load(json_data)
        json_data.close()

        return dataset

    @staticmethod
    def __build_tagged_corpus(dataset):
        """
        Return a dictionary of list of tagged haikus
        """
        # The following unused code allows the sentence tokenization of a text (useless here)
        # sent_detector = nltk.data.load('tokenizers/punkt/english.pickle')
        # sentences = sent_detector.tokenize(dataset['SUMMER Terrestrial'][0].strip()))
        print "POS-tagging dataset..."

        # Feel free to transform it into a one-liner (if doable)
        tagged_dataset = {}
        for key in dataset.keys():
            tagged_haikus = []
            for haiku in dataset[key]:
                words = nltk.word_tokenize(haiku)
                # TODO: remove punctuaton and apostrophes (and possessive ? => 's)
                tagged_words = nltk.pos_tag(words)
                tagged_haikus.append(tagged_words)
            tagged_dataset[key] = tagged_haikus

        return tagged_dataset


if __name__ == '__main__':
    print POSTagger.get_pos_tagged_dataset()
