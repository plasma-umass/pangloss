import sys
import csv
import math

if len(sys.argv) < 3:
    print "Invoke glosser with a csv file as the classifications, and a second with class names."
    sys.exit(1)

classifiers = []
classifications = []
classes = {}

with open(sys.argv[1], 'rb') as csvfile:
    reader = csv.reader(csvfile)
    for row in reader:
        clazz = int(row.pop()) # class is last entry
        classifications.append(clazz)
        classifiers.append(row)

with open(sys.argv[2], 'rb') as csvfile:
    reader = csv.reader(csvfile)
    for row in reader:
        classes[int(row[0])] = row[1]

classifiers = [map(float, row) for row in classifiers] 

counts = {}

total = 0
with open('/dev/stdin', 'r') as f:
    for line in f:
        for ch in line:
            counts[ord(ch)] = counts.get(ord(ch), 0) + 1
            total = total + 1

for i in xrange(0,256):
    counts[i] = counts.get(i, 0)

# Naive Bayes
# Bayes:
#  P(hypothesis_k true | evidence) = P(hypothesis_k true) * P(evidence | hypothesis_k true) / P(evidence)
#           posterior = prior * likelihood / evidence
# Naive Bayes:
#      ignore evidence as it is the same for all
#      => posterior ~ prior * likelihood
#
#      prior = #(hypothesis_k) / #(all hypotheses)
#      likelihood = P(evidence | hypothesis_k true)
#
#      assume independence of outcomes
#      now we just multiply prior * likelihood and find the argmax for k

# for multinomials:
#   argmax_k log prior + sum_i (evidence_i * log Pr(hypothesis_k[i]))

argmax = classifications[0]
max = float('-inf')
for i in xrange(0,len(classifiers)):
    val = 0
    for j in xrange(0,256):
        if (classifiers[i][j] != 0.0):
            val = val + counts[j] * math.log(classifiers[i][j])
    if val > max:
        max = val
        argmax = classifications[i]

print classes[argmax]

