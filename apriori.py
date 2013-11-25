import sys

from itertools import  combinations
from collections import defaultdict
from optparse import OptionParser

class Itemset(object):
    def __init__(self,items):
        self.items = items
        self.support = 0

class TreeNode(object):
    def __init__(self):
        self.internalNode = dict()

"""fast-join"""
class PrefixTree(object):
    def __init__(self):
        self.root = dict()
        self.leaf = []
    def add(self,itemset):
        node = self.root
        for i in range(0,len(itemset.items)-1):
            b = itemset.items[i]
            if b in node.internalNode:
                node = node.internalNode[b]
            else:
                n = TreeNode()
                node.internalNode[b] = n
                node = n
        node.append(itemset)

"""anti-monotone strategy"""
class HashTree(object):
    def __init__(self,fp = True):
        self.leaf = []
        self.root = TreeNode()
        self.fp = fp;
    def add(self,itemset):
        if self.fp == True:
            items = itemset.items[0:len(itemset.items)-1]
        else:
            items = itemset.items
        node = self.root
        for item in items:
            if item in node.internalNode:
                node = node.internalNode[item]
            else:
                n = TreeNode()
                node.internalNode[item] = n
                node = n
        node.leaf.append(items)
    def update(self,itemset):
        node = self.root;
        for item in itemset:
            if item in node.internalNode:
                node = node.internalNode
            else:
                return False
        node.leaf[0] = node.leaf[0]+1



def subsets(itemset,k):
    """ Returns non empty subsets of arr"""
    return combinations(itemset,k-1)


def antiMonotonePruning():
    pass
def returnItemsWithMinSupport(transactionList,freqSet, candidates, minSupport,k):
    if k > 2:
        antiMonotonePruning(freqSet,candidates,k)
    newFreqSet = HashTree(fp = True)
    for transaction in transactionList:
        for subset in subsets(transaction,k+1):
            candidates.update(subset)


def joinSet(tree,k):
    """Join a set with itself and returns the n-element itemsets"""
    candidates = HashTree()
    for leaf in tree.leaf:
        for i in range(0,len(leaf)):
            for j in range(i+1,len(leaf)):
                if leaf[i][-1]>leaf[j][-1]:
                    items = [item for item in leaf[i][0:k-1]]
                    items.append(leaf[j][-1])
                    items.append(leaf[i][-1])
                else:
                    items = [item for item in leaf[i][0:k-1]]
                    items.append(leaf[i][-1])
                    items.append(leaf[j][-1])
    return candidates


def initial(data_iterator,minSupport):
    """large 1-itemset and 2-candidates"""
    itemset = dict(int)
    for record in data_iterator:
        for item in record:
            itemset[item] = itemset[item]+1
    largeset = []
    for key,value in itemset.items():
        if value >= minSupport:
            largeset.append(key)

    candidates = HashTree(fp = False)
    for i in range(0,len(largeset)):
        for j in range(i+1,len(largeset)):
            candidates.add(Itemset([largeset[i],largeset[j]]))
    return large,candidates

def runApriori(data_iter, minSupport, minConfidence):
    """the large-1 itemset and candidates-2 itemset"""
    currentLSet,currentCSet = initial(data_iter,minSuppor)
    assocRules= dict()
    k = 2
    while(currentLSet != set([])):
        largeSet[k-1]= currentLSet
        currentLSet= returnItemsWithMinSupport(currentLSet, currentCSet, minSupport)
        currentCSet = joinSet(currentLSet)
        k = k + 1

    def getSupport(item):
        """local function which Returns the support of an item"""
        return float(freqSet[item])/len(transactionList)

    toRetItems=[]
    for key,value in largeSet.items():
        toRetItems.extend([(tuple(item), getSupport(item))
            for item in value])

        toRetRules=[]
    for key,value in largeSet.items()[1:]:
        for item in value:
            _subsets = map(frozenset,[x for x in subsets(item)])
            for element in _subsets:
                remain = item.difference(element)
                if len(remain)>0:
                    confidence = getSupport(item)/getSupport(element)
                    if confidence >= minConfidence:
                        toRetRules.append(((tuple(element),tuple(remain)),
                            confidence))
                        return toRetItems, toRetRules


def printResults(items, rules):
    """prints the generated itemsets and the confidence rules"""
    for item, support in items:
        print "item: %s , %.3f" % (str(item), support)
    print "\n------------------------ RULES:"
    for rule, confidence in rules:
        pre, post = rule
        print "Rule: %s ==> %s , %.3f" % (str(pre), str(post), confidence)


def dataFromFile(fname):
    """Function which reads from the file and yields a generator"""
    file_iter = open(fname, 'rU')
    for line in file_iter:
        record = (map(int,line.split(',')))
        record.sort()
        yield record


if __name__ == "__main__":

    optparser = OptionParser()
    optparser.add_option('-f', '--inputFile', dest = 'input', help = 'the filename which contains the comma separated values', default=None)
    optparser.add_option('-s', '--minSupport', dest='minS', help = 'minimum support value', default=0.15, type='float')
    optparser.add_option('-c','--minConfidence', dest='minC', help = 'minimum confidence value', default = 0.6, type='float')

    (options, args) = optparser.parse_args()

    if options.input is None:
        inFile = sys.stdin
    elif options.input is not None:
        inFile = dataFromFile(options.input)
    else:
        print 'No dataset filename specified, system with exit\n'
        sys.exit('System will exit')

    minSupport		= options.minS
    minConfidence = options.minC
    items, rules	= runApriori(inFile, minSupport, minConfidence)

    printResults(items,rules)
