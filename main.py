import query_text
import time
import CONSTANTS
import os, re


runs = {
    'c/Cat.txt': {
        'test': [{
            'query': '"cat" [0,10] "are" [0,10] "to"',
            'result': 10,
        },{
            'query': '"cat" [0,100] "anatomy"',
            'result': 11,
        }, {
            'query': '"china" [30,150] "washington"',
            'result': 1,
        }, {
            'query': '"english" [0,200] "cat"',
            'result': 37,
        }, {
            'query': '"kitten" [15,85] "cat" [0,100] "sire" [0,200] "oxford"',
            'result': 2,
        }],
    },
    # 'a': {
    #     'test':[{
    #         'query': '"arnold" [0,10] "schwarzenegger" [0,10] "is"',
    #         'result': 14,
    #     }, {
    #         'query': '"apache" [0,100] "software"',
    #         'result': 1517,
    #     }, {
    #         'query': '"aarhus" [30,150] "denmark"',
    #         'result': 555,
    #     },  {
    #         'query': '"english" [0,100] "alphabet"',
    #         'result': 181,
    #     }, {
    #         'query': '"first" [0,85] "letter" [0,100] "alphabet" [0,200] "consonant"',
    #         'result': 3,
    #     }]
    # },
}

# ['first', (0, 85), 'letter', (0, 100), 'alphabet', (0, 200), 'consonant']


def getValidationData(path_to_validation_queries):
    test_data = {}
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
    return test_data



if __name__ == "__main__":
    queryExecuter = query_text.QueryExecuter()
    for run in runs:
        for test in runs[run]['test']:
            start = time.clock()
            raw_result = queryExecuter.runQueryRaw(test['query'], 'pages_new_all', run)
            end = time.clock()
            if raw_result:
                print 'we found', len(raw_result), 'results for:', test['query']
                for string in raw_result:
                    print '  --  result:', string
            else:
                print '++++++++++++  we found 0 results for', test['query'], '++++++++++++++'
            print 'Running time :', (end - start), '\n----------------------------------------------------------------\n'
            test['raw_outcome'] = {
                'time': end - start,
                'results': raw_result,
                'accuracy': round(float(len(raw_result)) / test['result'], 4)

            }
            # start = time.clock()
            # # put here the code you wrote
            # indexed_result = queryExecuter.???
            # end = time.clock()
            # if indexed_result:
            #     print 'we found', len(indexed_result), 'results for:', test['query']
            #     for string in indexed_result:
            #         print '  --  result:', string
            # else:
            #     print '++++++++++++  we found 0 results for', test['query'], '++++++++++++++'
            # print 'Running time :', (end - start), '\n----------------------------------------------------------------\n'
            # test['indexed_outcome'] = {
            #     'time': end - start,
            #     'results': indexed_result,
            #     'accuracy': round(float(len(indexed_result)) / test['result'], 4)
            #
            # }
    print '\nSUMMARY'
    for run in runs:
        for test in runs[run]['test']:
            data = test['raw_outcome']
            print test['query'], len(data['results']), 'res\t', data['time'], 's\t', data['accuracy'], 'acc\t'
            # data = test['indexed_outcome']
            # print test['query'], len(data['results']), 'res\t', data['time'], 's\t', data['accuracy'], 'acc\t'
