#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Author  : xuyinghao

class TreeNode:
    def __init__(self,x):
        self.val = x
        self.right = None
        self.left = None

class Solution:
    def AhasB(self,pHead1,pHead2):
        result = False
        if pHead1 != None and pHead2 !=None:
            if pHead1.val == pHead2.val:
                result = self.SameStruct(pHead1,pHead2)
            if not result:
                result = self.AhasB(pHead1.left,pHead2)
            if not result:
                result = self.AhasB(pHead1.right,pHead2)
        return  result

    def SameStruct(self,proot1,proot2):
        if proot2 == None:
            return  True
        if proot1 == None:
            return False
        if proot1.val !=proot2.val:
            return  False
        return  self.SameStruct(proot1.left,proot2.left) and self.SameStruct(proot1.right,proot2.right)


node1 = TreeNode(1)
node2 = TreeNode(2)
node3 = TreeNode(3)
node4 = TreeNode(4)
node5 = TreeNode(5)

node1.left = node2
node1.right = node3
node2.left = node4
node2.right = node5

node11 = TreeNode(1)
node22 = TreeNode(2)
node33 = TreeNode(3)

node11.left = node22
node11.right = node33

s = Solution()
print(s.AhasB(node1,node11))