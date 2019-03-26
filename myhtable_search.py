# Got slate magazine data from http://www.anc.org/data/oanc/contents/
# rm'd .xml, .anc files, leaving just .txt
# 4534 files in like 55 subdirs

from htable import *
from words import get_text

import pprint

def myhtable_create_index(files):
    """
    Build an index from word to set of document indexes
    This does the exact same thing as create_index() except that it uses
    your htable.  As a number of htable buckets, use 4011.
    Returns a list-of-buckets hashtable representation.
    """
    d = htable(4011) # initialize empty htable
    # k = 0
    for k, file in enumerate(files):  # loop through files
        # k = k + 1
        wordsInDoc = words(get_text(file))
        # print("len doc {:<4d}: {:<6d}".format(k, len(wordsInDoc)))
        for word in wordsInDoc:  # loop through words in that file
            htable_put(d, word, {files[k]})
            # print("word {:d} ({:<14s}), doc {:d}".format(i+1, word, k)) # warning: x6 runtime!
    #pp = pprint.PrettyPrinter(indent=4)
    #pp.pprint(d)
    return d


def myhtable_index_search(files, index, terms):
    """
    This does the exact same thing as index_search() except that it uses your htable.
    I.e., use htable_get(index, w) not index[w].
    """
    try:
        docs = [htable_get(index, k) for k in terms]  # returns all files containing search terms
        commonDocs = set.intersection(*docs)  # return interesction of docs
    except:
        return None


    #print("============ Common Docs:")
    #pp = pprint.PrettyPrinter(indent=4)
    #pp.pprint(commonDocs)
    return commonDocs

