#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Author  : xuyinghao
"""
输入n个整数，找出其中最小的K个数。例如输入4,5,1,6,2,7,3,8这8个数字，则最小的4个数字是1,2,3,4。
"""

"""
思路：第一种方法是基于划分的方法，如果是查找第k个数字，第一次划分之后，划分的位置如果大于k，那么就在前面的子数组中进行继续划分，
反之则在后面的子数组继续划分，时间复杂度O(n)；第二种方法是可以适用于海量数据的方法，该方法基于二叉树或者堆来实现，首先把数组前k个数字构建一个最大堆，
然后从第k+1个数字开始遍历数组，如果遍历到的元素小于堆顶的数字，那么久将换两个数字，重新构造堆，继续遍历，最后剩下的堆就是最小的k个数，时间复杂度O(nlog k)。
"""
import heapq

class Solution:
    #构建大根堆
    def GetLeastNumbers(self, tinput, k):
        if len(tinput) == 0 or len(tinput) <k or k==0:
            return None
        output = []
        for i in tinput:
            if len(output)<k:
                output.append(i)
            else:
                output = heapq.nlargest(k,output)
                if output[0] > i:
                    continue
                else:
                    output[0] = i
        return  output[::-1]


tinput1 = [4,5,1,6,2,7,3,8]
s = Solution()
print(s.GetLeastNumbers(tinput1,4))
