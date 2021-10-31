# -*- coding: utf-8 -*-
from base.binary_search_tree import BinarySearchTree, TreeNode


class AVLTree(BinarySearchTree):
    def __init__(self):
        super(AVLTree, self).__init__()

    def _put(self, key, val, currentNode):
        if key < currentNode.key:
            if currentNode.hasLeftChild():
                self._put(key, val, currentNode.leftChild)
            else:
                currentNode.leftChild = TreeNode(key, val, parent=currentNode)
                self.updateBalance(currentNode.leftChild, insert=True)
        else:
            if currentNode.hasRightChild():
                self._put(key, val, currentNode.rightChild)
            else:
                currentNode.rightChild = TreeNode(key, val, parent=currentNode)
                self.updateBalance(currentNode.rightChild, insert=True)

    def delete(self, key):
        if self.size > 1:
            nodeToRemove = self._get(key, self.root)
            if nodeToRemove:
                if nodeToRemove.hasBothChildren():
                    succ = nodeToRemove.findSuccessor()
                    succ.addChildAttr()
                    self.remove(nodeToRemove)
                    nodeToRemove = succ
                else:
                    nodeToRemove.addChildAttr()
                    self.remove(nodeToRemove)
                self.updateBalance(nodeToRemove, first2delete=True)
                self.size = self.size - 1
            else:
                raise KeyError('Error, key not in tree')
        elif self.size == 1 and self.root.key == key:
            self.root = None
            self.size = self.size - 1
        else:
            raise KeyError('Error, key not in tree')

    def updateBalance(self, node, insert=False, delete=False, first2delete=False):
        if node.balanceFactor > 1 or node.balanceFactor < -1:
            # 如果碰到不平衡的树结构，就需要再平衡。如果碰不到，就一路更新父节点的平衡因子就行，那是运气很好了
            self.rebalance(node)
            return
        if node.parent != None:
            if insert:
                if node.isLeftChild():
                    node.parent.balanceFactor += 1
                elif node.isRightChild():
                    node.parent.balanceFactor -= 1
                if node.parent.balanceFactor != 0:
                    self.updateBalance(node.parent, insert=True)
            if first2delete:
                '''
                第一次删除操作传进来的节点是已被删除的节点，这个节点虽然还知道自己父亲是谁，但他的父亲已经不知道自己孩子是谁了
                所以这个节点调用isLeftChild() 或者 isRightChild()一定是False。
                所以我们要在TreeNode里面添加两个属性isleftchild and is rightchild
                '''
                recursion = False
                if node.parent.balanceFactor != 0:
                    recursion = True
                if node.isleftchild:
                    node.parent.balanceFactor -= 1
                elif node.isrightchild:
                    node.parent.balanceFactor += 1
                if recursion:
                    self.updateBalance(node.parent, delete=True)
            if delete:
                recursion = False
                if node.parent.balanceFactor != 0:
                    recursion = True
                if node.isLeftChild():
                    node.parent.balanceFactor -= 1
                elif node.isRightChild():
                    node.parent.balanceFactor += 1
                if recursion:
                    self.updateBalance(node.parent, delete=True)

    def rebalance(self, node):
        if node.balanceFactor < 0:
            if node.rightChild.balanceFactor > 0:
                self.rotateRight(node.rightChild)
                self.rotateLeft(node)
            else:
                self.rotateLeft(node)
        elif node.balanceFactor > 0:
            if node.leftChild.balanceFactor < 0:
                self.rotateLeft(node.leftChild)
                self.rotateRight(node)
            else:
                self.rotateRight(node)

    def rotateLeft(self, rotRoot):
        newRoot = rotRoot.rightChild
        rotRoot.rightChild = newRoot.leftChild
        if newRoot.leftChild != None:
            newRoot.leftChild.parent = rotRoot
        newRoot.parent = rotRoot.parent
        if rotRoot.isRoot():
            self.root = newRoot
        else:
            if rotRoot.isLeftChild():
                rotRoot.parent.leftChild = newRoot
            else:
                rotRoot.parent.rightChild = newRoot
        newRoot.leftChild = rotRoot
        rotRoot.parent = newRoot
        rotRoot.balanceFactor = rotRoot.balanceFactor + 1 - min(newRoot.balanceFactor, 0)
        newRoot.balanceFactor = newRoot.balanceFactor + 1 + max(rotRoot.balanceFactor, 0)

    def rotateRight(self, rotRoot):
        '''
        右旋转逻辑有点绕
        需要旋转的点一共有四个, 分别是新、旧父节点，新父节点的孩子(右旋转中是右孩子)和旧父节点的父节点
        每个节点有两组关联节点，父亲和孩子。
        那么，要更改4个点×2组关联=八组关联
        但事实上，只有新旧父节点是两个关联都需要修改，新父节点的孩子只要改自己的父亲，旧父节点的父节点只要改自己的孩子。
        所以，一共需要改6个关联关系。
        并且这6项更改是有顺序的。
        '''
        newRoot = rotRoot.leftChild
        rotRoot.leftChild = newRoot.rightChild
        if newRoot.rightChild != None:
            newRoot.rightChild.parent = rotRoot
        newRoot.parent = rotRoot.parent
        if rotRoot.isRoot():
            self.root = newRoot
        else:
            if rotRoot.isLeftChild():
                rotRoot.parent.leftChild = newRoot
            else:
                rotRoot.parent.rightChild = newRoot
        newRoot.rightChild = rotRoot
        rotRoot.parent = newRoot
        rotRoot.balanceFactor = rotRoot.balanceFactor - 1 - max(newRoot.balanceFactor, 0)
        newRoot.balanceFactor = newRoot.balanceFactor - 1 + min(rotRoot.balanceFactor, 0)


tree = AVLTree()
tree[0] = 'a'
tree[1] = 'a'
tree[2] = 'a'
tree[3] = 'a'
tree[4] = 'a'
tree[5] = 'a'

tree.levelOrder()
print('\n')

del tree[5]
del tree[4]

tree.levelOrder()
