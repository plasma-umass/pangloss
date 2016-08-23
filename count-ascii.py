import sys

if len(sys.argv) < 2:
    print "Invoke with a number as an argument (this is the classification of the input stream)."
    sys.exit(1)
    
counts = {}

total = 0
with open('/dev/stdin', 'r') as f:
    for line in f:
        for ch in line:
            counts[ord(ch)] = counts.get(ord(ch), 0) + 1
            total = total + 1

# Add smoothing for cases where there is a zero entry.
# See https://en.wikipedia.org/wiki/Additive_smoothing
for i in xrange(0,256):
    print str(counts.get(i,1) / float(total + 1)) + ",",
    #    print str(counts.get(i,0)) + ",",

print sys.argv[1]

    #    print str(i) + " : " + str(counts.get(i, 0))
            
    
