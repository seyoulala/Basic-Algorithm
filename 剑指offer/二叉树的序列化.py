#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Date    : 2019-08-10 10:52:35
# @Author  : xuyinghao (xyh650209@163.com)
# @Link    : https://github.com/seyoulala/Basic-Algorithm
# @Version : $Id$


class TreeNode:

    def __init__(self, x):
        self.val = x
        self.left = None
        self.right = None


class Solution:
    def serizlBypre(self, node: TreeNode)->str:
        # basecase
        if node is None:
            return '#_'
        res = str(node.val) + '_'
        # 接住左子树的值
        res += self.serizlBypre(node.left)
        res += self.serizlBypre(node.right)
        return res

    def serizlByInoder(self, node):
        if node is None:
            return '#_'
        res = ''
        res += self.serizlByInoder(node.left)
        res += str(node.val) + '_'
        res += self.serizlByInoder(node.right)
        return res

    def serizlBypos(self, node):
        if node is None:
            return '#_'
        res = ''
        res += self.serizlBypos(node.left)
        res += self.serizlBypos(node.right)
        res += str(node.val) + '_'
        return res

    def serizlBypos(self, node):
        if node is None:
            return "#_"
        res = ''
        res += self.serizlBypos(node.left)
        res += self.serizlBypos(node.right)
        res += str(node.val) + '_'
        return res

    def reconByPreString(self, preStr: list)-> TreeNode:
        value = preStr.pop(0)
        if value == '#':
            return None
        head = TreeNode(value)
        head.left = self.reconByPreString(preStr)
        head.right = self.reconByPreString(preStr)
        return head
    # def reconByInString(self, inStr):


if __name__ == '__main__':
    node1 = TreeNode(1)
    node2 = TreeNode(2)
    node3 = TreeNode(3)
    node4 = TreeNode(4)
    node5 = TreeNode(5)
    node1.left = node2
    node2.left = node3
    node1.right = node4
    node4.left = node5
    s = Solution()
    # preStr = s.serizlBypre(node1)
    # preStr = list(preStr.split('_'))
    # print(s.reconByPreString(preStr).val)
    inStr = s.serizlByInoder(node1)
    inStr = list(inStr.split('_'))
    print(s.reconByPreString(inStr).val)
