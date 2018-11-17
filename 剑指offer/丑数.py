#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Date    : 2018-11-16 18:46:17
# @Author  : Your Name (you@example.org)
# @Link    : http://example.org
# @Version : $Id$

"""
首先从丑数的定义我们知道，一个丑数的因子只有2,3,5，那么丑数p = 2 ^ x * 3 ^ y * 5 ^ z，换句话说一个丑数一定由另一个丑数乘以2或者乘以3或者乘以5得到，
那么我们从1开始乘以2,3,5，就得到2,3,5三个丑数，在从这三个丑数出发乘以2,3,5就得到4，6,10,6，9,15,10,15,25九个丑数，
我们发现这种方法会得到重复的丑数，而且我们题目要求第N个丑数，这样的方法得到的丑数也是无序的。那么我们可以维护三个队列：
（1）丑数数组： 1
乘以2的队列：2
乘以3的队列：3
乘以5的队列：5
选择三个队列头最小的数2加入丑数数组，同时将该最小的数乘以2,3,5放入三个队列；
（2）丑数数组：1,2
乘以2的队列：4
乘以3的队列：3，6
乘以5的队列：5，10
我们没有必要维护三个队列，只需要记录三个指针显示到达哪一步；“|”表示指针,arr表示丑数数组；
（1）1
|2
|3
|5
目前指针指向0,0,0，队列头arr[0] * 2 = 2,  arr[0] * 3 = 3,  arr[0] * 5 = 5
（2）1 2
2 |4
|3 6
|5 10
目前指针指向1,0,0，队列头arr[1] * 2 = 4,  arr[0] * 3 = 3, arr[0] * 5 = 5
"""


class Solution:
    def GetUglyNumber(self, index):
        if not index:
            return 0
        array = [1] * index
        nextindex = 1

        index2 = 0
        index3 = 0
        index5 = 0
        while nextindex < index:
            minval = min(array[index2] * 2, array[index3]
                         * 3, array[index5] * 5)
            array[nextindex] = minval

            while array[index2] * 2 <= array[nextindex]:
                index2 += 1
            while array[index3] * 3 <= array[nextindex]:
                index3 += 1
            while array[index5] * 5 <= array[nextindex]:
                index5 += 1
            nextindex += 1

        return array[index - 1]
