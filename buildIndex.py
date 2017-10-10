import os
from collections import defaultdict
import pickle, re
import codecs
import json
import nltk
import utils

class WikiIndexer:
    def __init__(self, page_folder, output_name, file_names = None):
        self.page_folder = page_folder
        self.output_name = output_name
        if file_names:
            self.file_names = file_names
        else:
            self.file_names = os.listdir(page_folder)
        self.index = defaultdict(set)

    def get_number_of_texts(self):
        return len(self.file_names)

    def __clean_text(self, text):
        tokens = nltk.word_tokenize(text)
        return tokens

    def build_index(self):
        for fIndex in range(len(self.file_names)):
            print '{0}/{1} \r'.format(fIndex, len(self.file_names)),
            fName = self.file_names[fIndex]
            indexToSave = fName[:-4]#Only part without txt
            f = codecs.open(self.page_folder+fName, 'r')
            text = f.read().decode('utf-8')
            words = self.__clean_text(text)
            for word in words:
                self.index[word].add(indexToSave)

    def json_dump(self,name):
        if name:
            outfile_name = '{0}/indexFile_{1}'.format(self.output_name, name)
        else:
            outfile_name = '{0}/index_first_{1}_texts_pickle'.format(self.output_name, self.get_number_of_texts())

            raise Exception('A problem with file name')
        print 'JSON dumping index in ', outfile_name

        for i in self.index:
            self.index[i] = list(self.index[i])

        with open(outfile_name + '.json', 'w') as fp:
            json.dump(self.index, fp)
    def mongoDump(self,name):
        from pymongo import MongoClient
        client = MongoClient()
        client = MongoClient('mongodb://localhost:27017/')
        db = client['indexDatabase_'+name]
        posts = db.posts
        posts.insert_many([{'k': myId, 'indexes': list(self.index[myId])} for myId in self.index])
    def find_text(self, word):
        indeces = self.index[word]
        print 'Found', len(indeces), 'number of texts'


if __name__ == "__main__":
    indexer = WikiIndexer('pages_all', 'indexed_all')
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
