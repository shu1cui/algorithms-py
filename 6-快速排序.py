# -*- coding: utf-8 -*-
from random import randint
import timeit

def insertionSort(alist):
    for i in range(1,len(alist)):
        currentvalue=alist[i]
        position=i
        while alist[position-1]>currentvalue and position>0:
            alist[position]=alist[position-1]
            position=position-1
        alist[position]=currentvalue
    return alist

def mergeSort(alist):
    if len(alist)>1:
        if len(alist)<=16:
            alist=insertionSort(alist)
            return alist
        mid=len(alist)//2
        lefthalf=alist[:mid]
        righthalf=alist[mid:]
        lefthalf=mergeSort(lefthalf)
        righthalf=mergeSort(righthalf)
        if lefthalf[-1] <= righthalf[0]:
            alist=lefthalf+righthalf
            return alist
        i,j,k=0,0,0
        while i<len(lefthalf) and j<len(righthalf):
            if lefthalf[i]<=righthalf[j]:
                alist[k]=lefthalf[i]
                i+=1
            else:
                alist[k]=righthalf[j]
                j+=1
            k+=1
        while i<len(lefthalf):
            alist[k]=lefthalf[i]
            k+=1
            i+=1
        while j<len(righthalf):
            alist[k]=righthalf[j]
            k+=1
            j+=1
    return alist

def quickSort(alist):
    quickSortHelper(alist,0,len(alist)-1)
    return alist

def quickSortHelper(alist,first,last):
    if first<last:
        if last - first <= 16:  #优化：当列表足够小的时候使用插入排序
            insertionSortForQS(alist, first, last)
        else:
            splitpoint=partition(alist,first,last)
            quickSortHelper(alist,first,splitpoint-1)
            quickSortHelper(alist,splitpoint+1,last)

def partition(alist,first,last):
    rand = randint(first, last) #优化，随机取标定点，以解决近乎有序的列表
    alist[first],alist[rand]=alist[rand],alist[first]
    pivotvalue=alist[first]
    leftmark=first+1
    rightmark=last
    done=False
    while not done:  #这里使用了双路快排，以解决有大量相同值的列表
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
list=[randint(-max,max) for x in range(max)]
alist=list[:]
blist=list[:]
t1=timeit.Timer('mergeSort(alist)','from __main__ import mergeSort,alist')
print('归并排序: %s s' % t1.timeit(number=1))
t2=timeit.Timer('quickSort(blist)','from __main__ import quickSort,blist')
print('快速排序: %s s' % t2.timeit(number=1))

""" 在对快速排序进行优化时, 感觉能够将列表均衡分开的标定点才是好的标定点。均匀分开意味着保持logn的复杂度。 """
