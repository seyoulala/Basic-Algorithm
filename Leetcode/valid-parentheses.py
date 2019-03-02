# -*- coding: utf-8 -*-
# @Time : 2019/1/27 18:59
# @Author : XuYingHao
# @File : valid-parentheses.py

"""
"""


class Solution:
    def isValid(self, s):
        """
        :type s: str
        :rtype: bool
        """
        map_to_dict = {")": "(", "}": "{", "]": "["}
        stack = []
        for i in s:
            # 如果是右括号,看栈顶元素是否类型的左括号
            if i in map_to_dict.keys():
                if stack:
                    top_element = stack.pop()
                else:
                    top_element = '$'  # 任何字符
                if map_to_dict[i] != top_element:
                    return False
            else:
                stack.append(i)
        if len(stack) != 0:
            return False
        return True
