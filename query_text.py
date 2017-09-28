import re, ast, sys, time, os

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
    matchObj = re.findall(regex, text)
    if (matchObj):
        return matchObj

_, text_file, query = sys.argv


try:
    with open(text_file, 'r') as infile:
        text = infile.read().replace('\n', '')
except IOError:
    text = ''
    print 'Got a folder, merging', len(os.listdir(text_file)), 'files'
    for filename in os.listdir(text_file):
        with open(text_file + '/' + filename, 'r') as infile:
            text += infile.read().replace('\n', '') + '\n'


print "Looking for", query, "'in ", text_file

times = []
for i in range(100):
    t1 = time.clock()
    result = findQuery(query, text)
    t2 = time.clock()
    times.append(t2 - t1)

avg_time = sum(times) / len(times)
print 'in an average of', avg_time  , 's in 100 loops'

if result:
    print 'Found', len(result), 'results'
    print 'The found occorences were'
    # for item in result:
    #     print item
else:
    print 'No matches were found'
