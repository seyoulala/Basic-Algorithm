# -*- coding: utf-8 -*-
# author='XuYingHao'


"""
假设按照升序排序的数组在预先未知的某个点上进行了旋转。
( 例如，数组 [0,0,1,2,2,5,6] 可能变为 [2,5,6,0,0,1,2] )。
编写一个函数来判断给定的目标值是否存在于数组中。若存在返回 true，否则返回 false。
示例 1:

输入: nums = [2,5,6,0,0,1,2], target = 0
输出: true

"""

"""
排序好的数组，找到某个数适合二分查找
"""


class Solution:
	def search(self, nums, target):
		"""
		:type nums: List[int]
		:type target: int
		:rtype: bool
		"""
		# length = len(nums)
		# for i in range(length - 1):
		# 	if nums[i] > nums[i + 1]:
		# 		nums[:] = nums[i + 1:] + nums[:i + 1]

		length = len(nums)
		nums = sorted(nums)
		left = 0
		right = length - 1
		while left <= right:
			middle = (right + left) // 2
			if target < nums[middle]:
				right = middle - 1
			elif target > nums[middle]:
				left = middle + 1
			else:
				if nums[middle] == target:
					return True

		return False

s = Solution()
print(s.search([2,5,6,0,0,1,2],0))