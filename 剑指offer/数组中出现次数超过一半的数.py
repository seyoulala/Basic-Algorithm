#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Author  : xuyinghao

"""
数组中有一个数字出现的次数超过数组长度的一半，请找出这个数字。例如输入一个长度为9的数组{1,2,3,2,2,2,5,4,2}。
由于数字2在数组中出现了5次，超过数组长度的一半，因此输出2。如果不存在则输出0。
"""
"""
思路1：哈希表法
用一个字典保存数组中出现的数以及其出现的次数,遍历其keys，判断value是否大于长度的一半。时间复杂度O(n)

思路2：第二种思路根据数组的特点，出现次数超过一半的数，他出现的次数比其他数字出现的总和还要多，因此可以最开始保存两个数值：
数组中的一个数字以及它出现的次数，然后遍历，如果下一个数字等于这个数字，那么次数加一，如果不等，次数减一，当次数等于0的时候，
在下一个数字的时候重新复制新的数字以及出现的次数置为1，直到进行到最后，
然后再验证最后留下的数字是否出现次数超过一半，因为可能前面的次数依次抵消掉，最后一个数字就直接是保留下来的数字，但是出现次数不一定超过一半。
"""


class Solution:
    #哈希表
    def MoreThanHalfNum_Solution(self, numbers):
        # write code here
        res  ={}
        m = len(numbers)/2
        for i in numbers:
            if i not in res.keys():
                res[i] =1
            else:
                res[i]+=1
        for key in res.keys():
            if res[key]>m:
                return int(key)
        return 0
    #方法二
    def check_mid(self,numbers,length,number):
        time=0
        for i in numbers:
            if i==number:
                time+=1
        if time > (length/2):
            return True
        else:
            return False

    def MoreThanHalfNum_Solution_1(self, numbers):
        length = len(numbers)
        times = 1
        number = numbers[0]
        for i in range(1,length):
            if times ==0:
                number = numbers[i]
                times =1
            elif numbers[i] == number:
                times +=1
            else:
                times -=1
        if self.check_mid(numbers,length,number):
            return number
        return 0


s = Solution()
num = [1,2,3,2,2,2,5,4,2]
num1 = [4,1,4,1,2,4]
print(s.MoreThanHalfNum_Solution_1(num1))




