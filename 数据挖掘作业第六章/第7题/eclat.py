FREQUENT = 30


class Eclat:

    def __init__(self, min_support=FREQUENT, max_items=2):
        self.min_support = min_support
        self.max_items = max_items
        self.result = []
        self.itemDict = {}

    def fit(self, transactions):
        self.transactions = transactions
        self.num_transactions = len(transactions)
        self._get_items()

    def _get_items(self):
        items = []
        k = 0
        for transaction in self.transactions:
            k += 1
            for item in transaction:
                if ([item] not in items):
                    items.append([item])
                if (frozenset([item]) not in self.itemDict):
                    self.itemDict[frozenset([item])] = set()
                self.itemDict[frozenset([item])].add(k)
        self.items = sorted(list(items))
        self.filter(self.itemDict, self.items)

    def filter(self, itemDict, keys):
        for key in keys:
            if (len(itemDict[frozenset(key)]) < self.min_support):
                del itemDict[frozenset(key)]
            else:
                self.result.append(key)
        return itemDict

    def _get_frequent_itemsets(self):
        nextRound = self.items
        for i in range(0, self.max_items):
            nextRound = self.__generate_next_itemList(nextRound)
            self.itemDict = self.filter(self.itemDict, nextRound)
            if not nextRound:
                break
        return self.result

    def __generate_next_itemList(self, itemList):
        next_itemList = []
        for i in range(len(itemList)):
            for j in range(i+1, len(itemList)):
                if ((itemList[i][:-1] == itemList[j][:-1]) and (self.itemDict.get(frozenset(itemList[i]), {})) and (self.itemDict.get(frozenset(itemList[j]), {}))):
                    newList = [x for x in itemList[i]]
                    newList.append(itemList[j][-1])
                    next_itemList.append(newList)
                    self.itemDict[frozenset(newList)] = self.itemDict[frozenset(
                        itemList[i])].intersection(self.itemDict[frozenset(itemList[j])])
        return next_itemList
