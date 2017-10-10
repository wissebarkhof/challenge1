import re, ast, codecs,os,json
import CONSTANTS
from pymongo import MongoClient

class QueryExecuter:

    #This class runs the queries

    def __init__(self,useJSON = False, indexFolder = None, pagesFolder = CONSTANTS.pagesFolder):
        self.useJSON = useJSON #We can use JSON or MongoDB as index databases
        self.pagesFolder = pagesFolder#Page folder to look
        if(self.useJSON):
            self.jsonLoaded = False
            self.jsonFTable = None
            self.jsonIndexes = None
            self.d = {n: None for n in CONSTANTS.letters}#If JSON is used we will load all indexes as dictionary
            #Keys are words and values are ids of files which these word is passing -> "cat":[1,188,193]
            if indexFolder == None:
                raise Exception('Give an index folder')
            else:
                self.indexFolder = indexFolder
            self.loadIndexesFromLetters(CONSTANTS.letters)
        self.strings = []
        self.wild_cards = []
        self.client = MongoClient('mongodb://localhost:27017/')
        self.regex = ''

    def parseQuery(self, query): #Divide query into words and wild cards
        elements = query.split()
        self.strings = [string.replace('"', '') for string in elements[::2]]
        self.wild_cards = [ast.literal_eval(element) for element in elements[1::2]]

    def buildRegex(self,query):#Get regex string
        self.parseQuery(query)
        regex_string = r''
        for index, string in enumerate(self.strings):
            regex_string += re.escape(string)
            if (index < (len(self.strings) - 1)):
                min_char, max_char = self.wild_cards[index]
                unknown = '.{' + str(min_char) + ',' + str(max_char) + '}'
                regex_string += unknown
        return regex_string

    def findQuery(self,query, text):#Run regex on text
        if not self.regex or self.regex == '':
            self.regex = self.buildRegex(query)
        matchObj = re.findall(self.regex, text)
        if (matchObj):
            return matchObj
        else:
            return []

    def findQueryFromFile(self, query, fNames):#Finds results from a list of files
        #Basically reads files and run regex on them
        pagesDir = self.pagesFolder
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

    def runQueryRaw(self, query, path = None):#Brute force approach
        pagesDir = self.pagesFolder
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

    def getFromIndex(self, word, letter):#Gets the indexes
        #Index files are organized in terms of letters
        #So if one tries to look only the pages where "cat" is passing and where the title of the page starts with 'a'
        #Just have self.d['a'].get("cat", set())
        #OR self.client['a'].posts.find_one({"k":"cat"}) // FOR MONGODB
        if not self.useJSON:
            s = 'indexDatabase_'+letter.lower()
            db = self.client[s]
            posts = db.posts
            ind = posts.find_one({"k": word})
            if ind!=None:
                return set(ind['indexes'])
            return set()
        else:
            if not self.jsonLoaded:
                self.loadIndexesFromLetters(CONSTANTS.letters)
            return self.d[letter].get(word, set())

    def loadIndexesFromLetters(self, startL):#It loads json index files !!WARNING NOT FEASIBLE FOR BIG FILES
        print 'loading all needed indexes for', startL
        for s in startL:
            print 'loading indeces for pages starting with', s
            if self.d[s] == None:
                with open(self.indexFolder+'/indexFile_' + s + '.json', 'r') as fp:
                    k = json.load(fp)
                for i in k:
                    k[i] = set(k[i])
                self.d[s] = k
                k = None

    def word_index_findQueryFromLettersGiven(self, query, startL):#Word index query function
        #StartL is the letters to look for , so if we only look in letter 'a' startL = 'a'
        print 'Looking for', query, '...'
        allFSet = set()
        self.parseQuery(query)
        for s in startL:
            fileIndexesToLook = set.intersection(*[self.getFromIndex(string, s) for string in self.strings])#Get the intersecting files
            #for example cat:[1,2,10,15] dog:[10,12,15] then only do query in [10,15]
            allFSet = allFSet.union(set([s + '/' + str(f)+'.txt' for f in fileIndexesToLook]))
        return self.findQueryFromFile(query, allFSet)
