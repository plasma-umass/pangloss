#!/usr/bin/env python

import sys
import operator
import os

from itertools import tee, islice
import collections

# Break a file into words.
def oldwords(fileobj):
    for line in fileobj:
        for word in line.split():
            yield word


def ngrams(lst, n):
  tlst = lst
  while True:
    a, b = tee(tlst)
    l = tuple(islice(a, n))
    if len(l) == n:
      yield l
      next(b)
      tlst = b
    else:
      break
  
def wordsn(fileobj,n,skip=0):
    frequencies = collections.Counter([])
    words = fileobj.read().split()
#    print words
#    print words[::skip+1]
    words = words + words[::skip+1]
#    words += words[::skip+1]
    return ngrams(words, n)


# Break into conjoined bigrams.
def words(fileobj):
    wprev = None
    for line in fileobj:
        for w in line.split():
            if wprev is not None:
                yield wprev+":"+w
            else:
                yield w
            wprev = w

# Only record the top N
threshold = 200

counts = {}

total = 0
with open('/dev/stdin', 'r') as f:
    wordgen = wordsn(f,2,2)
    for word in wordgen:
        if True: # len(word) <= 8:
            counts[word] = counts.get(word, 0) + 1
            total += 1

ignore = [] # ["the", "and", "be", "are", "is", "an", "a", "it", "we", "The", "from", "will", "can", "that", "to", "by"]

print "{",
totalSoFar = 0
printedSoFar = 0

for word in sorted(counts, key=counts.get, reverse=True):
    totalSoFar = totalSoFar + 1 # counts[word]
    if totalSoFar <= threshold:
        if word not in ignore:
            if printedSoFar > 0:
                print ", ",
            print repr(word) + ' : ' + str(counts[word]),
            printedSoFar = printedSoFar + 1
        
print "}"
    
