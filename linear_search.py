# Got slate magazine data from http://www.anc.org/data/oanc/contents/
# rm'd .xml, .anc files, leaving just .txt
# 4534 files in like 55 subdirs

from words import get_text, words

def linear_search(files, terms):
    """
    Given a list of fully-qualified filenames, return a list of them
    whose file contents has all words in terms as normalized by your words() function.
    Parameter terms is a list of strings.
    Perform a linear search, looking at each file one after the other.
    """
    listOfFiles = []

    for file in files:
        # convert to list of words
        allWordsInFile = words(get_text(file))

        # check to see if the search terms are subsets of the file words
        if set(terms).issubset(allWordsInFile):
            listOfFiles.append(file)

    return(listOfFiles)


