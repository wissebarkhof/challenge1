import query_text
import time


if __name__ == "__main__":

    start = time.clock()
    queryExecuter = query_text.QueryExecuter()
    query ='"as" [2,4] "of"'
    print queryExecuter.findQueryFromFileUsingIndex(query,"as","of",'abcdefghijklmnopqrstuvwxyz')
    print 'Running time :', time.clock() - start








