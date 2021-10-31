# -*- coding: utf-8 -*-
import re

from base.binary_search_tree import BinarySearchTree

# 简单实现
# python 中的 Counter?
tree = BinarySearchTree()
with open('8-test.txt', 'r', encoding='utf-8') as f:
    file = f.read()
words = list(re.split('\W+', file))
for word in words:
    word = word.lower()
    if tree[word] is None:
        tree[word] = 1
    else:
        tree[word] = tree[word] + 1

print(tree['god'])
