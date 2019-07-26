#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Date    : 2018-12-03 21:45:28
# @Author  : xuyinghao (xyh650209@163.com)
# @Link    : https://github.com/seyoulala/Basic-Algorithm
# @Version : $Id$

'''
找出所有和为S的连续正数序列
输出所有和为S的连续正数序列。序列内按照从小至大的顺序，序列间按照开始数字从小到大的顺序
'''

"""
思路:用两个指针begin,end分别表示序列的最小值和最大值，
首先将begin,end初始化为1,2.
如果begin到end的和大于s那么去掉较小的值(增大begin)
想反只需要增加end.

终止条件，begin<(s+1)/2,并且end< s

思路２:
    由于要求的是连续的正整数数组,因此数组的求和可以用等差数列的求和公式来求解
    首先划定一个长度为１的窗口,求窗口内连续数字的和，若窗口内的数比要求的数更小
    那么窗口的右边移动一位，若窗口内的数要更大，那么窗口左边界移动一位。等到左边
    界赶上右边界的时候循环结束
"""


class Solution:
    def FindContinuousSequence(self, tsum):
        # write code here
        res = []
        for i in range(1, tsum // 2 + 1):
            sumRes = i
            for j in range(i + 1, tsum // 2 + 2):
                sumRes += j
                if sumRes == tsum:
                    res.append(list(range(i, j + 1)))
                    break
                elif sumRes > tsum:
                    break
        return res

    def FindContinuousSequence1(self, tsum):
        """
        由于要求的是连续的真整数数组,因此数组的求和可以用等差数列的求和公式来求解
        #首先划定一个长度为１的窗口,求窗口内连续数字的和，若窗口内的数比要求的数更小
        那么窗口的右边移动一位，若窗口内的数要更大，那么窗口左边界移动一位
        :param tsum:
        :return:
        """
        begin=1
        end=2
        res =[]
        while begin<end:
            #求窗口内的和,等差数列求和公式
            total_sum = (end+begin)*(end-begin+1)/2
            if total_sum ==tsum:
                #如果窗口内的数和目标值相等的话，那就返回窗口内连续的数值
                res.append(list(range(begin,end+1)))
                begin+=1
            elif total_sum>tsum:
                begin+=1
            else:
                end+=1
        #若循环退出了还没有找到，说明已经找不到了
        return res

s = Solution()
print(s.FindContinuousSequence(100))
