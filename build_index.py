import os
from collections import defaultdict
import pickle, re

class WikiIndexer:
    def __init__(self, page_folder):
        self.page_folder = page_folder
        self.file_names = os.listdir(page_folder)
        self.texts = []
        self.text_line_numbers = {}
        self.index = defaultdict(list)

    def get_number_of_texts(self):
        return len(self.file_names)

    def __read_texts(self):
        print 'reading in texts'
        for index, file_name in enumerate(self.file_names):
            page_name, _ = file_name.split('.')
            self.text_line_numbers[page_name] = index
            with open(self.page_folder + '/' + file_name) as infile:
                line = page_name + ' | ' + infile.read()
                self.texts.append(line)

    def __write_texts_to_file(self):
        self.__read_texts()
        outfile_name = 'indexed/first_{0}_texts.txt'.format(self.get_number_of_texts())
        print 'writing', self.get_number_of_texts(), 'texts to', outfile_name
        with open(outfile_name, 'w') as outfile:
            for text_line in self.texts:
                outfile.write(text_line)

    def __clean_word(self, word):
        step1 = re.sub('[/.,|\[]]', ' ', word.lower())
        return re.sub("[^A-Za-z0-9 ']", '', step1.lower())

    def build_index(self):
        self.__write_texts_to_file()
        for i, text in enumerate(self.texts):
            print 'building index for text {0} out of {1} \r'.format(i, self.get_number_of_texts()),
            page_name = text.split(' | ')[0]
            index = self.text_line_numbers[page_name]
            words = list(set([self.__clean_word(word) for word in text.split(' ')]))
            for word in words:
                self.index[word].append(index)

    def pickle_dump(self):
        outfile_name = 'indexed/index_first_{0}_texts_pickle'.format(self.get_number_of_texts())
        print 'pickle dumping index in ', outfile_name
        with open(outfile_name, 'w') as outfile:
            pickle.dump(outfile, self.index)

    def find_text(self, word):
        indeces = self.index[word]
        print 'Found', len(indeces), 'number of texts'
        return [self.texts[i] for i in indeces]

if __name__ == "__main__":
    indexer = WikiIndexer('pages')
    indexer.build_index()
    print 'Found ', len(indexer.index.keys()), 'different words to index'
    test_word = 'wikipedia'
    print 'Testing the indeces for the word "{0}"'.format(test_word)
    texts = indexer.find_text(test_word)
    for text in texts:
        print 'The word "{0}" appears at index'.format(test_word), text.index(test_word)
