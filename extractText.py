import xml.etree.ElementTree as etree
import re
import codecs
import urllib2

bigFileAdress = '/home/ahmet/Downloads/enwiki-20170820-pages-articles.xml'
def titleToFileName(title):
    return './pages/' + re.sub(r'\W', '', title) + '.txt'

def saveToFile(fileName,text):
    f = codecs.open(fileName, 'w', "utf-8")
    f.write(text)
    f.close()


def extractTextFromHugeXML(fileName):
    index = 0
    limit = 1000

    blockStart = '{http://www.mediawiki.org/xml/export-0.10/}'
    for event, elem in etree.iterparse(fileName, events=('start', 'end')):
        if 'page' in elem.tag and event == 'start':
            textElem = elem.find(blockStart+'revision//'+blockStart+'text')
            titleElem = elem.find(blockStart+'title')
            if textElem!=None:
                fileText = textElem.text
                title = titleElem.text
                if title != None and fileText!=None:
                    saveToFile(titleToFileName(title),processText(fileText))
                    index+=1
                    if index>limit:
                        break


            else:
                continue
            b = None
            # for i in elem:
            #     if 'revision' in i.tag:


    # return processText(text)

def processText(s):
    s = s.lower()
    s = s.replace('\n', ' ')

    return  s


extractTextFromHugeXML(bigFileAdress)