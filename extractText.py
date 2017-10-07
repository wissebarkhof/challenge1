import xml.etree.ElementTree as etree
import re, codecs, urllib2, sys
import CONSTANTS
import os
import utils

class Extractor:

<<<<<<< HEAD
    def __init__(self, fileAdress):
        self.limit = float('inf')
        self.start = 0

=======
    def __init__(self, fileAdress, pageRange = [0, float('inf')], pagesFolder = './pages/'):
        self.limit = pageRange[1]
        self.start = pageRange[0]
>>>>>>> b7ed0566cf300bcd56923b62f0e5ba512ff25d30
        self.fileAdress = fileAdress
        self.pagesFolder = pagesFolder


<<<<<<< HEAD
    def titleToFileName(self,title):
        return './pages_all/' + re.sub(r'\W', '', title) + '.txt'
=======
    def checkAllSubFolders(self, folderNames = CONSTANTS.letters):
        for f in folderNames:
            directory = self.pagesFolder+f
            if not os.path.exists(directory):
                os.makedirs(directory)
>>>>>>> b7ed0566cf300bcd56923b62f0e5ba512ff25d30

    def saveToFile(self, fileName,text):
        f = codecs.open(fileName, 'w', "utf-8")
        f.write(text)
        f.close()

    def extractTextFromHugeXML(self):
        self.checkAllSubFolders()
        index = 0
        blockStart = '{http://www.mediawiki.org/xml/export-0.10/}'
        for event, elem in etree.iterparse(self.fileAdress, events=('start', 'end')):
            if 'page' in elem.tag and event == 'start':
                # if index % 1000 == 0:
                print 'Now processing {0} \r'.format(index),
                index += 1
                if index > self.limit:
                    break
                if index < self.start:
                    elem.clear()
                    continue
                textElem = elem.find(blockStart+'revision//'+blockStart+'text')
                titleElem = elem.find(blockStart+'title')
                if textElem!=None:
                    fileText = textElem.text
                    title = titleElem.text
                    if title != None and fileText!=None and title !='':
                        self.saveToFile(utils.titleToFileAdress(title, self.pagesFolder), self.processText(fileText))
                else:
                    continue
            elem.clear()
    def processText(self,s):
        s = s.lower()
        s = s.replace('\n', ' ')
        return s



if __name__ == "__main__":
<<<<<<< HEAD
=======
    page_from = 0
    page_to = 100000
    print 'Fetching pages from', page_from, 'to', page_to
>>>>>>> b7ed0566cf300bcd56923b62f0e5ba512ff25d30
    bigFileAdress = str(sys.argv[1])
    extractor = Extractor(bigFileAdress)
    extractor.extractTextFromHugeXML()
