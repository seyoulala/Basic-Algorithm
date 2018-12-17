#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Author  : xuyinghao

class TreeNode:
    def __init__(self,x):
        self.val = x
        self.left = None
        self.right = None

class Solution:
    def Printlevel(self,pRoot):
        if pRoot == None:
            return None
        nodes,res = [pRoot],[]
        left_to_right = True
        while nodes:
            curvalues,nextStack =[],[]
            for node in nodes:
                curvalues.append(node.val)
                if node.left:
                    nextStack.append(node.left)
                if node.right:
                    nextStack.append(node.right)
            if not left_to_right:
                curvalues.reverse()
            if curvalues:
                res.append(curvalues) #保存当前层的值
            nodes = nextStack
            left_to_right = not left_to_right
        return res


node1 = TreeNode(1)
node2 = TreeNode(2)
node3 = TreeNode(3)
node4 = TreeNode(4)
node5 = TreeNode(5)
node6 = TreeNode(6)
node7 = TreeNode(7)

node1.left = node2
node1.right = node3
node2.left = node4
node2.right = node5
node3.left = node6
node3.right = node7

s = Solution()
print(s.Printlevel(node1))
