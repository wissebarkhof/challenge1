import xml.etree.ElementTree as etree
import re
import codecs
import urllib2



class Extractor:

    def __init__(self, fileAdress, pageRange = [0, float('inf')]):
        self.limit = pageRange[1]
        self.start = pageRange[0]
        self.fileAdress = fileAdress


    def titleToFileName(self,title):
        return './pages/' + re.sub(r'\W', '', title) + '.txt'

    def saveToFile(self, fileName,text):
        f = codecs.open(fileName, 'w', "utf-8")
        f.write(text)
        f.close()


    def extractTextFromHugeXML(self):
        index = 0
        blockStart = '{http://www.mediawiki.org/xml/export-0.10/}'
        for event, elem in etree.iterparse(self.fileAdress, events=('start', 'end')):

            if 'page' in elem.tag and event == 'start':
                if index%1000 == 0:
                    print 'Now processing ', index
                index += 1

                if index > self.limit:
                    break

                if index < self.start:
                    continue
                textElem = elem.find(blockStart+'revision//'+blockStart+'text')
                titleElem = elem.find(blockStart+'title')
                if textElem!=None:
                    fileText = textElem.text
                    title = titleElem.text
                    if title != None and fileText!=None:
                        self.saveToFile(self.titleToFileName(title),self.processText(fileText))
                else:
                    continue
    def processText(self,s):
        s = s.lower()
        s = s.replace('\n', ' ')
        return s



if __name__ == "__main__":
    bigFileAdress = '/home/ahmet/Downloads/enwiki-20170820-pages-articles.xml'
    pageRangeToExtract = [100000,1000000]
    extractor = Extractor(bigFileAdress,pageRangeToExtract)
    extractor.extractTextFromHugeXML()
