import os
from collections import defaultdict
import pickle, re
import codecs
import json
import nltk

class WikiIndexer:
    def __init__(self, page_folder, file_names = None):
        self.page_folder = page_folder

        if file_names:
            self.file_names = file_names
        else:
            self.file_names = os.listdir(page_folder)

        self.index = defaultdict(set)
        self.indexToFileName = {}

    def get_number_of_texts(self):
        return len(self.file_names)

    def __clean_text(self, text):
        tokens = nltk.word_tokenize(text)
        return tokens

    def build_index(self):
        for fIndex in range(len(self.file_names)):
            print '{0}/{1} \r'.format(fIndex, len(self.file_names)),
            fName = self.file_names[fIndex]
            self.indexToFileName[fIndex] = fName
            self.indexToFileName[fName] = fIndex
            f = codecs.open(self.page_folder + '/' + fName, 'r')
            text = f.read().decode('utf-8')
            words = self.__clean_text(text)
            for word in words:
                self.index[word].add(fIndex)

    def json_dump(self,name):
        if name:
            outfile_name = 'indexed/indexFile_{0}'.format(name)
        else:
            outfile_name = 'indexed/index_first_{0}_texts_pickle'.format(self.get_number_of_texts())

        print 'JSON dumping index in ', outfile_name
        # toSave = [self.indexToFileName, self.index]
        for i in self.index:
            self.index[i] = list(self.index[i])
        with open(outfile_name+'.json', 'w') as fp:
            json.dump(self.index, fp)
        with open(outfile_name+'IndexToFileName.json', 'w') as fp:
            json.dump(self.indexToFileName,fp)

    def find_text(self, word):
        indeces = self.index[word]
        print 'Found', len(indeces), 'number of texts'
    #     return [self.texts[i] for i in indeces]

if __name__ == "__main__":
    indexer = WikiIndexer('pages')
    indexer.build_index()
    print 'Found ', len(indexer.index.keys()), 'different words to index'
    test_words = [
        'python',
        'wikipedia',
        'links',
        '[[',
        ]
    for word in test_words:
        print 'Testing the indeces for the word "{0}"'.format(word)
        texts = indexer.find_text(word)
