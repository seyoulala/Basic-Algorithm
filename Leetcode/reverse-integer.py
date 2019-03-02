# -*- coding: utf-8 -*-
# author='XuYingHao'

"""
给出一个 32 位的有符号整数，你需要将这个整数中每位上的数字进行反转。

示例 1:

输入: 123
输出: 321
 示例 2:

输入: -123
输出: -321
示例 3:

输入: 120
输出: 21
注意:

假设我们的环境只能存储得下 32 位的有符号整数，则其数值范围为 [−231,  231 − 1]。请根据这个假设，如果反转后整数溢出那么就返回 0

"""
"""
将x%10得到的余数添加到零时列表中，将x重置为x//10.
"""

from functools import  reduce
class Solution:
    def reverse(self, x):
        """
        :type x: int
        :rtype: int
        """
        if x==0:
            return 0
        tmp = abs(x)
        tmp_list = []
        while tmp:
            tmp_mod = tmp%10
            tmp_list.append(tmp_mod)
            tmp//=10
        ans = reduce(lambda x,y:10*x+y,tmp_list)
        if x>0 and ans<pow(2,31)-1:
            return ans
        if x<0 and -ans>-pow(2,31):
            return -ans
        return 0

    def reverse1(self, x):
        """
		:type x: int
		:rtype: int
		"""
        if x==0:
            return 0
        tmp = abs(x)
        sum = 0
        while tmp:
            tmp_mod = tmp%10
            sum=10*sum+tmp_mod
            tmp//=10

        if x>0 and sum<pow(2,31)-1:
            return sum
        if x<0 and -sum>-pow(2,31):
            return -sum
        return 0
