from words import *
from jinja2 import Environment

"""
A hashtable represented as a list of lists with open hashing.
Each bucket is a list of (key,value) tuples
"""

def htable(nbuckets):
    """Return a list of nbuckets lists"""
    return([[] for _ in range(nbuckets)]) # return nbuckets empty lists (i.e. buckets)

def hashcode(o):
    """
    Return a hashcode for strings and integers; all others return None
    For integers, just return the integer value.
    For strings, perform operation h = h*31 + ord(c) for all characters in the string
    """
    if isinstance(o, str): # str
        h = 0
        for c in o:
            h = (h * 31) + ord(c)
        return (h)
    elif isinstance(o, int):
        return(o)
    else:  # neither string nor int
        return None


def bucket_indexof(targetBucket, key):
    """
    You don't have to implement this, but I found it to be a handy function.
    Return the index of the element within a specific bucket; the bucket is:
    table[hashcode(key) % len(table)]. You have to linearly
    search the bucket to find the tuple containing key.
    """
    return([tup[0] for tup in targetBucket].index(key))

def htable_put(table, key, value):
    """
    Perform the equivalent of table[key] = value
    Find the appropriate bucket indicated by key and then append (key,value)
    to that bucket if the (key,value) pair doesn't exist yet in that bucket.
    If the bucket for key already has a (key,value) pair with that key,
    then replace the tuple with the new (key,value).
    Make sure that you are only adding (key,value) associations to the buckets.
    The type(value) can be anything. Could be a set, list, number, string, anything!
    """
    bucketIndex = hashcode(key) % len(table)
    targetBucket = table[bucketIndex]
    if any(key in tup for tup in targetBucket): # check existence
        #print(targetBucket[bucket_indexof(targetBucket,key)][1])
        newSet = targetBucket[bucket_indexof(targetBucket,key)][1] # retrieve value
        if(type(value) is str):
            targetBucket[bucket_indexof(targetBucket,key)] = (key, value) # for strings, just replace instead of update
        else:
            newSet.update(value) # update set
            targetBucket[bucket_indexof(targetBucket,key)] = (key, newSet) # replace tuple
    else:
        targetBucket.append((key, value))


def htable_get(table, key):
    """
    Return the equivalent of table[key].
    Find the appropriate bucket indicated by the key and look for the
    association with the key. Return the value (not the key and not
    the association!). Return None if key not found.
    """
    bucketIndex = hashcode(key) % len(table)
    targetBucket = table[bucketIndex]
    if any(key in tup for tup in targetBucket): # check existence
        return targetBucket[bucket_indexof(targetBucket,key)][1]
    else:
        return None

################## STRING STUFF ######################

def htable_buckets_str(table):
    OUTPUT="""{%for bucket in table%}{{'%04d'%(loop.index-1)}}->{% for tup in bucket %}{{tup[0]}}:{{tup[1]}}{% if loop.last == false %}, {% endif %}{% endfor %}
{% endfor %}"""
    stringOutput = Environment().from_string(OUTPUT).render(table=table)
    return(stringOutput)

def htable_str(table):
    nonempty = [b for b in table if b]
    if len(nonempty) == 0:
        return("{}")
    elif nonempty:
        valType = type(nonempty[0][0][1])
        if valType is set:
            OUTPUT="""{% raw %}{{% endraw%}{% for bucket in table %}{% for elem in bucket %}{{ elem[0] }}:{{ elem[1] }}{% endfor %}{% endfor %}{% raw %}}{% endraw%}"""
        else:
            OUTPUT = """{% raw %}{{% endraw%}{% for bucket in table %}{% for elem in bucket %}{{ elem[0] }}:{{ elem[1] }}{% if loop.last == false %}, {% endif %}{% endfor %}{% if loop.last == false %}, {% endif %}{% endfor %}{% raw %}}{% endraw%}"""
    stringOutput = Environment().from_string(OUTPUT).render(table=nonempty)
    return(stringOutput)

"""
debugging
table = htable(5)
print(htable_buckets_str(table))
"""