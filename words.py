import os
import re
import string

# set up jinja
from jinja2 import Environment


def filelist(root):
    """Return a fully-qualified list of filenames under root directory"""
    allFiles = []
    for dirName, subdirList, fileList in os.walk(root):
        #print('Found directory: %s' % dirName)
        for fname in fileList:
            allFiles.append(os.path.realpath(dirName) + "/" + fname)
            #print(os.path.realpath(dirName) + "/" + fname)
    #print(len(allFiles))
    return allFiles
    """
    itemsInRoot = os.listdir(root)
    for item in itemsInRoot:
        if os.path.isdir(item):
            
    relativePath = os.path.realpath(root)
    fileList = []
    for file in allFileNames:
        fileList.append(relativePath + "/" + file)
    return fileList
    """


def get_text(fileName):
    f = open(fileName)
    s = f.read()
    f.close()
    return s

def words(text):
    """
    Given a string, return a list of words normalized as follows.
    Split the string to make words first by using regex compile() function
    and string.punctuation + '0-9\\r\\t\\n]' to replace all those
    char with a space character.
    Split on space to get word list.
    Ignore words < 3 char long.
    Lowercase all words
    """
    regex = re.compile('[' + re.escape(string.punctuation) + '0-9\\r\\t\\n]')
    nopunct = regex.sub(" ", text)  # delete stuff but leave at least a space to avoid clumping together
    words = nopunct.split(" ")
    words = [w for w in words if len(w) > 2]  # ignore a, an, to, at, be, ...
    words = [w.lower() for w in words]
    return words


def getTwoSentences(fileName, terms):
    chosenWord = terms[0]
    twoSentences = []
    with open(fileName) as f:
        line = f.readline()
        count = 1 # DEBUGGING <<<<<<<<<
        while line: # while there is a next line
            if chosenWord in words(line):
                twoSentences.append(line)
                twoSentences.append(f.readline())
                return("".join(twoSentences))
            else:
                line = f.readline()
            count = count + 1 # DEBUGGING <<<<<<<<<
            #line = f.readline()  # DEBUGGING <<<<<<<<<

def results(docs, terms):
    """
    Given a list of fully-qualifed filenames, return an HTML file
    that displays the results and up to 2 lines from the file
    that have at least one of the search terms.
    Return at most 100 results.  Arg terms is a list of string terms.
    """
    HTML = """
    <html>
    <body>
    <h2>Search results for <b>{% for term in searchTerms%}{{term}} {% endfor %}</b> in {{numFiles}} files</h2>
    
    {% for file in matchedFiles %}
    <p><a href="file:///{{file}}">{{file}}</a><br>  
    {{descriptions[loop.index0]}}<br><br>
    {% endfor %}
    </body>
    </html>
    """
    # get the sentences for each doc
    sentences = []
    try:
        for doc in docs:
            sentences.append(getTwoSentences(doc, terms))
    except:
        return(""""<html>
    <body>
    <h2>Search results for <b>NONE</b> in 0 files</h2>
    </body>
    </html>""")

    stringOutput = Environment().from_string(HTML).render(searchTerms = terms, numFiles=len(docs), matchedFiles = docs, descriptions=sentences)
    return(stringOutput)

def filenames(docs):
    """Return just the filenames from list of fully-qualified filenames"""
    if docs is None:
        return []
    return [os.path.basename(d) for d in docs]
