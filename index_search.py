from collections import defaultdict  # https://docs.python.org/2/library/collections.html

from words import get_text, words
import pprint

def toUnique(myList):
    return list(set(myList))

def create_index(files):
    d = {}
    for k, file in enumerate(files): # loop through files
        wordsInDoc = words(get_text(file))
        for word in wordsInDoc: # loop through words in that file
            if word not in d:
                d[word] = {files[k]}
            else:
                d[word].add(files[k])
            # print("word {:d} ({:<14s}), doc {:d}".format(i+1, word, k)) # warning: x6 runtime!
    return d

def create_index_old(files):
    """
    Given a list of fully-qualified filenames, build an index from word
    to set of document IDs. A document ID is just the index into the
    files parameter (indexed from 0) to get the file name. Make sure that
    you are mapping a word to a set of doc IDs, not a list.
    For each word w in file i, add i to the set of document IDs containing w
    Return a dict object mapping a word to a set of doc IDs.
    """
    # create massive list of all words from ALL FILES
    allWords = []
    for file in files:
        allWords.append(get_text(file)) # extract file contents as massive strings

    wordsInAllDocuments = [toUnique(words(f)) for f in allWords] # convert to words per document (used later)
    allWords = words(" ".join(allWords)) # convert strings into list of words
    allWords = toUnique(allWords) # make it unique (i.e. no duplicate words)

    # iterate through words and generate index

    dictionary = {w: set() for w in allWords}

    for word in allWords: # loop through all unique words
        for i, wordsInOneDocument in enumerate(wordsInAllDocuments): # loops through all files
            if word in wordsInOneDocument:
                dictionary[word].add(i + 1)
    return dictionary

def index_search(files, index, terms):
    """
    Given an index and a list of fully-qualified filenames, return a list of
    filenames whose file contents has all words in terms parameter as normalized
    by your words() function.  Parameter terms is a list of strings.
    You can only use the index to find matching files; you cannot open the files
    and look inside.
    """
    try:
        docs = [index[k] for k in terms] # returns all files containing search terms
    except:
        return None

    commonDocs = set.intersection(*docs) # return interesction of docs
    """
    pp = pprint.PrettyPrinter(indent=4)
    pp.pprint(docs)
    print("============ Common Docs:")
    pp.pprint(commonDocs)
    """
    return commonDocs

