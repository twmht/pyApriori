import sys
import csv

from itertools import  combinations
from collections import defaultdict
from optparse import OptionParser

class Itemset(object):
    def __init__(self,items):
        self.items = items
        self.support = 0
    def __equal__(self,other):
        return self.items == other.items
    def __len__(self):
        return len(self.items)

class TreeNode(object):
    def __init__(self):
        self.internalNode = dict()
        """How many itemset share the same prefix"""
        self.itemsets = []

class HashTree(object):
    def __init__(self):
        self.root = TreeNode()
        self.itemset = None
        """how many leaf nodes"""
        self.leaf = []
        self.length = 0

    def __len__(self):
        return self.length

    def add(self,itemset):
        node = self.root
        for item in range(0,len(itemset)-1):
            if item in node.internalNode:
                node = node.internalNode[item]
            else:
                n = TreeNode()
                node.internalNode[item] = n
                node = n
        """prefix leaf nodes"""
        if(len(self.leaf) == 0):
            """How many leaf nodes do we have"""
            self.leaf.append(node)
        node.itemsets.append(itemset)
        if itemset[-1] in node.internalNode:
            node = node.internalNode[itemset[-1]]
        else:
            n = TreeNode()
            node.internalNode[item] = n
        """Number of itemset is incremented"""
        n.itemset = itemset
        self.length = self.length+1

    def update(self,itemset,freqSet):
        node = self.root;
        for item in itemset:
            if item in node.internalNode:
                node = node.internalNode[item]
            else:
                return False
        node.itemset = node.itemset.support+1

        global transactions,minSupport
        if node.itemset.suppot/len(transactions) == minSupport:
            freqSet.add(node.itemset)

    def exist(self,itemset):
        node = self.root
        for item in itemset.items:
            if item in node.internalNode:
                node = node.internalNode[item]
            else:
                return False
        return True


def antiMonotonePruning(itemset,a,b,freqSet):
    """Every subset in a frequent itemset must be frequent"""
    for c in combinations(itemset.items,len(freqSet)-1):
        if c != a and c != b:
            if not freqSet.exist(c):
                return False
    return True

def returnItemsWithMinSupport(candidateSet, k):
    global transactions
    freqSet = HashTree()
    for t in transactions:
        for c in combinations(t,k):
            candidateSet.update(itemset(c),freqSet)
    return freqSet

def joinSet(largeSet,k):
    candidate = HashTree()
    if k == 2:
        """largeSet is a list"""
        for c in combinations(largeSet,2):
            candidate.add(c)
        return candidate
    """largeSet is a HashTree"""
    for leaf in largeSet.leafs:
        for i in range(0,len(leaf.itemsets)):
            for j in range(i+1,len(leaf.itemsets)) :
                if leaf.itemsets[i].items[k-1]>leaf.itemsets[j].items[k-1]:
                    a = leaf.itemset[i].items
                    b = leaf.itemset[j].items
                    r = itemset(a[0:k-1]+[b[k-1],a[k-1]])
                    if antiMonotonePruning(r,a,b,freqSet) == True:
                        candidate.add(r)
    return candidate

def firstPass():
    global transactions,minSupport
    """large 1-itemset and 2-candidates"""
    itemset = dict(int)
    for trans in transactions:
        for item in trans:
            itemset[item] = itemset[item]+1
    largeSet = []
    for key,value in itemset.items():
        if value >= minSupport:
            largeSet.append(key)
    largeSet.sort()
    return largeSet

def runApriori():
    """the large-1 itemset"""
    global freqDict
    currentLSet = firstPass()
    assocRules= dict()
    k = 2
    while(len(currentLSet)>1):
        freqDict[k-1]= currentLSet
        currentCSet = joinSet(currentLSet,k)
        currentLSet= returnItemsWithMinSupport(currentLSet, currentCSet)
        k = k + 1


def readCVSfile(infile):
    global transactions
    for trans in infile:
        t = trans[1:]
        t.sort()
        transactions.append(t)

if __name__ == "__main__":

    global minSupport,minConfidence,transactions,freqDict
    transactions = []
    freqDict = dict()

    optparser = OptionParser()
    optparser.add_option('-f', '--inputFile', dest = 'input', help = 'the filename which contains the comma separated values')
    optparser.add_option('-s', '--minSupport', dest='minS', help = 'minimum support value(default=0.15)', default=0.15, type='float')
    optparser.add_option('-c','--minConfidence', dest='minC', help = 'minimum confidence value(default = 0.6)', default = 0.6, type='float')

    (options, args) = optparser.parse_args()

    if options.input is not None:
        readCVSfile(csv.reader(open(options.input,'r')))
    else:
        print 'No dataset filename specified, system with exit\n'
        sys.exit('System will exit')

    minSupport		= options.minS
    minConfidence = options.minC
    runApriori()

    printResults(items,rules)
