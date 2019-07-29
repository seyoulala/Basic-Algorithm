#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Author  : xuyinghao

"""
在一个长度为n的数组里的所有数字都在0到n-1的范围内。
 数组中某些数字是重复的，但不知道有几个数字是重复的。
也不知道每个数字重复几次。请找出数组中任意一个重复的数字。
例如，如果输入长度为7的数组{2,3,1,0,2,5,3}，那么对应的输出是第一个重复的数字2
"""

"""
思路:方法1:首先对数组排序,然后查找重复的数字.时间复杂度可以是nlogn.方法2:建立一个哈希表,记录每个数字出现的次数,
时间复杂度为o(n),空间复杂度为O(n).方法三:因为所有数字都在0-n-1之间.如果数字没有重复,那么排序后数字i应该出现在
下标为i的地方.如果有重复数字,那么从头到尾扫描数组,交换数字i和下标为i处的数字,如果新交换的数字还不是他应该出现的位置，继续交换，
直至该处的数字m等于x下标m，如果在交换的过程中，第i处的位置数字等于第m处的数字，那么我们就找到了第一个重复的数字，记录这个数字，在从下一个位置继续扫描。

"""
class Solution:
    def duplicate(self,numbers):
        if len(numbers)<=0 or numbers is None:
            return -1
        for i in numbers:
            if i < 0 or i > len(numbers)-1:
                return -1
        rep_num =[]
        for i in range(len(numbers)):
            while numbers[i]!=i:
                if numbers[i] == numbers[numbers[i]]:
                    rep_num.append(numbers[i])
                    break
                else:
                    index = numbers[i]
                    numbers[i],numbers[index] = numbers[index],numbers[i]
        return  rep_num

s = Solution()

numbers = [2,3,1,0,2,5,3]
print(s.duplicate(numbers))