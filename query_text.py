import re
import ast
import sys
import timeit

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

def findQuery(query, text):
    regex = buildRegex(query)
    print 'Regex:', regex
    matchObj = re.findall(regex, text)
    if (matchObj):
        return matchObj

_, text_file, query = sys.argv

with open(text_file, 'r') as infile:
    text = infile.read().replace('\n', '')

print "Looking for", query, "'in ", text_file
print text

t1 = timeit.timeit()
result = findQuery(query, text)
t2 = timeit.timeit()

print 'Found', len(result), 'results in ', t2 - t1 , 'ms'
print 'The found occorences were'
for item in result:
    print item
