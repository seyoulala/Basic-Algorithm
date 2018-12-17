#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Date    : 2018-11-18 21:00:02
# @Author  : xuyinghao (xyh650209@163.com)
# @Link    : https://github.com/seyoulala/Basic-Algorithm
# @Version : $Id$


class TreeNode:
    def __init__(self, x):
        self.val = x
        self.right = None
        self.left = None


class Solution:
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
        return deep, tmp

    def TreeDepth(self, pRoot):
        if pRoot is None:
            return 0
        deep, levervalue = self.orderBylevel(pRoot)
        return deep, levervalue


if __name__ == "__main__":
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
    node3.left = node6
    node3.right = node7

    s = Solution()
    deep, value = s.TreeDepth(node1.left)
    print("树的深度是{0},每层节点的值为{1}".format(deep, value))

