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


class MaxHeap(object):
    def __init__(self, max=100000):
        self.heapList = [0]
        self.currentSize = 0
        self.maximum = max

    def shiftUp(self, i):
        currentvalue = self.heapList[i]
        while i // 2 > 0:
            if self.heapList[i // 2] < currentvalue:
                self.heapList[i] = self.heapList[i // 2]  # 优化：赋值替代交换
                i = i // 2
            else:
                break
        self.heapList[i] = currentvalue

    def insert(self, k):
        self.heapList.append(k)
        self.currentSize += 1
        self.shiftUp(self.currentSize)
        if self.currentSize > self.maximum:  # 在最大堆中这个操作会保留m个最小的元素。
            self.delFirst()

    def shiftDown(self, i):
        currentvalue = self.heapList[i]
        while i * 2 <= self.currentSize:
            mc = self.maxChild(i)
            if currentvalue < self.heapList[mc]:
                self.heapList[i] = self.heapList[mc]
                i = mc
            else:
                break
        self.heapList[i] = currentvalue

    def maxChild(self, i):
        if i * 2 + 1 > self.currentSize:
            return i * 2
        else:
            if self.heapList[i * 2] > self.heapList[i * 2 + 1]:
                return i * 2
            else:
                return i * 2 + 1

    def delFirst(self):  # 之所以叫delFirst是因为这个函数可以兼容最大堆和最小堆
        retval = self.heapList[1]
        if self.currentSize == 1:
            self.currentSize -= 1
            self.heapList.pop()
            return retval
        self.heapList[1] = self.heapList[self.currentSize]
        self.heapList.pop()
        self.currentSize -= 1
        self.shiftDown(1)
        return retval

    def buildHeap(self, alist):  # heapify
        self.heapList = [0] + alist[:]
        self.currentSize = len(alist)
        i = self.currentSize // 2
        while i > 0:
            self.shiftDown(i)
            i -= 1
        overflow = self.currentSize - self.maximum
        for i in range(overflow):
            self.delFirst()

    def HeapSort(self, alist):
        self.buildHeap(alist)
        sortedList = [self.delFirst() for x in range(self.currentSize)]
        sortedList.reverse()
        return sortedList

    def HeapSortInPlace(self, alist):
        self.buildHeap(alist)
        while self.currentSize > 1:
            self.heapList[1], self.heapList[self.currentSize] = self.heapList[self.currentSize], self.heapList[1]
            self.currentSize -= 1
            self.shiftDown(1)
        return self.heapList[1:]


class MinHeap(MaxHeap):  # 最小堆，继承自MaxHeap，覆盖了父类的上浮和下沉操作，酌情使用。
    def __init__(self):
        super(MaxHeap, self).__init__()

    def shiftUp(self, i):
        currentvalue = self.heapList[i]
        while i // 2 > 0:
            if self.heapList[i // 2] > currentvalue:
                self.heapList[i] = self.heapList[i // 2]
                i // 2
            else:
                break
        self.heapList[i] = currentvalue

    def shiftDown(self, i):
        currentvalue = self.heapList[i]
        while i * 2 <= self.currentSize:
            mc = self.minChild(i)
            if currentvalue > self.heapList[mc]:
                self.heapList[i] = self.heapList[mc]
                i = mc
            else:
                break
        self.heapList[i] = currentvalue

    def minChild(self, i):
        if i * 2 + 1 > self.currentSize:
            return i * 2
        else:
            if self.heapList[i * 2] < self.heapList[i * 2 + 1]:
                return i * 2
            else:
                return i * 2 + 1


heap = MaxHeap()
max = 50000
list = [randint(-max, max) for x in range(max)]
alist = list[:]
blist = list[:]
clist = list[:]
t1 = timeit.Timer('heap.HeapSort(alist)', 'from __main__ import heap,alist')
print('堆排序: %s s' % t1.timeit(number=1))
t2 = timeit.Timer('heap.HeapSortInPlace(blist)', 'from __main__ import heap,blist')
print('堆原地排序: %s s' % t2.timeit(number=1))
t3 = timeit.Timer('quickSort(clist)', 'from __main__ import quickSort,clist')
print('快速排序: %s s' % t3.timeit(number=1))
