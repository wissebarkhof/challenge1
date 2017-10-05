import os
from collections import defaultdict
import pickle, re
import codecs
import json

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

    def __clean_word(self, word):
        step1 = re.sub('[/.,|\[]]', ' ', word.lower())
        return re.sub("[^A-Za-z0-9 ']", '', step1.lower())

    def build_index(self):
        print 'building index'
        for fIndex in range(len(self.file_names)):
            if fIndex % 1000 == 0:
                print fIndex , '/' , len(self.file_names)
            fName = self.file_names[fIndex]
            self.indexToFileName[fIndex] = fName
            self.indexToFileName[fName] = fIndex
            f = codecs.open(self.page_folder + '/' + fName, 'r')
            text = f.read()
            words = list(set([self.__clean_word(word) for word in text.split(' ')]))
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
    test_word = 'wales'
    print 'Testing the indeces for the word "{0}"'.format(test_word)
    texts = indexer.find_text(test_word)
    indexer.pickle_dump('ac')
