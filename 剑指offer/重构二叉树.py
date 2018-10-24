#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Author  : xuyinghao

class TreeNode:
    def __init__(self,x):
        self.val = x
        self.left = None
        self.right = None

class Solution:
    def reconstructTree(self,pre,tin):
        if not pre and not tin :
            return  None

        root = TreeNode(pre[0])
        if set(pre) != set(tin):
            return None
        index = tin.index(pre[0])
        root.left = self.reconstructTree(pre[1:index+1],tin[0:index])
        root.right = self.reconstructTree(pre[index+1:],tin[index+1])

        return  root

pre = [1, 2, 3, 5, 6, 4]
tin = [5, 3, 6, 2, 4, 1]
test = Solution()
newTree = test.reconstructTree(pre, tin)
print(newTree.val)
