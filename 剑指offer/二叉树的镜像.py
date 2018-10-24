#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Author  : xuyinghao

class TreeNode:
    def __init__(self,x):
        self.val = x
        self.left = None
        self.right = None

class Solution:
    def Mirror(self,proot):
        if proot == None:
            return -1
        if proot.left == None and proot.right == None:
            return proot

        tmp = proot.left
        proot.left = proot.right
        proot.right = tmp

        self.Mirror(proot.left)
        self.Mirror(proot.right)


    #非递归实现
    def Mirror2(self,proot):
        if proot == None:
            return  -1
        stacknode = [proot]
        while len(stacknode)>0:
            root = stacknode.pop(0)
            if root.left != None or root.right != None:
                root.left ,root.right = root.right,root.left
            if root.left :
                stacknode.append(root.left)
            if root.right:
                stacknode.append(root.right)


pNode1 = TreeNode(8)
pNode2 = TreeNode(6)
pNode3 = TreeNode(10)
pNode4 = TreeNode(5)
pNode5 = TreeNode(7)
pNode6 = TreeNode(9)
pNode7 = TreeNode(11)

pNode1.left = pNode2
pNode1.right = pNode3
pNode2.left = pNode4
pNode2.right = pNode5
pNode3.left = pNode6
pNode3.right = pNode7

s = Solution()
s.Mirror(pNode1)
print(pNode1.left.left.val)


