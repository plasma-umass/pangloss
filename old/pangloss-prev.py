import sys
import csv
import math

if len(sys.argv) < 3:
    classifierFn = "classifiers.csv"
    clazzesFn    = "classes.csv"
else:
    classifierFn = sys.argv[1]
    clazzesFn = sys.argv[2]

classifiers = []
classifications = []
classes = {}
prior = {}

with open(classifierFn, 'rb') as csvfile:
    reader = csv.reader(csvfile)
    for row in reader:
        clazz = int(row.pop()) # class is last entry
        classifications.append(clazz)
        classifiers.append(row)

priortotal = 0
with open(clazzesFn, 'rb') as csvfile:
    reader = csv.reader(csvfile)
    i = 0
    for row in reader:
        classes[int(row[0])] = row[1]
        prior[i] = float(row[2])
        priortotal = priortotal + prior[i]
        i = i + 1

for key in prior:
    prior[key] = prior[key] / priortotal

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
ascii = list(xrange(32,128))
ascii.insert(0, 9)
for i in xrange(0,len(classifiers)):
    val = 0
    
    for j in ascii:
        c = classifiers[i][j]
        val = val + counts[j] * math.log(c)
    val = val + math.log(prior[i])
    
    print str(val) + " : " + classes[classifications[i]]
    if val > max:
        max = val
        argmax = classifications[i]

print classes[argmax]

