import buildIndex
import string
import os
import CONSTANTS

indexFolder = CONSTANTS.toyIndexFolder
class indexerMaster:

    def __init__(self,page_folder):
        self.page_folder = page_folder

    def createAllIndexesByStartingLetterJSON(self):
        for first in CONSTANTS.letters:
            print 'Creating index for "', first, '"'
            subPageFolder = self.page_folder+"/"+first+"/"
            fNames = os.listdir(subPageFolder)
            if fNames:
                indexer = buildIndex.WikiIndexer(subPageFolder, indexFolder, file_names=fNames)
                indexer.build_index()
                name = first
                indexer.json_dump(name.lower())
    def createAllIndexesByStartingLetterMongo(self):
        for first in CONSTANTS.letters:
            print 'Creating index for "', first, '"'
            subPageFolder = self.page_folder+"/"+first+"/"
            fNames = os.listdir(subPageFolder)
            if fNames:
                indexer = buildIndex.WikiIndexer(subPageFolder, indexFolder, file_names=fNames)
                indexer.build_index()
                name = first
                indexer.mongoDump(name.lower())

if __name__ == "__main__":
    master = indexerMaster(CONSTANTS.toyPagesFolder)
    print 'START'
    # master.createAllIndexesByStartingLetterMongo()
    master.createAllIndexesByStartingLetterJSON()