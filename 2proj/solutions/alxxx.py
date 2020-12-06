# -*- coding: utf-8 -*-
"""
Grupo alxxx
Student id #77777
Student id #77777
"""

import numpy as np
"""
class Node:
    def __init__(self, data = None):
        self.left = None
        self.right = None
        self.data = data

    @property
    def left(self):
        return self.left

    @property.setter
    def left(self, node : Node):
        self.left = node

    @property
    def right(self):
        return self.right

    @property.setter
    def right(self, node : Node):
        self.right = node
"""

def sameClassification(attributes):
    return np.all(attributes == attributes[0])

def maxVals(examples):
    count = np.bincount(examples.reshape(-1))
    return np.argmax(count)

def GI(attribute, examples):
    def I(p, n):
        return - p*np.log2(p) - n*np.log2(n) if p != 0 and n != 0 else 0
    
    g = 0
    for v in np.unique(attribute):
        idxs = np.where(attribute == v)
        elems = np.take(examples, idxs, axis=0)
        p = np.count_nonzero(elems)
        n = len(elems) - p
        g += (len(elems)/len(examples)) * I(p, n)

    return 1 - g


def chooseAttribute(attributes, examples):
    return np.argmax(GI(att[i], examples) for i in range(len(examples)))

def DTL(examples, attributes, default):
    if (not examples.any()):
        return maxVals(default)
    elif (sameClassification(attributes)):
        return attributes[0]
    elif (not attributes.any()):
        return maxVals(examples)
    else:
        print("---------")
        best = chooseAttribute(attributes, examples)
        tree = []
        for v in np.unique(attributes.T[best]):
            print(f"best: {best}")
            print(f"attributes: {attributes}")

            valid_idx = np.where(attributes.T[best] == v)
            print(f"valid_idx: {valid_idx}")
            valid_idx = [e for e in valid_idx[0] if e < len(examples)]
            print(f"examples: {examples}")

            exs = np.take(examples, valid_idx).reshape(-1)

            atts = np.concatenate((attributes.T[:best] ,attributes.T[best + 1:])).T
            
            print(f"atts: {atts}")
            subtree = DTL(exs, atts, default)
            tree = best, v, subtree

    return tree


if __name__ == "__main__":
    att = np.array([[0, 0],
                    [0, 1],
                    [1, 0],
                    [1, 1]])        
                 
    examples = np.array([0,0,0,1])

    print(DTL(examples, att, examples))

    #print(att.T)
    #idx = np.where(att.T[1] == 0)
    #print(idx)
    #vals = np.take(examples, idx, axis=0)
    #print(vals)
    #print(np.count_nonzero(vals))

    chooseAttribute(att, examples)