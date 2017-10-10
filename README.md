# challenge1

you'll need to have NLTK installed

to install:
 * sudo pip install -U nltk
 * python (in terminal)
 * \>\>\> import nltk
 * \>\>\> nltk.dowload()
 * a window should pop up
 * download the 'popular' category


 --- HOW to run a small demo?

1)  First go to the CONSTANTS.py file and change `bigFileAddress` to the address of the wikipedia xml file
2)  Run extractText.py this will create a folder on the a folder. You can change this folder by editing CONSTANTS miniPagesFolder = "../miniPages"
3)  Run buildIndexForAllPages.py This creates an index folder. You can change this folder by editing CONSTANTS miniIndexFolder
4)  Run main.py

 Here you will be asked to run your query you can for example try w/w/ "cats" [1,10] "dogs"
 This will run query using word indexing method
 Note that since we are running only in a small dataset results do not cover all wiki
 Also if you try to work on a specific page

