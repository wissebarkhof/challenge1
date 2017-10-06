import re, ast, sys, time, os,codecs
import pickle
import json
import CONSTANTS

class QueryExecuter:
    def __init__(self):
        self.jsonLoaded = False
        self.jsonFTable = None
        self.jsonIndexes = None
        self.d = {n.lower(): None for n in CONSTANTS.capitals}
        self.d1 = {n.lower(): None for n in CONSTANTS.capitals}
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
            f = codecs.open(pagesDir+'/'+ fN)
            text = f.read()
            x = self.findQuery(query,text)
            if x:
                out += x
        return out

    def getFromIndex(self, string, letter):
        # do a partial lookup on the keys in the index
        # keys = [k for k,v in self.d[letter].items() if string in k]
        # indexes = set()
        # for key in keys:
        #     indexes.union(self.d[letter][key])
        indexes = self.d[letter]
        result = indexes.get(string, set())
        return result

    def findQueryFromLettersGiven(self, query, startL):
        print 'Looking for', query, '...'
        allFSet = set()
        self.parseQuery(query)
        for s in startL:
            print 'scanning pages starting with', s
            if self.d[s] == None:
                with open('./indexed/indexFile_' + s + '.json', 'r') as fp:
                    k = json.load(fp)
                for i in k:
                    k[i] = set(k[i])
                self.d[s] = k
                k = None
                with open('./indexed/indexFile_' + s + 'IndexToFileName.json', 'r') as fp:
                    self.d1[s] = json.load(fp)
            fTable = self.d1[s]
            indexes = self.d[s]
            fileIndexesToLook = set.intersection(*[self.getFromIndex(string, s) for string in self.strings])
            # TODO:  we could merge these lookups if the fileIndex = fileName
            allFSet = allFSet.union(set([fTable[str(f)] for f in fileIndexesToLook]))
        return self.findQueryFromFile(query, allFSet)

    def findQueryFromJsonFileUsingIndex(self,query):
        if self.jsonLoaded == False:
            with open('./indexed/indexFile_allIndexes.json', 'r') as fp:
                self.jsonIndexes = json.load(fp)
            for i in self.jsonIndexes:
                self.jsonIndexes[i] = set(self.jsonIndexes[i])
            with open('./indexed/indexFile_allIndexesIndexToFileName.json', 'r') as fp:
                self.jsonFTable = json.load(fp)

        L = query.split()
        word1 = L[0].replace('"', '')
        word2 = L[2].replace('"', '')
        fileIndexesToLook = self.jsonIndexes[word1].intersection(self.jsonIndexes[word2])
        allFSet = set([self.jsonFTable[str(f)] for f in fileIndexesToLook])
        out = self.findQueryFromFile(query,allFSet)
        return out
