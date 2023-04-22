FREQUENT = 30


class Apriori:

    # 判断itemList是否在order中
    def __contains(self, order, itemList):
        for item in itemList:
            if item not in order:
                return False
        return True

    # 计算itemList在shoppingCart中出现的次数
    def __count(self, itemList, shoppingCart):
        count = 0
        for order in shoppingCart:
            if (self.__contains(order, itemList)):
                count += 1
        return count

    # 生成下一层的itemList
    def __generate_next_itemList(self, itemList):
        next_itemList = []
        for i in range(len(itemList)):
            for j in range(i+1, len(itemList)):
                if itemList[i][:-1] == itemList[j][:-1]:
                    newList = [x for x in itemList[i]]
                    newList.append(itemList[j][-1])
                    next_itemList.append(newList)
        return next_itemList

    # 生成第一层的itemList
    def __getFirstItemLists(self, items):
        firstItemList = [[x] for x in set(items)]
        return firstItemList

    # 过滤掉不满足最小支持度的itemList
    def __filter(self, itemLists, shoppingCart):
        filterList = []
        for itemList in itemLists:
            if self.__count(itemList, shoppingCart) >= FREQUENT:
                filterList.append(itemList)
        return filterList

    # 主函数,也是对外接口
    def analyze(self, items, shoppingCart):
        itemLists = self.__getFirstItemLists(items)
        totalFrequentItemLists = []

        while len(itemLists) > 0:
            filteredItemLists = []
            filteredItemLists = self.__filter(itemLists, shoppingCart)
            if (len(filteredItemLists) > 0):
                totalFrequentItemLists.append(filteredItemLists)
            nextItemList = self.__generate_next_itemList(filteredItemLists)
            itemLists = nextItemList

        return totalFrequentItemLists
