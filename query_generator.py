
# coding: utf-8

# In[76]:

import re
import ast

text = ''' "henry duncan" may refer to: 
*[[henry duncan (royal navy officer, born 1735)]] 
(1735–1814), naval captain and deputy comptroller of 
the royal navy *sir [[henry duncan (royal navy officer, 
born 1786)]] (1786–1835), scottish sailor *[[henry duncan 
(minister)]] (1774–1846), scottish minister, geologist and
social reformer; founder of the savings bank movement  ==see
also== * {{intitle}} * [[james henry duncan (disambiguation)]]
{{hndis|duncan, henry}}'''

test_queries = [
    '"cat" [4,5] "hat"',
    '"henry"',
    '"henry" [0,1] "duncan"',
    '"royal" [4,6] "officer"',
    '"royal" [4,7] "officer" [4,8] "1735"'
]

def buildRegex(query):
    elements = query.split()
    strings = [string.replace('"', '') for string in elements[::2]]
    wild_cards = [ast.literal_eval(element) for element in elements[1::2]]
    regex_string = r''
    for index, string in enumerate(strings):
        regex_string += re.escape(string)
        if (index < (len(strings) - 1)):
            min_char, max_char = wild_cards[index]
            unknown = '.{' + str(min_char) + ',' + str(max_char) + '}' 
            regex_string += unknown
    return regex_string
      
def findQuery(query):
    regex = buildRegex(query)
    matchObj = re.findall(regex, text)
    if (matchObj):
        return matchObj

for query in test_queries:
    print 'Query:', query
    result = findQuery(query)
    if (result): 
        print 'Result count:', len(result), result


# In[53]:

matchObj.groupdict()


# In[ ]:



