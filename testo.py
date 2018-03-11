#!/usr/bin/env python

from sklearn import tree
import numpy as np

def get_code(tree, feature_names, target_names,
             spacer_base="    "):
    """Produce pseudo-code for decision tree.

    Args
    ----
    tree -- scikit-leant DescisionTree.
    feature_names -- list of feature names.
    target_names -- list of target (class) names.
    spacer_base -- used for spacing code (default: "    ").

    Notes
    -----
    based on http://stackoverflow.com/a/30104792.
    """
    left      = tree.tree_.children_left
    right     = tree.tree_.children_right
    threshold = tree.tree_.threshold
    features  = [feature_names[i] for i in tree.tree_.feature]
    value = tree.tree_.value

    def recurse(left, right, threshold, features, node, depth):
        spacer = spacer_base * depth
        if (threshold[node] != -2):
            print(spacer + "if ( '" + features[node] + "' <= " + \
                  str(threshold[node]) + " ) {")
            if left[node] != -1:
                    recurse(left, right, threshold, features,
                            left[node], depth+1)
            print(spacer + "}\n" + spacer +"else {")
            if right[node] != -1:
                    recurse(left, right, threshold, features,
                            right[node], depth+1)
            print(spacer + "}")
        else:
            target = value[node]
            for i, v in zip(np.nonzero(target)[1],
                            target[np.nonzero(target)]):
                target_name = target_names[i]
                target_count = int(v)
                print(spacer + "return " + str(target_name) + \
                      " ( " + str(target_count) + " examples )")

    recurse(left, right, threshold, features, 0, 0)
    
# class, struct, public
# C ,C++

words = {}

with open('words.txt', 'r') as w:
    for line in w:
        for word in line.split():
            words[word] = True

features = []
for w in words:
    features.append(w)

targets = ["C++", "JavaScript", "Java", "C", "Ruby", "Perl", "TypeScript", "Python", "Scala", "PHP", "Objective-C"]

import config

from cpluspluscounts import *
from javascriptcounts import *
from javacounts import *
from ccounts import *
from rubycounts import *
from perlcounts import *
from typescriptcounts import *
from scalacounts import *
from phpcounts import *
from objectiveccounts import *


#features = ["class", "struct", "public", "private", "void"]
#X = [[.1, .01, .3, 0.9], [0.0, 0.3, 0.01, 0.1], [0.12, 0.1, 0.2, 0.4], [0.0, 0.4, 0.0, 0.2]]
#Y = [1, 0, 2, 0]

clf = tree.DecisionTreeClassifier(max_depth=5) #,min_samples_split=0.2,min_weight_fraction_leaf=0.1)
#clf = tree.DecisionTreeClassifier(max_depth=8,min_samples_split=0.2,min_weight_fraction_leaf=0.05)
clf = clf.fit(x, y)
#import graphviz 
#dot_data = tree.export_graphviz(clf, out_file=None) 
#print dot_data
#graph = graphviz.Source(dot_data) 
#graph.render("treep")
# print clf
#dot_data = tree.export_graphviz(clf, out_file=None, 
                         #feature_names=iris.feature_names,  
                         #class_names=iris.target_names,  
#                         filled=True, rounded=True,  
#                         special_characters=True)
#graph = graphviz.Source(dot_data)  
#graph
get_code(clf, features, targets)

