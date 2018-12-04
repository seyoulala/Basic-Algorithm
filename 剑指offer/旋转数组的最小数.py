#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Date    : 2018-10-12 22:06:45
# @Author  : Your Name (you@example.org)
# @Link    : http://example.org
# @Version : $Id$
"""
有序旋转数组的最小值
1. 旋转数组的首元素肯定不小于尾元素的值，使用二分查找，若中间元素的
值大于尾元素，说明最小值在后半区域，front = mid。中间元素值小于首元素
则最小值在前半区域，rear = mid
2. 假若旋转元素的个数为0，即首元素小于尾元素。那么首元素为最小值
3. 假若首尾和中间元素相等，则遍历数组，依次寻找。
"""


class Solution:
    def minNumberInRotateArray(self, rotateArray):
        if len(rotateArray) == 0:
            return None
        front = 0
        rear = len(rotateArray) - 1
        minval = rotateArray[0]
        if rotateArray[front] < rotateArray[rear]:
            return rotateArray[front]
        else:
            while rear - front > 1:
                mid = (front + rear) // 2
                if rotateArray[mid] > rotateArray[rear]:
                    front = mid
                elif rotateArray[mid] < rotateArray[front]:
                    rear = mid
                elif rotateArray[front] == rotateArray[mid] == rotateArray[rear]:
                    for i in range(1, len(rotateArray)):
                        if rotateArray[i] < minval:
                            minval = rotateArray[i]
                            rear = i
            minval = rotateArray[rear]
        return minval


Test = Solution()
print(Test.minNumberInRotateArray([3, 4, 5, 1, 2]))
print(Test.minNumberInRotateArray([1, 2, 3, 4, 5]))
print(Test.minNumberInRotateArray([1, 1, 1, 0, 1]))
print(Test.minNumberInRotateArray([1, 0, 1, 1, 1]))
print(Test.minNumberInRotateArray([]))
print(Test.minNumberInRotateArray([1]))
