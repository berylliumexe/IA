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

def sameClassification(Y):
    return np.all(Y == Y[0])

def maxVals(D):
    count = np.bincount(D)
    return np.argmax(count)

def chooseAttribute(attributes, examples):
    bestAtt = 0
    bestRatio = 0
    for i, att in enumerate(attributes.T):
        posAtt = np.count_nonzero(np.take(examples, np.where(att == 1), axis=0))
        negAtt = np.count_nonzero(np.take(examples, np.where(att == 0), axis=0))

        posRatio = abs(posAtt - examples.shape[0]/2)
        negRatio = abs(negAtt - examples.shape[0]/2)

        totRatio = posRatio + negRatio

        if (totRatio > bestRatio):
            bestAtt = i
            bestRatio = totRatio
    
    return bestAtt

def createdecisiontree(D,Y, noise = False):
    if (D == []):
        return noise
    elif (sameClassification(Y)):
        return Y[0]
    elif (Y == []):
        return maxVals(D)
    else:
        best = chooseAttribute(Y, D)
        tree = []
        for v in (0, 1):
            examplesi = np.take(Y, np.where(D == 1), axis=0)
            subtree = createdecisiontree(examplesi, Y[:best] + Y[best+1:], maxVals(Y))
            tree = best, v, subtree

    return tree


if __name__ == "__main__":
    att = np.array([[0, 0],
                    [0, 1],
                    [1, 0],
                    [1, 1]])        
                 
    examples = np.array([1,0,1,1])

    print(att.T)
    idx = np.where(att.T[1] == 0)
    print(idx)
    vals = np.take(examples, idx, axis=0)
    print(vals)
    print(np.count_nonzero(vals))

    chooseAttribute(att, examples)