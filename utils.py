import re

def titleToFileAdress(title, pagesFolder):
    fileName = re.sub(r'\W', '', title)
    if  not title[0].isalnum() or len(fileName) == 0:
        fileName = unicode(title).encode('cp1252')
        return pagesFolder +  r"other/" + re.sub(r'\W', '', title) + '.txt'
    return pagesFolder + fileName[0].lower() + r"/" + re.sub(r'\W', '', title) + '.txt'
