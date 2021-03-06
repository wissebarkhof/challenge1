import os
from collections import defaultdict
import pickle, re
import codecs
import json
import nltk
import utils

class WikiIndexer:
    #This class builds index pages. It is controlled by buildIndexForAllPages.py

    def __init__(self, page_folder, output_name, file_names = None):
        self.page_folder = page_folder # Folder where pages are stored
        self.output_folder = output_name
        if file_names:
            self.file_names = file_names # Files to index
        else:
            self.file_names = os.listdir(page_folder)
        self.index = defaultdict(set)

    def get_number_of_texts(self):
        return len(self.file_names)

    def __clean_text(self, text):
        tokens = nltk.word_tokenize(text)# This is the function we used to get words in a page
        return tokens

    def build_index(self):
        for fIndex in range(len(self.file_names)): # For every page
            print '{0}/{1} \r'.format(fIndex, len(self.file_names)),
            fName = self.file_names[fIndex]
            indexToSave = fName[:-4]#Only part without txt
            f = codecs.open(self.page_folder+fName, 'r')
            text = f.read().decode('utf-8')
            words = self.__clean_text(text) # Get all the words in this page
            for word in words:
                self.index[word].add(indexToSave) # Save it to the index

    def json_dump(self,name): #json saving
        if not os.path.exists(self.output_folder):
            os.makedirs(self.output_folder)
        if name:
            outfile_name = '{0}/indexFile_{1}'.format(self.output_folder, name)
        else:
            raise Exception('A problem with file name')

        print 'JSON dumping index in ', outfile_name

        for i in self.index:
            self.index[i] = list(self.index[i])

        with open(outfile_name + '.json', 'w') as fp:
            json.dump(self.index, fp)
    def mongoDump(self,name): # MongoDB saving
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
