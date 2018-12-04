#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Date    : 2018-11-21 21:00:55
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
    """
    获取树的高度
    """

    def TreeDepth(self, root):
        if root is None:
            return 0
        return max(self.TreeDepth(root.left), self.TreeDepth(root.right)) + 1
    """
    递归判断左右孩子高度
    """

    def IsBalanced_Solution(self, root):
        if root is None:
            return True
        left = self.TreeDepth(root.left)
        right = self.TreeDepth(root.right)
        if abs(left - right) > 1:
            return False
        return self.IsBalanced_Solution(root.left) and self.IsBalanced_Solution(root.right)
    # 树深的非递归

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


if __name__ == '__main__':
    node1 = TreeNode(1)
    node2 = TreeNode(2)
    node3 = TreeNode(3)
    node4 = TreeNode(4)
    node5 = TreeNode(5)
    node6 = TreeNode(6)
    node7 = TreeNode(7)
    node8 = TreeNode(8)

    node1.left = node2
    node1.right = node3
    node2.left = node4
    node2.right = node5

    s = Solution()
    print(s.IsBalanced_Solution(node1))
