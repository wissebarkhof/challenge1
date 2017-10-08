import buildIndex
import string
import os
import CONSTANTS

class indexerMaster:

    def __init__(self,page_folder):
        self.page_folder = page_folder

    def createAllIndexesByStartingLetter(self):
        for first in CONSTANTS.letters:
            print 'Creating index for "', first, '"'
            subPageFolder = self.page_folder+"/"+first+"/"
            fNames = os.listdir(subPageFolder)
            if fNames:
                indexer = buildIndex.WikiIndexer(subPageFolder, 'indexed_all', file_names=fNames)
                indexer.build_index()
                name = first
                indexer.json_dump(name.lower())

    def creatAllIndexAsAWhole(self):
        fNames = os.listdir(self.page_folder)
        indexer = buildIndex.WikiIndexer(self.page_folder,file_names=fNames)
        indexer.build_index()
        name = 'allIndexes'
        indexer.json_dump(name)


if __name__ == "__main__":
    master = indexerMaster('pages_all')
    print 'START'
    master.createAllIndexesByStartingLetter()
    # master.creatAllIndexAsAWhole()
