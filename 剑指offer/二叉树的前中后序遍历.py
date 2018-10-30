#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Author  : xuyinghao

class TreeNode:
    def __init__(self,x):
        self.val = x
        self.left = None
        self.right = None


class Solution:

    def PreOrder(self,root):
        if root :
            print(root.val)
            self.PreOrder(root.left)
            self.PreOrder(root.right)
    def MinOrder(self,root):
        if root is not  None:
            self.MinOrder(root.left)
            print(root.val)
            self.MinOrder(root.right)
    def PostOrder(self,root):
        if root is not None:
            self.PostOrder(root.left)
            self.PostOrder(root.right)
            print(root.val)





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

if __name__ =='__main__':

    s = Solution()
    # s.PreOrder(pNode1)
    s.MinOrder(pNode1)
    # s.PostOrder(pNode1)
