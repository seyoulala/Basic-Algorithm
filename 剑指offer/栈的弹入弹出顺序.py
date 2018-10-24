#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Author  : xuyinghao

"""
输入两个整数序列，第一个序列表示栈的压入顺序，请判断第二个序列是否可能为该栈的弹出顺序。假设压入栈的所有数字均不相等。
例如序列1,2,3,4,5是某栈的压入顺序，序列4,5,3,2,1是该压栈序列对应的一个弹出序列，
但4,3,5,1,2就不可能是该压栈序列的弹出序列。（注意：这两个序列的长度是相等的）

思路：
新建一个辅助栈，顺序将压入栈中的数压入辅助栈，同时判断辅助栈栈顶元素是否等于
弹出序列首元素，若不相等，则继续压栈，否则pop出元素。
若最后辅助栈为空，那么弹出序列是该栈的弹出序列，否则不是
"""
class Solution:

    def IsPopOrder(self, pushV, popV):
        if len(pushV)==0 or len(popV) ==0:
            return  False
        #辅助栈
        stack = []
        for i in pushV:
            stack.append(i)
            if stack[-1] != popV[0]:
                continue
            else:
                stack.pop()
                popV.pop(0)

        while len(stack) >0 and stack[-1] == popV[0]:
            stack.pop()
            popV.pop(0)

        if len(stack) == 0:
            return  True
        else:
            return  False

s = Solution()
pre = [1,2,3,4,5]
after = [4,3,5,1,2]
print(s.IsPopOrder(pre,after))