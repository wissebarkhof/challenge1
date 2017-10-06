import buildIndex
import string
import os
import CONSTANTS

class indexerMaster:

    def __init__(self,page_folder):
        self.page_folder = page_folder

    def createAllIndexesByStartingLetter(self):
        for first in CONSTANTS.capitals:
            print 'Creating index for "', first, '"'
            fNames = filter(lambda s: s.startswith(first), os.listdir(self.page_folder))
            indexer = buildIndex.WikiIndexer(self.page_folder, file_names=fNames)
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
    master = indexerMaster('pages')
    print 'START'
    master.createAllIndexesByStartingLetter()
    # master.creatAllIndexAsAWhole()
