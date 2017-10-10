import query_text
import time
import CONSTANTS
import os, re
import utils

runs = {
    # 'c/cat.txt': {
    #     'test': [{
    #         'query': '"cat" [0,10] "are" [0,10] "to"',
    #         'result': 10,
    #     },{
    #         'query': '"cat" [0,100] "anatomy"',
    #         'result': 11,
    #     }, {
    #         'query': '"china" [30,150] "washington"',
    #         'result': 1,
    #     }, {
    #         'query': '"english" [0,200] "cat"',
    #         'result': 37,
    #     }, {
    #         'query': '"kitten" [15,85] "cat" [0,100] "sire" [0,200] "oxford"',
    #         'result': 2,
    #     }],
    # },
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
    '/': {
        'test': [{
            'query': '"elephants" [0,20] "are" [0,20] "to"',
            'result': 181,
        },{
            'query': '"technical" [0,20] "university" [0,20] "denmark"',
            'result': 611,
        }, {
            'query': '"testing" [0,20] "with" [0,20] "a" [0,30] "lot" [0,4] "of [0,5] "words"',
            'result': 0,
        }, {
            'query': '"stress" [0,250] "test"',
            'result': 7355,
        },{
            'query': '"object" [10,200] "application" [0,100] "python" [10,200] "system" [0,100] "computer" [0,10] "science" [0,150] "linux" [0,200] "ruby"',
            'result': 1,
        },]
    }
}


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

    pageFolder = CONSTANTS.toyPagesFolder
    letters = CONSTANTS.letters
    queryExecuter = query_text.QueryExecuter(pagesFolder=pageFolder)

    for run in runs:
        for test in runs[run]['test']:
            # if '.txt' in run:
            #     run = run[0:2]+ utils.getIdByTitle(run[2:-4])+'.txt'#only the part without txt
            if run == '/':
                run =None
            start = time.clock()
            raw_result = queryExecuter.runQueryRaw(test['query'],  run)
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
                'accuracy': round(float(len(raw_result)) / test['result'], 4) if test['result'] > 0 else 1
            }
#
#
#
# print "-------------------------------------------------------------------"
#
# print "-------------------------------------------------------------------"
#
# print "-------------------------------------------------------------------"
#
# for run in runs:
#     for test in runs[run]['test']:
#         if '.txt' in run:
#             run = run[0:2] + utils.getIdByTitle(run[2:-4]) + '.txt'
#             start = time.clock()
#             indexedResult = queryExecuter.findQueryFromFile(test['query'],[run])
#             end = time.clock()
#         elif run == '/':
#             start = time.clock()
#             indexedResult = queryExecuter.word_index_findQueryFromLettersGiven(test['query'], letters)
#             end = time.clock()
#         elif len(run) == 1:
#             start = time.clock()
#             indexedResult = queryExecuter.word_index_findQueryFromLettersGiven(test['query'], run)
#             end = time.clock()
#
#         if raw_result:
#             print 'we found', len(indexedResult), 'results for:', test['query']
#             for string in indexedResult:
#                 print '  --  result:', string
#         else:
#             print '++++++++++++  we found 0 results for', test['query'], '++++++++++++++'
#         print 'Running time :', (end - start), '\n----------------------------------------------------------------\n'
#         test['indexed_outcome'] = {
#             'time': end - start,
#             'results': raw_result,
#             'accuracy': round(float(len(raw_result)) / test['result'], 4) if test['result'] > 0 else 1
#
#         }
# print '\nSUMMARY'
# raw_output_file = open('raw_query_results.txt', 'w')
# indexed_output_file = open('indexed_query_results.txt', 'w')
#
# # for run in runs:
# #     print 'summarying', run
# #     for test in runs[run]['test']:
# #         data = test['indexed_outcome']
# #         summary = '\n' + run + '\t' + test['query'] + '\t' + str(len(data['results'])) + ' res\t' + str(data['time']) + 's\t' + str(data['accuracy']) + ' acc\n'
# #         print summary
# #         indexed_output_file.write(summary)
# #         for result in data['results']:
# #             indexed_output_file.write(result + '\n')
#
# for run in runs:
#     print 'summarying', run
#     for test in runs[run]['test']:
#         data = test['raw_outcome']
#         summary = '\n' + run + '\t' + test['query'] + '\t' + str(len(data['results'])) + ' res\t' + str(data['time']) + 's\t' + str(data['accuracy']) + ' acc\n'
#         print summary
#         raw_output_file.write(summary)
#         for result in data['results']:
#             raw_output_file.write(result + '\n')
#
#
#
#
# raw_output_file.close()
# indexed_output_file.close()