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

    def buildRegex(self,query):
        elements = query.split()
        strings = [string.replace('"', '') for string in elements[::2]]
        wild_cards = [ast.literal_eval(element) for element in elements[1::2]]
        regex_string = r''
        for index, string in enumerate(strings):
            regex_string += re.escape(string)
            if (index < (len(strings) - 1)):
                min_char, max_char = wild_cards[index]
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
        print 'There are ', len(fNames), 'pages to running query'
        print fNames
        for fN in fNames:
            f = codecs.open(pagesDir+'/'+ fN)
            text = f.read()
            x = self.findQuery(query,text)
            if x!=None:
                out.append(x)
        return out

    def findQueryFromLettersGiven(self, query, startL):
        for s in startL:
            if self.d[s] == None:
                with open('./indexed/indexFile_' + s + '.json', 'r') as fp:
                    k = json.load(fp)
                for i in k:
                    k[i] = set(k[i])
                self.d[s] = k
                k = None
                with open('./indexed/indexFile_' + s + 'IndexToFileName.json', 'r') as fp:
                    self.d1[s] = json.load(fp)

        L = query.split()
        word1 = L[0].replace('"', '')
        word2 = L[2].replace('"', '')
        allFSet = set()

        for s in startL:
            fTable = self.d1[s]
            indexes = self.d[s]
            fileIndexesToLook = indexes.get(word1,set()).intersection(indexes.get(word2,set()))
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
