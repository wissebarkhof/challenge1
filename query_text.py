import re, ast, sys, time, os,codecs
import pickle
import json
import CONSTANTS

class QueryExecuter:
    def __init__(self):
        self.jsonLoaded = False
        self.jsonFTable = None
        self.jsonIndexes = None
        self.d = {n: None for n in CONSTANTS.letters}
        self.d1 = {n: None for n in CONSTANTS.letters}
        self.strings = []
        self.wild_cards = []

    def parseQuery(self, query):
        elements = query.split()
        self.strings = [string.replace('"', '') for string in elements[::2]]
        self.wild_cards = [ast.literal_eval(element) for element in elements[1::2]]

    def buildRegex(self,query):
        if not (self.strings or self.query):
            self.parseQuery(query)
        regex_string = r''
        for index, string in enumerate(self.strings):
            regex_string += re.escape(string)
            if (index < (len(self.strings) - 1)):
                min_char, max_char = self.wild_cards[index]
                unknown = '.{' + str(min_char) + ',' + str(max_char) + '}'
                regex_string += unknown
        return regex_string

    def findQuery(self,query, text):
        regex = self.buildRegex(query)
        matchObj = re.findall(regex, text)
        if (matchObj):
            return matchObj

    def findQueryFromFile(self, query, fNames, pagesDir = './pages'):
        out = []
        print 'There are ', len(fNames), 'pages to run', query
        for name in fNames:
            print ' - running the query on', name
        for fN in fNames:
            fileDir = pagesDir+'/'+ fN
            f = codecs.open(fileDir)
            text = f.read()
            x = self.findQuery(query,text)
            if x:
                out += x
        return out

    def getFromIndex(self, string, letter):
        # do a partial lookup on the keys in the index ->>> too slow

        # keys = [k for k,v in self.d[letter].items() if k.startswith(string)]
        # indexes = set()
        # for key in keys:
        #     indexes = indexes.union(self.d[letter][key])
        # # print len(keys), ' keys found for"', string, '" on "', letter, '"'
        # print 'PARTIAL LOOKUP', len(indexes), ' indexes found for"', string, '" on "', letter, '"'
        #
        # indexes = self.d[letter]
        # result = indexes.get(string, set())
        # print 'FULL LOOKUP', len(result), ' indexes found for"', string, '" on "', letter, '"'

        return self.d[letter].get(string, set())

    def loadIndexesFromLetters(self, startL):
        print 'loading all needed indexes for', startL
        for s in startL:
            print 'loading indeces for pages starting with', s
            if self.d[s] == None:
                with open('./indexed/indexFile_' + s + '.json', 'r') as fp:
                    k = json.load(fp)
                for i in k[0]:
                    k[0][i] = set(k[0][i])
                self.d[s] = k[0]
                self.d1[s] = k[1]
                k = None


    def findQueryFromLettersGiven(self, query, startL):
        print 'Looking for', query, '...'
        allFSet = set()
        self.parseQuery(query)
        for s in startL:
            fTable = self.d1[s]
            indexes = self.d[s]
            fileIndexesToLook = set.intersection(*[self.getFromIndex(string, s) for string in self.strings])
            # TODO:  we could merge these lookups if the fileIndex = fileName
            allFSet = allFSet.union(set([s + '/'+ fTable[str(f)] for f in fileIndexesToLook]))
        return self.findQueryFromFile(query, allFSet)

