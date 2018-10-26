#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Author  : xuyinghao
"""
输入一颗二叉树的跟节点和一个整数，打印出二叉树中结点值的和为输入整数的所有路径。
路径定义为从树的根结点开始往下一直到叶结点所经过的结点形成一条路径。(注意: 在返回值的list中，数组长度大的数组靠前)

思路:
通过递归找出所有路径，判断路径中是否有符合条件的解

"""
class TreeNode:
    def __init__(self,x):
        self.val = x
        self.left = None
        self.right = None


class Solution:
    def AllPath(self,root):
        #根节点不存在
        if not root:
            return []
        # 如果没有左右子树
        if root.left == None and root.right == None:
            return [str(root.val)]
        leftPath = [str(root.val) +","+ path for  path in self.AllPath(root.left) ]
        rightPath = [ str(root.val)+","+path for path in self.AllPath(root.right)]
        path = leftPath + rightPath
        return  path

    def FindPath(self, root, expectNumber):
        res = []
        treepath = self.AllPath(root)
        for i in treepath:
            if sum(map(int,i.split(','))) == expectNumber:
                res.append(list(map(int,i.split(','))))
        return res

pNode1 = TreeNode(10)
pNode2 = TreeNode(5)
pNode3 = TreeNode(12)
pNode4 = TreeNode(4)
pNode5 = TreeNode(7)


pNode1.left = pNode2
pNode1.right = pNode3
pNode2.left = pNode4
pNode2.right = pNode5


S = Solution()
print(S.FindPath(pNode1,22))





