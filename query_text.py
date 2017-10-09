import re, ast, codecs
import CONSTANTS
from pymongo import MongoClient

class QueryExecuter:
    def __init__(self):
        self.strings = []
        self.wild_cards = []
        self.client = MongoClient('mongodb://localhost:27017/')
        self.regex = ''

    def parseQuery(self, query):
        elements = query.split()
        self.strings = [string.replace('"', '') for string in elements[::2]]
        self.wild_cards = [ast.literal_eval(element) for element in elements[1::2]]

    def buildRegex(self,query):
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
        if not self.regex or self.regex == '':
            self.regex = self.buildRegex(query)
        matchObj = re.findall(self.regex, text)
        if (matchObj):
            return matchObj
        else:
            return []

    def findQueryFromFile(self, query, fNames, pagesDir = CONSTANTS.pagesFolder):
        # initialize all query data
        self.regex = ''
        self.strings = self.wild_cards = []
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

    def runQueryRaw(self, query, pagesDir = './pages_new', path = None):
        # initialize all query data
        self.regex = ''
        self.strings = self.wild_cards = []
        result = []
        if path and path.endswith('.txt'):
            print 'Looking only in file "' + path + '"'
            with open(pagesDir + '/' + path) as text:
                result = self.findQuery(query, text.read())
        elif path and len(path) == 1:
            print 'looking in all files with the letter "' + path + '"'
            for filename in os.listdir(pagesDir + '/' + path):
                with open(pagesDir + '/' + path + '/' + filename) as text:
                    result += self.findQuery(query, text.read())
        else:
            print 'looking in all files in the folders in', pagesDir
            for folder in os.listdir(pagesDir):
                print 'looking in {0} \r'.format(folder),
                for filename in os.listdir(pagesDir + '/' + folder):
                    print 'currently scanning {0} \r'.format(filename),
                    with open(pagesDir + '/' + folder + '/' + filename) as text:
                        result += self.findQuery(query, text.read())
        return result

    def getFromIndex(self, string, letter):
        s = 'indexDatabase_'+letter.lower()
        db = self.client[s]
        posts = db.posts
        ind = posts.find_one({"id": string})
        if ind!=None:
            return set(ind['indexes'])
        return None

    def findQueryFromLettersGiven(self, query, startL):
        print 'Looking for', query, '...'
        allFSet = set()
        self.parseQuery(query)
        for s in startL:
            fileIndexesToLook = set.intersection(*[self.getFromIndex(string, s) for string in self.strings])
            allFSet = allFSet.union(set([s + '/' + str(f)+'.txt' for f in fileIndexesToLook]))
        return self.findQueryFromFile(query, allFSet)
