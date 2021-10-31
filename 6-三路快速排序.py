# -*- coding: utf-8 -*-
from random import randint
import timeit

def quickSort(alist):
    quickSortHelper(alist,0,len(alist)-1)
    return alist

def quickSortHelper(alist,first,last):
    if first<last:
        if last - first <= 16:
            insertionSortForQS(alist, first, last)
        else:
            splitpoint=partition(alist,first,last)
            quickSortHelper(alist,first,splitpoint-1)
            quickSortHelper(alist,splitpoint+1,last)

def partition(alist,first,last):
    rand = randint(first, last)
    alist[first],alist[rand]=alist[rand],alist[first]
    pivotvalue=alist[first]
    leftmark=first+1
    rightmark=last
    done=False
    while not done:
        while leftmark<=rightmark and alist[leftmark]<pivotvalue:
            leftmark+=1
        while rightmark>=leftmark and alist[rightmark]>pivotvalue:
            rightmark-=1
        if leftmark>rightmark:
            done=True
        else:
            alist[leftmark],alist[rightmark]=alist[rightmark],alist[leftmark]
            leftmark+=1
            rightmark-=1
    alist[first],alist[rightmark]=alist[rightmark],alist[first]
    return rightmark

def quickSort3Ways(alist):
    quickSort3WaysHelper(alist,0,len(alist)-1)
    return alist

def quickSort3WaysHelper(alist,first,last):
    if first<last:
        if last - first <= 16:  #优化：当列表足够小的时候使用插入排序
            insertionSortForQS(alist, first, last)
        else:
            ltEnd,gtStart=partition3Ways(alist,first,last)
            quickSort3WaysHelper(alist,first,ltEnd)
            quickSort3WaysHelper(alist,gtStart,last)

def partition3Ways(alist,first,last):
    rand=randint(first,last)
    alist[first], alist[rand] = alist[rand], alist[first]
    pivolvalue=alist[first]
    lt,i,gt=first,first+1,last+1
    done=False
    while not done:
        if alist[i]<pivolvalue:
            alist[lt+1],alist[i]=alist[i],alist[lt+1]
            i+=1
            lt+=1
        elif alist[i]==pivolvalue:
            i+=1
        else:
            alist[gt-1],alist[i]=alist[i],alist[gt-1]
            gt-=1
        if i>=gt:
            done=True
    alist[first],alist[lt]=alist[lt],alist[first]
    lt-=1
    return lt,gt

def insertionSortForQS(alist,first,last):
    #专门为辅助快速排序设计的插入排序
    for i in range(first+1,last+1):
        currentvalue=alist[i]
        position=i
        while position>first and alist[position-1]>currentvalue:
            alist[position]=alist[position-1]
            position=position-1
        alist[position]=currentvalue
    return alist

max=100000

list=[randint(0,10) for x in range(max)]
alist=list[:]
blist=list[:]
t1=timeit.Timer('quickSort(alist)','from __main__ import quickSort,alist')
print('双路快排: %s s' % t1.timeit(number=1))
t2=timeit.Timer('quickSort3Ways(blist)','from __main__ import quickSort3Ways,blist')
print('三路快排: %s s' % t2.timeit(number=1))

""" 对于拥有大量相等值的列表，三路快排拥有相当棒的性能 """
