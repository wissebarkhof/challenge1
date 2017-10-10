import buildIndex
import string
import os
import CONSTANTS

class indexerMaster:
    #This class builds indexer and saves it
    def __init__(self,page_folder,indexFolder):
        self.page_folder = page_folder
        self.indexFolder = indexFolder

    def createAllIndexesByStartingLetterJSON(self):
        for first in CONSTANTS.letters:#For every letter
            print 'Creating index for "', first, '"'
            subPageFolder = self.page_folder+"/"+first+"/"#Get pages starting with that letter
            fNames = os.listdir(subPageFolder)#Get the ids of the pages
            if fNames:
                indexer = buildIndex.WikiIndexer(subPageFolder, self.indexFolder, file_names=fNames)
                indexer.build_index()#Build index
                name = first
                indexer.json_dump(name.lower())#Save it as JSON

    def createAllIndexesByStartingLetterMongo(self): # Creates all the indexes in the given
        for first in CONSTANTS.letters:#For every letter
            print 'Creating index for "', first, '"'
            subPageFolder = self.page_folder+"/"+first+"/"#Get pages starting with that letter
            fNames = os.listdir(subPageFolder)#Get the ids of the pages
            if fNames:
                indexer = buildIndex.WikiIndexer(subPageFolder, self.indexFolder, file_names=fNames)
                indexer.build_index()#Build index
                name = first
                indexer.mongoDump(name.lower())#Save the index to database

if __name__ == "__main__":
    indexFolder = CONSTANTS.miniIndexFolder
    master = indexerMaster(CONSTANTS.miniPagesFolder, indexFolder)
    print 'START'
    # master.createAllIndexesByStartingLetterMongo()
    master.createAllIndexesByStartingLetterJSON()