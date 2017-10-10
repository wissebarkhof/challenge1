import re
import unicodedata
import urllib2
import json

def titleToFileAdress(title, pagesFolder):
    def is_ascii(s):
        return all(ord(c) < 128 for c in s)
    fileName = re.sub(r'\W', '', title)
    if not title[0].isalnum() or len(fileName) == 0:
        fileName = ''.join( c if is_ascii(c) and c.isalnum() else str(ord(c)) for c in title)
        return pagesFolder +  r"other/" + fileName + '.txt'
    return pagesFolder + fileName[0].lower() + r"/" + re.sub(r'\W', '', title) + '.txt'


def titleToFileAdressByID(title,id, pagesFolder):
    def is_ascii(s):
        return all(ord(c) < 128 for c in s)
    fileName = re.sub(r'\W', '', title)
    if not title[0].isalnum() or len(fileName) == 0:
        return pagesFolder +  r"/other/" + id + '.txt'
    return pagesFolder+'/' + fileName[0].lower() + r"/" + id + '.txt'


def getIdByTitle(title):
    url = "https://en.wikipedia.org/w/api.php?action=query&titles=" + title + '&format=json'
    response = urllib2.urlopen(url)
    myJson = response.read()
    a = json.loads(myJson)
    return a['query']['pages'].keys()[0]


print getIdByTitle('cat')
