# -*- coding: utf-8 -*-
"""
Grupo tgxxx
Student id #77777
Student id #77777
"""

import numpy as np

def classify(T,data):
    
    data = np.array(data)
    out = []
    for el in data:
        #print("el",el,"out",out,"\nT",T)
        wT = T
        for ii in range(len(el)):
            #print(T[0],el[T[0]],T)
            if el[wT[0]]==0:
                if not isinstance(wT[1], list):
                    out += [wT[1]]
                    break
                else:
                    wT = wT[1]
            else:
                if not isinstance(wT[2], list):
                    out += [wT[2]]
                    break
                else:
                    wT = wT[2]
    return np.array(out)

def countNodes(tree):
    if isinstance(tree, (int, np.integer)):
        return 1
    else:
        return countNodes(tree[1]) + countNodes(tree[2])

def treePruning(D, Y, tree):

    #select only Y's that satisfy tree[0]
    #D(tree[0]) = 0
    if isinstance(tree, (int, np.integer)):
        return tree

    if isinstance(tree[1], (int, np.integer)) and not isinstance(tree[2], (int, np.integer)):
        return [tree[0], tree[1], smallerTree(tree[2])]

    if isinstance(tree[2], (int, np.integer)) and not isinstance(tree[1], (int, np.integer)):
        return [tree[0], smallerTree(tree[1]), tree[2]]

    if isinstance(tree[1], (int, np.integer)) and isinstance(tree[1], (int, np.integer)):
        return tree
    
    elems = Y[Y >= 0]
    Na = np.count_nonzero(elems)
    Nb = len(elems) - Na

    idx = np.where(D.T[tree[0]] == 0)
    Yx1 = np.empty(Y.shape, dtype=np.int32)
    Yx1[:] = -1
    np.put(Yx1, idx, np.take(Y, idx))

    #elems = np.take(Y, idx)



    idx = np.where(D.T[tree[0]] == 1)
    Yx2 = np.empty(Y.shape, dtype=np.int32)
    Yx2[:] = -1
    np.put(Yx2, idx, np.take(Y, idx))
    
    

    #pL = 
    #pR = 
    #K = 


    left = treePruning(D, Yx1, tree[1])
    right = treePruning(D, Yx2, tree[2])



    


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
    
    ps = []
    ns = []

    for v in np.unique(attribute):
        idxs = np.where(attribute == v)
        elems = np.take(examples, idxs)
        elems = elems[elems >= 0]
        p = np.count_nonzero(elems)
        n = len(elems) - p
        ps.append(p)
        ns.append(n)

    p = sum(ps)
    n = sum(ns)

    remainder = 0
    for i, v in enumerate(np.unique(attribute)):
        if (ps[i] + ns[i]) != 0:
            remainder += ((ps[i] + ns[i])/(n+p)) * I(ps[i]/(ps[i]+ns[i]), ns[i]/(ps[i]+ns[i]))

    return I(p/(p+n), n/(p+n)) - remainder


def chooseAttribute(attributes, examples):
    test = [GI(att, examples) if att[0] >= 0 else -1 for att in attributes]
    #print(test)
    return np.argmax(test)

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
        best = chooseAttribute(attributes.T, examples)
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
    import random
    D = D.astype(np.int32)
    Y = Y.astype(np.int32)
    saved_tree = DTL(Y, D, Y)
    saved_tree = smallerTree(saved_tree)
    saved_tree_error = np.mean(np.abs(classify(saved_tree, D) - Y))
    NUM_TRIES = 30
    
    if noise:
        for _ in range(NUM_TRIES):
            SPLIT = random.randint(5,8)/10
            idx = np.random.choice(np.arange(len(D)), int(len(D)*SPLIT), replace=False)
            Dt = D[idx]
            Yt = Y[idx]
            tree = DTL(Yt, Dt, Yt)
            tree = smallerTree(tree)
            err = np.mean(np.abs(classify(tree, D) - Y))
            if (err <= saved_tree_error and len(str(tree)) < len(str(saved_tree))):
                print("Found a better tree!")
                saved_tree = tree
                saved_tree_error = err

    return saved_tree

if __name__ == "__main__":
    #np.random.seed(13102020)
    D = np.array([
              [1,0,0,0],
              [0,0,0,1],
              [1,0,1,0],
              [0,0,1,1],
              [1,1,0,0],
              [0,1,0,1],
              [1,1,1,0],
              [0,1,1,1]]) 

    datasetnumb = 26
    Y = (np.array([datasetnumb%2,datasetnumb%4,datasetnumb%16,datasetnumb%8,datasetnumb%16,datasetnumb%8,datasetnumb%4,datasetnumb%2])>0).astype('int32') 

    tree = createdecisiontree(D, Y)
    print(tree)
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