class BagOfWords(object):
    ''' frequency of word usage in a document '''

    def __init__(self):
        self.__number_of_words = 0
        self.__bag_of_words = {}

    def __add__(self, other):
        ''' overloading + operator to join two BagOfWords '''
        erg = BagOfWords()
        sum = erg.__bag_of_words
        for key in self.__bag_of_words:
            sum[key] = self.__bag_of_words[key]
            if key in other.__bag_of_words:
                sum[key] += other.__bag_of_words[key]
        for key in other.__bag_of_words:
            if key not in sum:
                sum[key] = other.__bag_of_words[key]
        return erg

    def add_word(self, word):
        ''' add word to dictionary __bag_of_words '''
        self.__number_of_words += 1
        if word in self.__bag_of_words:
            self.__bag_of_words[word] += 1
        else:
            self.__bag_of_words[word] = 1

    def len(self):
        ''' return number of different words of an object '''
        return len(self.__bag_of_words)

    def Words(self):
        ''' return list of words of an object '''
        return self.__bag_of_words.keys()

    def BagOfWords(self):
        ''' return dictionary with keys (words) and values (frequencies) '''
        return self.__bag_of_words

    def WordFreq(self, word):
        ''' return frequency of a word '''
        if word in self.__bag_of_words:
            return self.__bag_of_words[word]
        else:
            return 0
