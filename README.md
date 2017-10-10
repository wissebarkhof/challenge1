# challenge1

you'll need to have NLTK installed

to install:
 * sudo pip install -U nltk
 * python (in terminal)
 * \>\>\> import nltk
 * \>\>\> nltk.dowload()
 * a window should pop up
 * download the 'popular' category


to use and install with mongoDB:%Note that you should be able to run withoud mongodb only with pymongo

* install mongoDB % A bit complex so skipped here
* sudo pip install pymongo


 --- HOW to run a small demo?

1)  First go to the CONSTANTS.py file and change `bigFileAddress` to the address of the wikipedia xml file
2)  Run extractText.py this will create a folder on the a folder. You can change this folder by editing CONSTANTS miniPagesFolder = "../miniPages"
3)  Run buildIndexForAllPages.py This creates an index folder. You can change this folder by editing CONSTANTS miniIndexFolder
4)  Run main.py

 Here you will be asked to run your query you can
 This will run query using word indexing method
 Note that since we are running only in a small dataset results do not cover all wiki
 Also if you try to work on a specific page

Examples

in main try /w/p/anarchism "anarchy" [1,50] "go"
            /w/w/ "anarchy" [1,50] "go"
            /w/l/ a "anarchy" [1,50] "go"
            /b/w/ "anarchy" [1,50] "go"
            /b/l/ a "anarchy" [1,50] "go"
