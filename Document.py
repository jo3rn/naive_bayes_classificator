from BagOfWords import BagOfWords
import os, re

class Document(object):
    ''' used for training and testing documents
        learn == True: training
        learn == False: testing
    '''

    def __init__(self, vocabulary):
        self.__name = ""
        self.__document_class = None
        self._words_and_freq = BagOfWords()
        Document._vocabulary = vocabulary

    def read_document(self, filename, learn=False):
        ''' encoding should be utf-8 or iso-8859
            words are stored in self._words_and_freq
        '''
        try:
            text = open(filename, 'r', encoding='utf-8').read()
        except UnicodeDecodeError:
            text = open(filename, 'r', encoding='latin-1').read()
        text = text.lower()
        words = re.split("[^\wäöüÜÖÄß]*", text)

        self._number_of_words = 0
        for word in words:
            self._words_and_freq.add_word(word)
            if learn:
                Document._vocabulary.add_word(word)

    def __add__(self, other):
        ''' overloading + operator to add BagOfWords of two documents '''
        res = Document(Document._vocabulary)
        res.words_and_freq = self._words_and_freq + other._words_and_freq
        return res

    def vocabulary_length(self):
        ''' return length of vocabulary '''
        return len(Document._vocabulary)

    def WordsAndFreq(self):
        ''' return dictionary with keys (words) and values (frequencies) '''
        return self._words_and_freq.BagOfWords()

    def Words(self):
        ''' return words of Document object '''
        d = self._words_and_freq.BagOfWords()
        return d.keys()

    def WordFreq(self, word):
        ''' return frequency of word in document '''
        bow = self._words_and_freq.BagOfWords()
        if word in bow:
            return bow[word]
        else:
            return 0

    def __and__(self, other):
        ''' return list of words occuring in both documents '''
        intersection = []
        words_one = self.Words()
        for word in other.Words():
            if word in words_one:
                intersection += [word]
        return intersection


class DocumentClass(Document):
    def __init__(self, vocabulary):
        Document.__init__(self, vocabulary)
        self._number_of_docs = 0

    def Probability(self, word):
        ''' return probability of word in class self '''
        voc_len = Document._vocabulary.len()
        sum_n = 0
        for i in range(voc_len):
            sum_n = DocumentClass._vocabulary.WordFreq(word)
        n = self._words_and_freq.WordFreq(word)
        erg = 1 + n
        erg /= voc_len + sum_n
        return erg

    def __add__(self, other):
        ''' overloading + operator to add BagOfWords of DocumentClass objects'''
        res = DocumentClass(self._vocabulary)
        res._words_and_freq = self._words_and_freq + other._words_and_freq
        return res

    def SetNumberOfDocs(self, number):
        self._number_of_docs = number

    def NumberOfDocuments(self):
        return self._number_of_docs


class Pool(object):
    def __init__(self):
        self.__document_classes = {}
        self.__vocabulary = BagOfWords()

    def sum_words_in_class(self, dclass):
        ''' number of times all different words if a dclass appear in a class'''
        sum = 0
        for word in self.__vocabulary.Words():
            waf = self.__document_classes[dclass].WordsAndFreq()
            if word in waf:
                sum += waf[word]
        return sum

    def learn(self, directory, dclass_name):
        ''' directory: path where files of dclass_name can be found '''
        x = DocumentClass(self.__vocabulary)
        dir = os.listdir(directory)
        for file in dir:
            d = Document(self.__vocabulary)
            print(directory + "/" + file)
            d.read_document(directory + "/" + file, learn = True)
            x = x + d
        self.__document_classes[dclass_name] = x
        x.SetNumberOfDocs(len(dir))

    def Probability(self, doc, dclass = ""):
        ''' calculates probability for dclass given a document doc '''
        if dclass:
            sum_dclass = self.sum_words_in_class(dclass)
            prob = 0

            d = Document(self.__vocabulary)
            d.read_document(doc)

            for j in self.__document_classes:
                sum_j = self.sum_words_in_class(j)
                prod = 1
                for i in d.Words():
                    wf_dclass = 1 + self.__document_classes[dclass].WordFreq(i)
                    wf = 1 + self.__document_classes[j].WordFreq(i)
                    r = wf * sum_dclass / (wf_dclass * sum_j)
                    prod *= r

                prob += prod * self.__document_classes[j]. \
                    NumberOfDocuments() / self.__document_classes[dclass \
                    ].NumberOfDocuments()

            if prob != 0:
                return 1 / prob
            else:
                return -1

        else:
            prob_list = []
            for dclass in self.__document_classes:
                prob = self.Probability(doc, dclass)
                prob_list.append([dclass, prob])
            prob_list.sort(key = lambda x: x[1], reverse = True)
            return prob_list

    def DocumentIntersectionWithClasses(self, doc_name):
        res = [doc_name]
        for dc in self.__document_classes:
            d = Document(self.__vocabulary)
            d.read_document(doc_name, learn = False)
            o = self.__document_classes[dc] & d
            intersection_ratio = len(o) / len(d.Words())
            res += (dc, intersection_ratio)
        return res
