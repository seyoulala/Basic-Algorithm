#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Date    : 2019-01-03 21:39:43
# @Author  : xuyinghao (xyh650209@163.com)
# @Link    : https://github.com/seyoulala/Basic-Algorithm
# @Version : $Id$

"""
给定一个排序数组，你需要在原地删除重复出现的元素，使得每个元素只出现一次，返回移除后数组的新长度。
不要使用额外的数组空间，你必须在原地修改输入数组并在使用 O(1) 额外空间的条件下完成.
示例 1:

给定数组 nums = [1,1,2], 

函数应该返回新的长度 2, 并且原数组 nums 的前两个元素被修改为 1, 2。 

你不需要考虑数组中超出新长度后面的元素
"""
"""
思路:  双指针法
数组完成排序后，我们可以放置两个指针i和j，其中i是慢指针，j是快指针。只要nums[i]=nums[j],
我们就增加j来跳过重复项。当遇到nums[i]!=nums[j]时，必须将nums[j]的值复制到nums[i+1]，然后
递增i。重复以上过程，直到j到达末尾为止. 
"""


class Solution:
    def removeDuplicates(self, nums):
        """
        :type nums: List[int]
        :rtype: int
        """
        if len(nums) < 1:
            return 0
        slow = 0
        for i in range(1, len(nums)):
            if nums[slow] != nums[i]:
                slow += 1
                nums[slow] = nums[i]
        length = slow + 1
        return length
