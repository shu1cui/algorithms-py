# -*- coding: utf-8 -*-
import timeit
from random import randint


def mergeSort(alist):
    if len(alist) > 1:
        if len(alist) <= 16:
            alist = insertionSort(alist)
            return alist
        mid = len(alist) // 2
        lefthalf = alist[:mid]
        righthalf = alist[mid:]
        lefthalf = mergeSort(lefthalf)
        righthalf = mergeSort(righthalf)
        if lefthalf[-1] <= righthalf[0]:
            alist = lefthalf + righthalf
            return alist
        i, j, k = 0, 0, 0
        while i < len(lefthalf) and j < len(righthalf):
            if lefthalf[i] <= righthalf[j]:
                alist[k] = lefthalf[i]
                i += 1
            else:
                alist[k] = righthalf[j]
                j += 1
            k += 1
        while i < len(lefthalf):
            alist[k] = lefthalf[i]
            k += 1
            i += 1
        while j < len(righthalf):
            alist[k] = righthalf[j]
            k += 1
            j += 1
    return alist


def insertionSort(alist):
    for i in range(1, len(alist)):
        currentvalue = alist[i]
        position = i
        while alist[position - 1] > currentvalue and position > 0:
            alist[position] = alist[position - 1]
            position = position - 1
        alist[position] = currentvalue
    return alist


def quickSort(alist):
    quickSortHelper(alist, 0, len(alist) - 1)
    return alist


def quickSortHelper(alist, first, last):
    if first < last:
        if last - first <= 16:
            insertionSortForQS(alist, first, last)
        else:
            splitpoint = partition(alist, first, last)
            quickSortHelper(alist, first, splitpoint - 1)
            quickSortHelper(alist, splitpoint + 1, last)


def partition(alist, first, last):
    rand = randint(first, last)
    alist[first], alist[rand] = alist[rand], alist[first]
    pivotvalue = alist[first]
    leftmark = first + 1
    rightmark = last
    done = False
    while not done:
        while leftmark <= rightmark and alist[leftmark] < pivotvalue:
            leftmark += 1
        while rightmark >= leftmark and alist[rightmark] > pivotvalue:
            rightmark -= 1
        if leftmark > rightmark:
            done = True
        else:
            alist[leftmark], alist[rightmark] = alist[rightmark], alist[leftmark]
            leftmark += 1
            rightmark -= 1
    alist[first], alist[rightmark] = alist[rightmark], alist[first]
    return rightmark


def insertionSortForQS(alist, first, last):
    for i in range(first + 1, last + 1):
        currentvalue = alist[i]
        position = i
        while position > first and alist[position - 1] > currentvalue:
            alist[position] = alist[position - 1]
            position = position - 1
        alist[position] = currentvalue
    return alist


class IndexMaxHeap(object):
    def __init__(self):
        self.indexList = [0]
        self.items = {}
        self.currentSize = 0

    def shiftUp(self, i):
        currentvalue = self.items[self.indexList[i]]
        currentindex = self.indexList[i]
        while i // 2 > 0:
            if self.items[self.indexList[i // 2]] < currentvalue:
                self.indexList[i] = self.indexList[i // 2]
                i = i // 2
            else:
                break
        self.indexList[i] = currentindex

    def insert(self, k, value):
        self.indexList.append(k)
        self.items[k] = value
        self.currentSize += 1
        self.shiftUp(self.currentSize)

    def shiftDown(self, i):
        currentvalue = self.items[self.indexList[i]]
        currentindex = self.indexList[i]
        while i * 2 <= self.currentSize:
            mc = self.maxChild(i)
            if currentvalue < self.items[self.indexList[mc]]:
                self.indexList[i] = self.indexList[mc]
                i = mc
            else:
                break
        self.indexList[i] = currentindex

    def maxChild(self, i):
        if i * 2 + 1 > self.currentSize:
            return i * 2
        else:
            if self.items[self.indexList[i * 2]] > self.items[self.indexList[i * 2 + 1]]:
                return i * 2
            else:
                return i * 2 + 1

    def delFirst(self):
        retval = self.items[self.indexList[1]]
        del self.items[self.indexList[1]]
        if self.currentSize == 1:
            self.currentSize -= 1
            self.indexList.pop()
            return retval
        self.indexList[1] = self.indexList[self.currentSize]
        self.indexList.pop()
        self.currentSize -= 1
        self.shiftDown(1)
        return retval

    def buildHeap(self, items):
        self.items = items
        self.indexList = [0] + list(self.items.keys())
        self.currentSize = items.__len__()
        i = self.currentSize // 2
        while i > 0:
            self.shiftDown(i)
            i -= 1

    def getItem(self, i):
        return self.items[i]

    def maxItemIndex(self):
        return self.indexList[1]

    def change(self, k, newValue):
        if k not in self.indexList:
            raise Exception('%s is not exist!' % k)
        self.items[k] = newValue
        i = self.indexList.index(k)  # index方法的复杂度是O1，根本不需要实现reverse列表。我猜python内部就是靠reverse列表来实现这个index方法的。
        self.shiftDown(i)
        self.shiftUp(i)
        return True


heap = IndexMaxHeap()
items = {'天禄': 87, '良龙': 76, '老秦': 65, '魏红': 98, '吴梦': 54}  # 按照分数构成最大堆
heap.buildHeap(items)
heap.insert('树熠', 32)
print('最高分: %s %s' % (heap.maxItemIndex(), heap.items[heap.maxItemIndex()]))
print('良龙: %s' % heap.getItem('良龙'))
# 将良龙的分数提高到99
heap.change('良龙', 99)
print('最高分: %s %s' % (heap.maxItemIndex(), heap.items[heap.maxItemIndex()]))
heap.delFirst()
print('最高分: %s %s' % (heap.maxItemIndex(), heap.items[heap.maxItemIndex()]))

'''python dict 实现索引堆实在是太嗖嗖嗖了'''
