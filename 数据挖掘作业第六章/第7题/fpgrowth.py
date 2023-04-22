FREQUENT = 30


class FPNode:
    # basic node in FP tree
    def __init__(self, name, count, parent):
        self.name = name
        self.count = count
        self.parent = parent
        self.children = {}
        self.sameNodeLink = None

    # add count to node
    def more(self, count):
        self.count += count


class FPAlgorithm:
    def __init__(self, minSup):
        self.minSup = minSup

    # 将原始事务集转换为字典形式

    def createInitSet(self, dataSet):
        retDict = {}
        for trans in dataSet:
            retDict[frozenset(trans)] = 1
        return retDict

    # 同一个元素的链表，尾插法
    def updateHeader(self, nodeToTest, targetNode):
        while (nodeToTest.sameNodeLink is not None):
            nodeToTest = nodeToTest.sameNodeLink
        nodeToTest.sameNodeLink = targetNode

    # 追踪一条路径
    def ascendTree(self, leafNode, prefixPath):
        if leafNode.parent is not None:
            prefixPath.append(leafNode.name)
            self.ascendTree(leafNode.parent, prefixPath)

    def findPrefixPath(self, basePat, treeNode):
        condPats = {}
        while treeNode is not None:
            prefixPath = []
            self.ascendTree(treeNode, prefixPath)
            if len(prefixPath) > 1:
                condPats[frozenset(prefixPath[1:])] = treeNode.count
            treeNode = treeNode.sameNodeLink
        return condPats

    def updateTree(self, items, inTree, headerTable, count):
        if items[0] in inTree.children:
            inTree.children[items[0]].more(count)
        else:
            inTree.children[items[0]] = FPNode(items[0], count, inTree)
            if headerTable[items[0]][1] is None:
                headerTable[items[0]][1] = inTree.children[items[0]]
            else:
                self.updateHeader(headerTable[items[0]][1],
                                  inTree.children[items[0]])

        if len(items) > 1:
            self.updateTree(items[1:], inTree.children[items[0]],
                            headerTable, count)

    def createTree(self, dataset):
        headerTable = {}
        for order in dataset:
            for item in order:
                headerTable[item] = headerTable.get(item, 0) + 1

        for k in list(headerTable.keys()):
            if headerTable[k] < FREQUENT:
                del (headerTable[k])

        freqItemSet = set(headerTable.keys())
        if len(freqItemSet) == 0:
            return None, None

        for k in headerTable:
            headerTable[k] = [headerTable[k], None]

        root = FPNode('Null Set', 1, None)

        for tran, count in dataset.items():
            localD = {}
            for item in tran:
                if item in freqItemSet:
                    localD[item] = headerTable[item][0]
            if len(localD) > 0:
                orderedItems = [v[0]
                                for v in sorted(localD.items(), key=lambda p:p[1], reverse=True)]
                self.updateTree(orderedItems, root, headerTable, count)

        return root, headerTable

    def mineTree(self, inTree, headerTable, minSup, preFix, freqItemList):
        bigL = [v[0]
                for v in sorted(headerTable.items(), key=lambda p:str(p[1]))]
        for basePat in bigL:
            newFreqSet = preFix.copy()
            newFreqSet.add(basePat)

            freqItemList.append(newFreqSet)
            condPattBases = self.findPrefixPath(
                basePat, headerTable[basePat][1])
            myCondTree, myHead = self.createTree(condPattBases)
            if myHead is not None:
                self.mineTree(myCondTree, myHead, minSup,
                              newFreqSet, freqItemList)

    def analyse(self, shoppingCart):
        self.trans = shoppingCart
        self.dataset = self.createInitSet(shoppingCart)
        root, headerTable = self.createTree(self.dataset)
        freqItemList = []
        self.mineTree(root, headerTable, FREQUENT, set([]), freqItemList)
        return freqItemList
