# -*-coding: utf-8 -*-
from random import randint

# 循环式
def binarySearch(alist,item):
    first=0
    last=len(alist)-1
    while first<=last:
        mid=first+(last-first)//2
        if alist[mid] == item:
            return True
        else:
            if alist[mid]<item:
                last=mid-1
            else:
                first=mid+1
    return False

# 递归式
def binarySearchRecursion(alist,item):
    if len(alist)==0:
        return False
    else:
        mid=len(alist)//2
        if alist[mid]==item:
            return True
        elif alist[mid]<item:
            return binarySearchRecursion(alist[mid+1:],item)
        else:
            return binarySearchRecursion(alist[:mid],item)


alist = []

for i in range(10000):
    alist.append(randint(0, 1000000))

j = randint(0, 1000000)
alist.append(j)

print(j)
print(len(alist))

print(binarySearch(alist, j))
print(binarySearchRecursion(alist, j))
