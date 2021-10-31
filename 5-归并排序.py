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
        # 优化2
        if len(alist)<=16:
            alist=insertionSort(alist)
            return alist
        mid=len(alist)//2
        # 切片操作为O(K)，会干扰算法性能
        lefthalf=alist[:mid]
        righthalf=alist[mid:]
        lefthalf=mergeSort(lefthalf)
        righthalf=mergeSort(righthalf)
        # 优化1。
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

def mergeSortBU(alist):
    n=len(alist)
    size=1
    while size<n:
        blist=alist[:]
        i=0
        while i+size<n:
            if alist[i+size-1]<alist[i+size]: #优化1。优化2方案放弃。
                i=i+size+size
                continue
            a,b,c=i,i+size,i
            while a<i+size and b<min(i+size+size,n):
                if blist[a]<=blist[b]:
                    alist[c]=blist[a]
                    a+=1
                else:
                    alist[c]=blist[b]
                    b+=1
                c+=1
            while a<i+size:
                alist[c]=blist[a]
                a+=1
                c+=1
            while b<min(i+size+size,n):
                alist[c]=blist[b]
                b+=1
                c+=1
            i=i+size+size
        size=size+size
    return alist


max=100000
list=[randint(-max,max) for x in range(max)]
alist=list[:]
blist=list[:]
t1=timeit.Timer('mergeSort(alist)','from __main__ import mergeSort,alist')
print('归并排序: %s s' % t1.timeit(number=1))
t2=timeit.Timer('mergeSortBU(blist)','from __main__ import mergeSortBU,blist')
print('BU归并排序: %s s' % t2.timeit(number=1))

'''BU归并算法比普通归并算法还要慢一点??'''

