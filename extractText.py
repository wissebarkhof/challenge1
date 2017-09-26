import xml.etree.ElementTree as ET
import codecs

def extractText(fileName ='HenryDuncan'):

    tree = ET.parse(fileName)
    root = tree.getroot()
    x  =root.find('revision')
    if x:
        x = x.find('text')
        if x == None:
            return None
    else:
        return None

    return processText(x.text)

def processText(s):
    s = s.lower()
    s = s.replace('\n', ' ')

    return  s


s =  extractText()
f = codecs.open('a2.txt','w',"utf-8")
f.write(s)