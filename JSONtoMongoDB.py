import json
from pymongo import MongoClient
import CONSTANTS
def jsonToMongo(letters, indexFolder = CONSTANTS.indexFolder):

    for s in letters:
        print "working for ",s
        d = dict()
        with open(indexFolder+'/indexFile_' + s + '.json', 'r') as fp:
            k = json.load(fp)
        client = MongoClient()
        client = MongoClient('mongodb://localhost:27017/')
        db = client['indexDatabase_'+s]
        posts = db.posts
        print 'Now structuring'
        toSave = [{'k': myId, 'indexes': k[myId]} for myId in k]
        print 'Now inserting'
        result = posts.insert_many(toSave)

jsonToMongo('JKL'.lower())
