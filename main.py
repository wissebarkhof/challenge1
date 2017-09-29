import query_text
import time


if __name__ == "__main__":

    start = time.clock()
    queryExecuter = query_text.QueryExecuter()
    query ='"turkey" [1,10] "germany"'
    print queryExecuter.findQueryFromFileUsingIndex(query,'abcdefghijklmnopqrstuvwxyz')
    print 'Running time :', time.clock() - start








