# -*- coding: utf-8 -*-
"""
Grupo tgxxx
Student id #77777
Student id #77777
"""

import numpy as np

def countNodes(tree):
    if isinstance(tree, (int, np.integer)):
        return 1
    else:
        return countNodes(tree[1]) + countNodes(tree[2])

def treePruning(num, tree):
    for i in range(num):
        x = random.randint(2,pruneTree.countNodes(pruneTree.root)-1)
        tempNode = Node()
        tempNode = searchNode(newTree,x)

        if(tempNode is not None):
            tempNode.left = None
            tempNode.right = None
            tempNode.nodeType = "L"
            if(tempNode.negativeCount >= tempNode.positiveCount):
                tempNode.label = 0
            else:
                tempNode.label = 1

def smallerTree(tree):
    def check_equal(left, right):
        return np.array_equal(left, right)

    if isinstance(tree, (int, np.integer)):
        return [tree, tree, tree]

    if isinstance(tree[1], (int, np.integer)) and not isinstance(tree[2], (int, np.integer)):
        return [tree[0], tree[1], smallerTree(tree[2])]

    if isinstance(tree[2], (int, np.integer)) and not isinstance(tree[1], (int, np.integer)):
        return [tree[0], smallerTree(tree[1]), tree[2]]

    if isinstance(tree[1], (int, np.integer)) and isinstance(tree[1], (int, np.integer)):
        return tree

    if check_equal(tree[1], tree[2]):
        return smallerTree(tree[1])

    else:
        return [tree[0], smallerTree(tree[1]), smallerTree(tree[2])]


def sameClassification(examples):
    x = np.unique(examples)
    x = x[x >= 0]
    return all(x==x[0])

def maxVals(examples):
    count = np.bincount(examples[examples >= 0])
    return np.argmax(count)

def GI(attribute, examples):
    def I(p, n):
        return - p*np.log2(p) - n*np.log2(n) if p > 0 and n > 0 else 0
    
    g = 0
    for v in np.unique(attribute):
        idxs = np.where(attribute == v)
        elems = np.take(examples, idxs)
        #elems = elems[elems > -1]
        p = np.count_nonzero(elems)
        n = len(elems) - p
        g += (len(elems)/len(examples)) * I(p, n)

    return 1 - g


def chooseAttribute(attributes, examples):
    test = [GI(att, examples) if att[0] >= 0 else -1 for att in attributes]
    #print(test)
    return np.argmax(test), max(test)

def DTL(examples, attributes, default):
    if (np.all(examples < 0)):
        return maxVals(default)
    elif (sameClassification(examples)):
        x = np.unique(examples)
        x = x[x >= 0]
        return x[0]
    elif (np.all(attributes.reshape(-1) < 0)):
        return maxVals(examples)
    else:
        best, val = chooseAttribute(attributes.T, examples)
        #print(val)
        #if val < 1:
        #    return []
        tree = []
        tree += [best]
        for v in np.unique(attributes.T[best]):
            valid_idx = np.where(attributes.T[best] == v)

            exs = np.empty(examples.shape, dtype=np.int32)
            exs[:] = -1
            np.put(exs, valid_idx, np.take(examples, valid_idx))

            atts = np.copy(attributes).T
            atts[best] = -1
            atts = atts.T
            
            subtree = DTL(exs, atts, examples)

            tree += [subtree]

        return tree

#                      attributes, examples
def createdecisiontree(D, Y, noise=False):
    D = D.astype(np.int32)
    Y = Y.astype(np.int32)

    tree = DTL(Y, D, Y)
    tree = smallerTree(tree)
    return tree

if __name__ == "__main__":
    np.random.seed(13102020)
    D = np.random.rand(1000,10)>0.5
    Y = ((D[:,1] == 0) & (D[:,6] == 0)) | ((D[:,3] == 1) & (D[:,4] == 1)) 

    #tree = createdecisiontree(D, Y)
    #print(tree)
    #print(len(str(tree)))
    print(countNodes([0, [1,0,0], [1,0,0]]))
    #print(att.T)
    #idx = np.where(att.T[1] == 0)
    #print(idx)
    #vals = np.take(examples, idx, axis=0)
    #print(vals)
    #print(np.count_nonzero(vals))
    #[1, [6, 1, [3, 0, [4, 0, 1]]], [4, 0, [3, 0, 1]]]

    #[1, [3, [6, 1, 0], [4, [6, 1, 0], 1]], [3, 0, [4, 0, 1]]]