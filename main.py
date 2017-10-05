import query_text
import time
import CONSTANTS
import os, re

if __name__ == "__main__":
    queryExecuter = query_text.QueryExecuter()
    path_to_validation_queries = 'validation_queries'
    test_data = {
            'own_test': {
                    'query': '"wikipedia" [0,10] "links" [0,1000] "the"'
                }
        }
    for file_name in os.listdir(path_to_validation_queries):
        query = file_name.split('.')[0]
        split = re.split(r'\[(.*?)\]', query)
        strings = ['"{0}"'.format(string) for string in split[::2]]
        wild_cards = ['[{0}]'.format(string) for string in split[1::2]]
        processed = ' '.join([j for i in zip(strings, wild_cards) for j in i] + [strings[-1]])
        output = [string.strip().split('\t') for string in open(path_to_validation_queries + '/' + file_name).readlines()]
        test_data[file_name] = {
            'query' : processed,
            'output': output
        }
    # print queryExecuter.findQueryFromLettersGiven(query, CONSTANTS.capitals.lower())
    for file_name in test_data:
        start = time.clock()
        result = queryExecuter.findQueryFromLettersGiven(test_data[file_name]['query'], CONSTANTS.capitals.lower())
        if result:
            print '------------- we found', len(result), 'results -------------------'
            for string in result:
                print 'result:', string
        print 'Running time :', (time.clock() - start), '\n\n'
