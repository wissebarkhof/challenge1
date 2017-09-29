import re, ast, sys, time, os,codecs
import pickle

class QueryExecuter:
    def __init__(self):
        pass

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
        for fN in fNames:
            f = codecs.open(pagesDir+'/'+ fN)
            text = f.read()
            x = self.findQuery(query,text)
            if x!=None:
                out.append(x)
        return out

    def findQueryFromFileUsingIndex(self,query, startL):
        L = query.split()
        word1 =L[0].replace('"','')
        word2 =L[2].replace('"','')

        allFSet = set()
        for s in startL:
            fileAddress = './indexed/indexFile_'+s+'.pickle'
            d = pickle.load(open(fileAddress,'rb'))
            fTable = d[0]
            indexes = d[1]
            fileIndexesToLook = indexes[word1].intersection(indexes[word2])
            allFSet = allFSet.union(set([fTable[f] for f in fileIndexesToLook]))

        return self.findQueryFromFile(query,allFSet)

