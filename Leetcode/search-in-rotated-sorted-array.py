# -*- coding: utf-8 -*-
# author='XuYingHao'


"""
假设按照升序排序的数组在预先未知的某个点上进行了旋转。
( 例如，数组 [0,1,2,4,5,6,7] 可能变为 [4,5,6,7,0,1,2] )。
搜索一个给定的目标值，如果数组中存在这个目标值，则返回它的索引，否则返回 -1 。
你可以假设数组中不存在重复的元素。
你的算法时间复杂度必须是 O(log n) 级别。

"""
"""
看到log n 就要想到二分查找.
"""


class Solution:
    def search(self, nums, target):
        """
        :type nums: List[int]
        :type target: int
        :rtype: int
        """
        nums_copy = nums.copy()
        nums = sorted(nums)
        length = len(nums)
        left = 0
        right = length - 1
        while left <= right:
            middle = (right + left) // 2
            if target < nums[middle]:
                right = middle - 1
            elif target > nums[middle]:
                left = middle + 1
            else:
                if nums[middle] == taret:
                    return nums_copy.index(target)

        return -1

s = Solution()
print(s.search([4,5,6,7,0,1,2],3))
