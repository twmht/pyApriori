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
    def __iter__(self):
        self.begin = 0
        return self
    def next(self):
        if self.begin >=  len(self.items):
            raise StopIteration
        self.begin = self.begin+1
        return self.items[self.begin-1]


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
        return len(self.itemsets)

    def add(self,itemset):
        node = self.root
        new = False
        for item in range(0,self.length-1):
            if itemset[item] in node.internalNode:
                node = node.internalNode[itemset[item]]
            else:
                new = True
                n = TreeNode()
                node.internalNode[itemset[item]] = n = TreeNode()
                node = n
        """prefix leaf nodes"""
        """How many leaf nodes do we have"""
        if new == True:
            """This node is a new leaf node"""
            self.leafs.append(node)
        node.itemsets.append(itemset)
        """the total itemsets"""
        self.itemsets.append(itemset)
        """A fake leaf node for antiMonotonePruning"""
        node.internalNode[itemset[-1]] = n =  TreeNode()
        n.itemset = itemset

    """update the support count and find out the frequent itemset"""
    def update(self,itemset,freqSet):
        node = self.root;
        for item in itemset:
            if item in node.internalNode:
                node = node.internalNode[item]
            else:
                return False
        node.itemset.support = node.itemset.support+1
        global transactions,minSupport
        if node.itemset.support == int(minSupport*len(transactions)):
            freqSet.add(node.itemset)

    def exist(self,items):
        node = self.root
        for item in items:
            if item in node.internalNode:
                node = node.internalNode[item]
            else:
                return False
        return node.itemset
    def returnSupport(self,items):
        node = self.root
        for item in items:
            if item in node.internalNode:
                node = node.internalNode[item]
        return node.itemset.support


def antiMonotonePruning(itemset,a,b,freqSet):
    """Every (k-1)-subset in a k-frequent itemset must be frequent"""
    for c in combinations(itemset.items,freqSet.length):
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
    if k == 2:
        """largeSet is a list"""
        for c in combinations(largeSet.iterkeys(),2):
            candidate.add(Itemset(c))
        return candidate
    """largeSet is a HashTree"""
    for leaf in largeSet.leafs:
        for i in range(0,len(leaf.itemsets)):
            for j in range(i+1,len(leaf.itemsets)) :
                a = leaf.itemsets[i]
                b = leaf.itemsets[j]
                if a[k-2] > b[k-2]:
                    r = Itemset(a[0:k-2]+(b[k-2],a[k-2]))
                else:
                    r = Itemset(a[0:k-2]+(a[k-2],b[k-2]))
                if antiMonotonePruning(r,a,b,largeSet) == True:
                    #print r.items
                    candidate.add(r)
    return candidate

def firstPass():
    global transactions,minSupport
    """large 1-itemset and 2-candidates"""
    itemset = defaultdict(int)
    for trans in transactions:
        for item in trans:
            itemset[item] = itemset[item]+1
    largeSet = defaultdict(int)
    for key,value in itemset.items():
        if value >= int(minSupport*len(transactions)):
            largeSet[key] = [value,True]
    return largeSet

def findMaximal(currentLSet,lastLSet):
    if currentLSet.length == 2:
        for itemset in currentLSet.itemsets:
            a = itemset[0]
            b = itemset[1]
            if a in lastLSet:
                lastLSet[a][1] = False
            if b in lastLSet:
                lastLSet[a][1] = False
    else:
        for items in currentLSet.itemsets:
            for c in combinations(items,lastLSet.length):
                itemset = lastLSet.exist(c)
                """if the itemset is not maximal"""
                if itemset != False:
                    itemset.maximal = False

def runApriori():
    """the large-1 itemset"""
    global freqDict
    currentLSet = firstPass()
    assocRules= dict()
    k = 2
    while(len(currentLSet) >= 1):
        freqDict[k-1]= currentLSet
        currentCSet = joinSet(currentLSet,k)
        currentLSet= returnItemsWithMinSupport(currentCSet,k)
        findMaximal(currentLSet,freqDict[k-1])
        k = k + 1

def readCVSfile(infile):
    global transactions
    for trans in infile:
        t = map(int,trans[1:])
        t.sort()
        transactions.append(t)

def readGoods(infile):
    global goods
    for good in infile:
        goods[int(good[0])] = good[1].replace("'","") +' ' + good[2].replace("'","")

def printRules():
    global freqDict,goods,transactions,minConfidence
    for length,tree in freqDict.iteritems():
        if length >= 2:
            """determine the tree to check the support of the left side"""
            leftSupportTree = freqDict[length-1]
            totalSupportTree = freqDict[length]
            for itemset in tree.itemsets:
                if itemset.maximal == True:
                    items = itemset.items
                    for c in combinations(items,length-1):
                        if isinstance(leftSupportTree,dict):
                            leftSupport = leftSupportTree[c[0]][0]
                        else:
                            leftSupport = leftSupportTree.returnSupport(c)
                        totalSupport = totalSupportTree.returnSupport(items)
                        confidence = float(totalSupport)/leftSupport
                        if confidence >= minConfidence:
                            right = set(items).difference(set(c))
                            left = ', '.join(goods[item] for item in c)
                            print left,'-->',goods[next(iter(right))],"[ confidence = ",round(confidence,2),"]"

def printFrequentItemsets():
    global freqDict,goods,transactions
    for key,value in freqDict.iteritems():
        if key == 1:
            for item,value in value.iteritems():
                print goods[item],float(value[0])/len(transactions)
        if key >= 2:
            for itemset in value.itemsets:
                if itemset.maximal == True:
                    items = ', '.join(goods[item] for item in itemset.items)
                    print items,float(itemset.support)/len(transactions)

if __name__ == "__main__":

    global minSupport,minConfidence,transactions,freqDict,goods
    transactions = []
    freqDict = dict()
    goods = dict()

    optparser = OptionParser()
    optparser.add_option('-i', '--inputDatabase', dest = 'input', help = 'the filename which contains the comma separated values',default = None)
    optparser.add_option('-g', '--goods', dest = 'good', help = 'the file specifying the goods',default = None)
    optparser.add_option('-s', '--minSupport', dest='minS', help = 'minimum support value(default=0.15)', default=0.03, type='float')
    optparser.add_option('-c','--minConfidence', dest='minC', help = 'minimum confidence value(default = 0.6)', default = 0.5, type='float')

    (options, args) = optparser.parse_args()

    if options.input is not None:
        readCVSfile(csv.reader(open(options.input,'r')))
    else:
        print 'No dataset filename specified, system with exit\n'
        sys.exit('System will exit')

    if options.good is not None:
        readGoods(csv.reader(open(options.good,'r')))
    else:
        print 'No goods name specified, system with exit\n'
        sys.exit('System will exit')

    minSupport = options.minS
    minConfidence = options.minC
    runApriori()
    #printFrequentItemsets()
    printRules()
