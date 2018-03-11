#!/usr/bin/env python

import os
import glob
import pprint

targets = ["C++", "JavaScript", "Java", "C", "Ruby", "Perl", "TypeScript", "Python", "Scala", "PHP", "Objective-C"]
fnames = ["cpluspluscounts.py", "javascriptcounts.py", "javacounts.py", "ccounts.py",
          "rubycounts.py", "perlcounts.py", "typescriptcounts.py", "pythoncounts.py",
        "scalacounts.py", "phpcounts.py", "objectiveccounts.py" ]

extensions = [".cpp",
              ".js",
              ".java",
              ".c",
              ".rb",
              ".pm",
              ".ts",
              ".py",
              ".scala",
              ".php",
              ".m"]

oldextensions = [[".cpp", ".hpp", ".hh", ".cc", ".cxx", ".hxx", ".C"],
              [".js"],
              [".java"],
              [".c",".h"],
              [".rb"],
              [".pl",".pm"],
              [".ts"],
              [".py"],
              [".scala"],
              [".php"],
              [".m"]]

words = {}
overall = {}
maxcount = 500
totalfiles = 0

with open('words.txt', 'r') as w:
    for line in w:
        for word in line.split():
            words[word] = True

if False:
    print "features = ",
    wlist = []
    for w in words:
        wlist.append(w)
    print wlist
    print "targets = " + str(targets)

for index in range(0, len(targets)):
    x = []
    y = []
    name = targets[index]
    print name
    ext = extensions[index]
    counter = 0

    for dirpath, dirs, files in os.walk(name):
        if counter > maxcount:
            break
        for f in files:
            if counter > maxcount:
                break
            fname = os.path.join(dirpath, f)
            if ext in f:
                # fullname = root + "/" + dir + "/" + fname

                with open(fname, 'r') as f:
                    counter += 1
                    if counter > maxcount:
                        break
                    count = {}
                    total = 0
                    for line in f:
                        for word in line.split():
                            # print word,"-",
                            if word in words:
                                total += 1
                                count[word] = count.get(word, 0) + 1
                                overall[word] = overall.get(word, 0) + 1
                    totalfiles += 1
                    l = []
                    ind = 0
                    for w in words:
                        if w in count:
                            l.append(count[w] / (1.0 * total))
                            # l.append((ind, count[w] / (1.0 * total)))
                        else:
                            l.append(0.0)
                        ind += 1
                    x.append(l)
                    y.append(index)
                    

    with open(fnames[index], 'w') as f:
        print "writing "+fnames[index]
        f.write("from config import x,y\n")
        f.write("x += ")
        pprint.pprint(x, stream=f)
        f.write("\n")
        f.write("y += ")
        pprint.pprint(y, stream=f)
        f.write("\n")

if True:
    with open('usedwords.txt', 'w') as f:
            for w in overall:
                if overall[w] / (1.0 * totalfiles) > 0.75 * (1.0 / len(targets)):
                    f.write(w+"\n")
                    # f.write(w + "," + str(overall[w])+"\n")
        
