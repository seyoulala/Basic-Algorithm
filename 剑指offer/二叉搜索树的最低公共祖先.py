#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Author  : xuyinghao

class TreeNode:
    def __init__(self,x):
        self.val = x
        self.left = None
        self.right = None

class Solution:
    def lowestCommonAncestor(self,A,B,root):
        if A  is None or B is None:
            return -1
        if A.val == B.val:
            return -1

        val_left = A.val
        val_right = B.val

        while root !=None:
            if (root.val - val_left) * (root.val - val_right) <=0:
                return root
            #如果目标节点的值都比根节点值要小,那么目标节点应该在根节点左边
            elif root.val > val_left and root.val > val_right:
                root = root.left

            else:
                root = root.right
        return -1


node1 = TreeNode(7)
node2 = TreeNode(5)
node3 = TreeNode(9)
node4 = TreeNode(4)
node5 = TreeNode(6)
node6 = TreeNode(8)
node7 = TreeNode(10)

node1.left = node2
node1.right = node3
node2.left = node4
node2.right = node5
node3.left = node6
node3.right = node7

s = Solution()
print(s.lowestCommonAncestor(node6,node7,node1).val)
