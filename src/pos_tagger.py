import nltk

class POSTagger:
    tokenizer = nltk.tokenize.RegexpTokenizer(r"\w+|[!,.:;?]|'s")
    POSSESSIVE = '\'s'
    PUNCTUATION = ['!', ',', '.', ':', ';', '?']

    @staticmethod
    def get_pos_tagged_dataset(dataset):
        """
        Return a dictionary of list of tagged haikus (a haiku is here a list of tagged words)
        """
        return POSTagger.__build_tagged_dataset(dataset)

    @staticmethod
    def get_tagged_word_tree(pos_tagged_dataset):
        """
        Return a dictionary:
        - key: tag
        - value: list of (word, probability) following the key in the corpus
                     ordered by descending probability
        """
        return POSTagger.__build_tagged_word_tree(pos_tagged_dataset)

    @staticmethod
    def __build_tagged_dataset(dataset):
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
                # TODO: get rid of possesive form
                words = POSTagger.tokenizer.tokenize(haiku)
                tagged_words = nltk.pos_tag(words)
                tagged_haikus.append(tagged_words)
            tagged_dataset[key] = tagged_haikus

        return tagged_dataset

    @staticmethod
    def __build_tagged_word_tree(dataset):
        word_tree = {}

        # Build dictionary
        for key in dataset.keys():
            for haiku in dataset[key]:
                for word, tag in haiku:
                    if not tag in word_tree:
                        word_tree[tag] = {}

                    if word in word_tree[tag]:
                        word_tree[tag][word] = word_tree[tag][word] + 1
                    else:
                        word_tree[tag][word] = 1

        # Calculate probabilities
        for key in word_tree:
            sorted_words = sorted(word_tree[key].items(), key=lambda tuple: tuple[1], reverse=True)
            sum_words = sum(n for (word, n) in sorted_words)
            word_tree[key] = map(lambda (word, n): (word, float(n)/sum_words), sorted_words)

        return word_tree
