import buildIndex
import string
import os

class indexerMaster:
    capitals = 'ABCDEFGHIJKLMNOPQRSTUVWXYZ'
    def __init__(self,page_folder):
        self.page_folder = page_folder

    def createAllIndexes(self):
        for first in indexerMaster.capitals:
            fNames = filter(lambda s: s.startswith(first), os.listdir(self.page_folder))
            indexer = buildIndex.WikiIndexer(self.page_folder, file_names=fNames)
            indexer.build_index()
            name = first
            indexer.pickle_dump(name.lower())


if __name__ == "__main__":
    master = indexerMaster('pages')
    master.createAllIndexes()

