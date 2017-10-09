import json
from pymongo import MongoClient

def jsonToMongo(letters):
    for s in letters:
        d = dict()
        with open('./indexed/indexFile_' + s + '.json', 'r') as fp:
            k = json.load(fp)
        client = MongoClient()
        client = MongoClient('mongodb://localhost:27017/')
        db = client['indexDatabase_'+s]
        posts = db.posts
        print 'Now structuring'
        toSave = [{'k': myId, 'indexes': k[myId]} for myId in k]
        print 'Now inserting'
        result = posts.insert_many(toSave)
