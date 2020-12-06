# -*- coding: utf-8 -*-
"""
Grupo alxxx
Student id #77777
Student id #77777
"""

import numpy as np


def sameClassification(examples):
    x = np.unique(examples)
    x = x[x > -1]
    return all(x==x[0])

def maxVals(examples):
    count = np.bincount(examples[examples > -1])
    return np.argmax(count)

def GI(attribute, examples):
    def I(p, n):
        return - p*np.log2(p) - n*np.log2(n) if p != 0 and n != 0 else 0
    
    g = 0
    for v in np.unique(attribute):
        idxs = np.where(attribute == v)
        elems = np.take(examples, idxs, axis=0)
        elems = elems[elems > -1]
        p = np.count_nonzero(elems)
        n = len(elems) - p
        g += (len(elems)/len(examples)) * I(p, n)

    return 1 - g


def chooseAttribute(attributes, examples):
    test = [GI(attributes[i], examples) if i in attributes else -1 for i in range(len(examples))]
    return np.argmax(test)

def DTL(examples, attributes, default):
    if (np.all(examples == -1)):
        return maxVals(default)
    elif (sameClassification(examples)):
        x = np.unique(examples)
        x = x[x > -1]
        return x[0]
    elif (attributes == {}):
        return maxVals(examples)
    else:
        #print("---------")
        best = chooseAttribute(attributes, examples)
        tree = []
        tree += [best]
        for v in np.unique(attributes[best]):
            #print(f"best: {best}")
            #print(f"v: {v}")
            #print(f"attributes: {attributes}")

            valid_idx = np.where(attributes[best] == v)
            #print(f"valid_idx: {valid_idx}")
            valid_idx = [e for e in valid_idx[0] if e < len(examples)]
            #print(f"valid_idx: {valid_idx}")
            #print(f"examples: {examples}")

            exs = np.empty(examples.shape, dtype=np.int64)
            exs[:] = -1
            np.put(exs, valid_idx, np.take(examples, valid_idx))
            #print(exs)
            atts = {i:attributes[i] for i in attributes if i != best}
            
            #print(f"atts: {atts}")
            subtree = DTL(exs, atts, examples)
            #print(f"best: {best}")
            #print(f"v: {v}")
            tree += [subtree]

    return tree
#                      attributes, examples
def createdecisiontree(D, Y, noise=False):
    attributes = {i:att for i, att in enumerate(D.T)}
    tree = DTL(Y, attributes, Y)
    print(tree)
    return tree

if __name__ == "__main__":
    att = np.array([
              [0,0,0],
              [0,0,1],
              [0,1,0],
              [0,1,1],
              [1,0,0],
              [1,0,1],
              [1,1,0],
              [1,1,1]])        
                 
    examples = np.array([0,1,0,1,0,1,0,1])

    print(createdecisiontree(att, examples))

    #print(att.T)
    #idx = np.where(att.T[1] == 0)
    #print(idx)
    #vals = np.take(examples, idx, axis=0)
    #print(vals)
    #print(np.count_nonzero(vals))
