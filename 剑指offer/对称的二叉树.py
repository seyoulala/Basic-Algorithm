#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Author  : xuyinghao

"""
判断是否是对称的二叉树
"""

class TreeNode:
    def __init__(self, x):
        self.val = x
        self.left = None
        self.right = None
class Solution:
    def isSymmetrical(self, pRoot):
         return self.selfIsSymmetrical(pRoot, pRoot)
    def selfIsSymmetrical(self, pRoot1, pRoot2):
        if pRoot1 == None and pRoot2 == None:
            return True
        if pRoot1 == None or pRoot2 == None:
            return False
        if pRoot1.val != pRoot2.val:
            return False
        return self.selfIsSymmetrical(pRoot1.left, pRoot2.right) and self.selfIsSymmetrical(pRoot1.right, pRoot2.left)

    def isSymmetrical1(self,pRoot):
        preoutput = self.PreOrder(pRoot)
        mirroutput= self.mirrOrder(pRoot)
        if preoutput == mirroutput:
            return True
        return False


    def PreOrder(self,pRoot):
        if pRoot is None:
            return [None]
        val_stack = []
        node_stack = []
        pNode = pRoot
        while pNode:
            node_stack.append(pNode)
            val_stack.append(pNode.val)
            pNode = pNode.right
            if not pNode:
                val_stack.append(None)

            if len(node_stack)>0:
                pNode = node_stack.pop()
                pNode = pNode.left
                if not pNode:
                    val_stack.append(None)
        return  val_stack

    def mirrOrder(self, pRoot):
        if pRoot is None:
            return [None]
        val_stack = []
        node_stack = []
        pNode = pRoot
        while pNode :
            node_stack.append(pNode)
            val_stack.append(pNode.val)
            pNode = pNode.right

            if not pNode:
                val_stack.append(None)

            if len(node_stack) > 0:
                pNode = node_stack.pop()
                pNode = pNode.left
                if not pNode:
                    val_stack.append(None)

        return val_stack


pNode1 = TreeNode(1)
pNode2 = TreeNode(2)
pNode3 = TreeNode(3)
pNode4 = TreeNode(4)
pNode5 = TreeNode(5)
pNode6 = TreeNode(6)
pNode7 = TreeNode(7)
pNode8 = TreeNode(8)

pNode1.left = pNode2
pNode1.right = pNode3
pNode2.left = pNode4
pNode2.right = pNode5

pNode3.left = pNode6
pNode3.right = pNode7
pNode4.left = pNode8

pNode3.left = pNode6
pNode3.right = pNode7









