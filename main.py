import query_text
import time
import CONSTANTS
import os, re

if __name__ == "__main__":
    queryExecuter = query_text.QueryExecuter()
    search_letters = 'a'
    path_to_validation_queries = 'validation_queries'
    test_data = {
            'own_test': {
                    'query': '"wikipedia" [0,10] "links" [0,1000] "the"'
                }
        }
    for file_name in os.listdir(path_to_validation_queries):
        # transform file-names to query format
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
    for file_name in test_data:
        start = time.clock()
        # to run in pages startung with 'a'
        # result = queryExecuter.runQueryRaw(test_data[file_name]['query'], 'pages_new', 'a')
        # to run only on the page 'Abderus.txt'
        # result = queryExecuter.runQueryRaw(test_data[file_name]['query'], 'pages_new', 'a/Abderus.txt')
        # run on all pages in the pages_new directory and it's subdirectories
        result = queryExecuter.runQueryRaw(test_data[file_name]['query'], 'pages_new')

        end = time.clock()
        if result:
            print 'we found', len(result), 'results for:', test_data[file_name]['query']
            for string in result:
                print '  --  result:', string
        else:
            print '++++++++++++  we found 0 results for',test_data[file_name]['query'], '++++++++++++++'
        print 'Running time :', (end - start), '\n----------------------------------------------------------------\n'
        test_data[file_name]['results'] = {
            'time': end - start,
            'results': result
        }
    print '\nSUMMARY'
    for file_name in test_data:
        data = test_data[file_name]
        print data['query'], '\t', len(data['results']['results']), 'results\t', data['results']['time'], 'seconds'
