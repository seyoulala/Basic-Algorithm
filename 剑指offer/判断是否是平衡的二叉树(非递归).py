#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Date    : 2018-11-21 21:48:46
# @Author  : xuyinghao (xyh650209@163.com)
# @Link    : https://github.com/seyoulala/Basic-Algorithm
# @Version : $Id$

"""
输入一棵二叉树，判断该二叉树是否是平衡二叉树
"""

"""
思路:平衡二叉树的定义是，任意一个非叶子节点的左右孩子高度差不能超过1.
所以通过之前求树的深度，我们也可以解决一个问题
遍历每个节点，判断每个节点的左右孩子高度差
"""


class TreeNode:
    def __init__(self, x):
        self.val = x
        self.left = None
        self.right = None


class Solution:

    def IsBalanced_Solution(self, root):
        if root is None:
            return True
        stack = [root]
        while len(stack) != 0:
            cur = 0
            width = len(stack)
            while cur < width:
                root = stack.pop(0)
                if root.left:
                    stack.append(root.left)
                leftdepth = self.orderBylevel(root.left)
                if root.right:
                    stack.append(root.right)
                rightdepth = self.orderBylevel(root.right)
                if abs(leftdepth - rightdepth) > 1:
                    return False
                cur += 1
        return True

    def orderBylevel(self, pRoot):
        if pRoot is None:
            return 0
        stack = []  # 辅助栈
        deep = 0  # 树深
        stack.append(pRoot)  # 根节点先入栈
        tmp = []  # 每层节点的值
        while len(stack) != 0:
            cur = 0
            width = len(stack)  # 层宽度
            tmp_list = []  # 记录同层节点值
            while cur < width:
                root = stack.pop(0)  # 从左向右遍历,节点先进先出
                if root.left:
                    stack.append(root.left)
                if root.right:
                    stack.append(root.right)
                tmp_list.append(root.val)
                cur += 1
            deep += 1
            tmp.append(tmp_list)
        return deep
