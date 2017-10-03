import query_text
import time
import CONSTANTS

if __name__ == "__main__":

    start = time.clock()
    queryExecuter = query_text.QueryExecuter()
    query ='"turkey" [1,10] "if"'
    # print queryExecuter.findQueryFromLettersGiven(query, CONSTANTS.capitals.lower())
    for i in range(5):
        print queryExecuter.findQueryFromLettersGiven(query, CONSTANTS.capitals.lower())
        print queryExecuter.findQueryFromJsonFileUsingIndex(query)
    print 'Running time :', time.clock() - start








