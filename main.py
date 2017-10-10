
import  CONSTANTS
import query_text
import utils


def showOutput(result):
    print "OUTPUT: we have ", len(result)
    for i in result:
        print i

    # We did not write escapes so please be carefull entering right input
if __name__ == "__main__":
    pageFolder = CONSTANTS.miniPagesFolder
    letters = CONSTANTS.letters
    indexFolder = CONSTANTS.miniIndexFolder
    queryExecuter = query_text.QueryExecuter(pagesFolder=pageFolder,useJSON=CONSTANTS.useJSONinMain, indexFolder=indexFolder)

    while True:
        queryType = raw_input("Please enter the type of the query brute force / word indexex (b/w)")
        if queryType not in ['b','w']:
            print "Try Again"
            continue
        queryRange = raw_input("Are you going to run it on whole databese / a letter / or a page (w/l/p)")
        if queryRange not in ['w','l','p']:
            print "Try Again"
            continue
        if queryRange == 'l':
            queryLetters = raw_input("Which letters? (you can enter multiple like abc")
        elif queryRange == 'p':
            queryLetters = raw_input("Title?").lower()

        query = raw_input('enter the query')
##
        if queryType == 'w':
            if queryRange == 'p':
                r = utils.getIdByTitle(queryLetters) + '.txt'
                indexedResult = queryExecuter.findQueryFromFile(query, [r])
                showOutput(indexedResult)
            if queryRange == 'w':
                indexedResult = queryExecuter.word_index_findQueryFromLettersGiven(query, letters)
                showOutput(indexedResult)
            if queryRange == 'l':
                indexedResult = queryExecuter.word_index_findQueryFromLettersGiven(query, queryLetters)
                showOutput(indexedResult)
        if queryType == 'b':
            if queryRange == 'w':
                raw_result = queryExecuter.runQueryRaw(query)
                showOutput(raw_result)
            if queryRange == 'l':
                raw_result = []
                for i in queryLetters:
                    raw_result.append(queryExecuter.runQueryRaw(query,i))
                showOutput(raw_result)
            if queryRange == 'p':
                r = utils.getIdByTitle(queryLetters) + '.txt'
                raw_result = queryExecuter.runQueryRaw(query, r)
                showOutput(raw_result)


