import re
import unicodedata

def titleToFileAdress(title, pagesFolder):

    def is_ascii(s):
        return all(ord(c) < 128 for c in s)



    fileName = re.sub(r'\W', '', title)
    if not title[0].isalnum() or len(fileName) == 0:
        fileName = ''.join( c if is_ascii(c) and c.isalnum() else str(ord(c)) for c in title)
        return pagesFolder +  r"other/" + fileName + '.txt'
    return pagesFolder + fileName[0].lower() + r"/" + re.sub(r'\W', '', title) + '.txt'
