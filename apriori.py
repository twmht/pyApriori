import sys
import csv

from itertools import  combinations
from collections import defaultdict
from optparse import OptionParser
class Itemset(object):
    def __init__(self,items):
        self.items = items
        self.maximal = True
        self.support = 0
    def __eq__(self,other):
        if not isinstance(other,Itemset):
            return False
        return self.items == other.items
    def __len__(self):
        return len(self.items)
    def __getitem__(self,key):
        return self.items[key]

class TreeNode(object):
    def __init__(self):
        self.internalNode = dict()
        """How many itemset share the same prefix"""
        self.itemsets = []
        """For sub-set checking"""
        self.itemset = None

class HashTree(object):
    def __init__(self,k):
        self.root = TreeNode()
        """how many leaf nodes"""
        """Each leaf node stores the frequent itemsets where each of them shares the same prefix"""
        self.leafs = []
        self.itemsets = []
        self.length = k

    def __len__(self):
        return self.length

    def add(self,itemset):
        node = self.root
        new = False
        for item in range(0,len(itemset)-1):
            if item in node.internalNode:
                node = node.internalNode[item]
            else:
                new = True
                n = TreeNode()
                node.internalNode[item] = n
                node = n
        """prefix leaf nodes"""
        """How many leaf nodes do we have"""
        if new == True:
            self.leafs.append(node)
        node.itemsets.append(itemset)
        """for antiMonotonePruning"""
        n = TreeNode()
        node.internalNode[itemset[-1]] = n
        n.itemset = itemset
        self.itemsets.append(n.itemset)

    def update(self,itemset,freqSet):
        node = self.root;
        for item in itemset:
            if item in node.internalNode:
                node = node.internalNode[item]
            else:
                return False
        node.itemset.support = node.itemset.support+1

        global transactions,minSupport
        if node.itemset.support == minSupport*len(transactions):
            freqSet.add(node.itemset)

    def exist(self,itemset):
        node = self.root
        for item in itemset.items:
            if item in node.internalNode:
                node = node.internalNode[item]
            else:
                return False
        return node.itemset


def antiMonotonePruning(itemset,a,b,freqSet):
    """Every (k-1)-subset in a k-frequent itemset must be frequent"""
    for c in combinations(itemset.items,len(freqSet)-1):
        if c != a and c != b:
            if not freqSet.exist(c):
                return False
    return True

def returnItemsWithMinSupport(candidateSet, k):
    global transactions
    freqSet = HashTree(k)
    for t in transactions:
        for c in combinations(t,k):
            candidateSet.update(c,freqSet)
    return freqSet

def joinSet(largeSet,k):
    candidate = HashTree(k)
    print k
    if k == 2:
        """largeSet is a list"""
        for c in combinations(largeSet,2):
            candidate.add(Itemset(c))
        return candidate
    """largeSet is a HashTree"""
    for leaf in largeSet.leafs:
        for i in range(0,len(leaf.itemsets)):
            for j in range(i+1,len(leaf.itemsets)) :
                a = leaf.itemset[i].items
                b = leaf.itemset[j].items
                if a[k-1] > b[k-1]:
                    r = itemset(a[0:k-1]+[b[k-1],a[k-1]])
                else:
                    r = itemset(a[0:k-1]+[a[k-1],b[k-1]])
                if antiMonotonePruning(r,a,b,freqSet) == True:
                    candidate.add(r)
    return candidate

def firstPass():
    global transactions,minSupport
    """large 1-itemset and 2-candidates"""
    itemset = defaultdict(int)
    for trans in transactions:
        for item in trans:
            itemset[item] = itemset[item]+1
    largeSet = []
    for key,value in itemset.items():
        if value >= minSupport*len(transactions):
            largeSet.append(key)
    largeSet.sort()
    return largeSet

def findMaximal(currentLSet,lastLSet):
    for items in currentLSet.itemsets:
        for c in combinations(items,len(lastLSet)):
            itemset = lastLSet.exist(c)
            if itemset != False:
                itemset.maximal = True

def runApriori():
    """the large-1 itemset"""
    global freqDict
    currentLSet = firstPass()
    assocRules= dict()
    k = 2
    while(len(currentLSet)>1):
        freqDict[k-1]= currentLSet
        currentCSet = joinSet(currentLSet,k)
        currentLSet= returnItemsWithMinSupport(currentCSet,k)
        if k >= 3:
            findMaximal(currentLSet,freqDict[k-1])
        k = k + 1

def readCVSfile(infile):
    global transactions
    print (infile.line_num)
    for trans in infile:
        t = map(int,trans[1:])
        t.sort()
        transactions.append(t)

def readGoods(infile):
    global goods
    for good in infile:
        goods[int(good[0])] = good[1]

def printFrequentItemsets():
    global freqDict,goods
    for key,value in freqDict.iteritems():
        for itemset in value.itemsets:
            items = ','.join(goods[item] for item in itemset.items)
            print items

if __name__ == "__main__":

    global minSupport,minConfidence,transactions,freqDict,goods
    transactions = []
    freqDict = dict()
    goods = dict()

    optparser = OptionParser()
    optparser.add_option('-i', '--inputDatabase', dest = 'input', help = 'the filename which contains the comma separated values',default = None)
    optparser.add_option('-g', '--goods', dest = 'good', help = 'the file specifying the goods',default = None)
    optparser.add_option('-s', '--minSupport', dest='minS', help = 'minimum support value(default=0.15)', default=0.03, type='float')
    optparser.add_option('-c','--minConfidence', dest='minC', help = 'minimum confidence value(default = 0.6)', default = 0.6, type='float')

    (options, args) = optparser.parse_args()

    if options.input is not None:
        readCVSfile(csv.reader(open(options.input,'r')))
    else:
        print 'No dataset filename specified, system with exit\n'
        sys.exit('System will exit')

    if options.good is not None:
        readGoods(cvs.reader(open(options.good,'r')))

    minSupport = options.minS
    minConfidence = options.minC
    runApriori()
    printFrequentItemsets()
