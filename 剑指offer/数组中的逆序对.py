#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Date    : 2018-11-16 20:08:37
# @Author  : xuyinghao (xyh650209@163.com)
# @Link    : https://github.com/seyoulala/Basic-Algorithm
# @Version : $Id$


import random
import copy
class Solution:
	def InversePairs(self, arr):
		if arr is None or len(arr) < 2:
			return 0
		return self.mergeSort(arr, 0, len(arr) - 1)

	def mergeSort(self, arr, l, r):
		if l == r:
			return 0
		# 防止l+r溢出
		mid = l + ((r - l) >> 1)
		return self.mergeSort(arr, l, mid) + self.mergeSort(arr, mid + 1, r) + self.merge(arr, l, mid, r)

	def merge(self, arr, l, mid, r):
		# 定义一个辅助数组
		helps = [0] * (r - l + 1)
		i = 0
		p1 = l
		p2 = mid + 1
		res = 0
		while p1 <= mid and p2 <= r:
			res += (r - p2 + 1) if arr[p1] > arr[p2] else 0
			if arr[p1] > arr[p2]:
				helps[i] = arr[p1]
				p1 += 1
			else:
				helps[i] = arr[p2]
				p2 += 1
			i += 1

		while p1 <= mid:
			helps[i] = arr[p1]
			i += 1
			p1 += 1

		while p2 <= r:
			helps[i] = arr[p2]
			p2 += 1
			i += 1
		# 将数组拷贝回到原来额数组
		k = 0
		while l <= r:
			arr[l] = helps[k]
			l += 1
			k += 1
		return res

#对数器

	#首先写一个绝对正确的方法
	def comparator(self,arr):
		if arr is None or len(arr)<2:
			return 0
		res = 0
		length = len(arr)
		for i in range(1,length):
			for j in range(i):
				if arr[j]>arr[i]:
					res+=1
		return res

	#产生一个随机数发生器
	def generateRandomArray(self,maxSize,maxValue):
		arr = [0]*maxSize
		for i in range(maxSize):
			arr[i] = random.randint(-maxValue,maxValue)
		return  arr

	def isEqual(self,arr1,arr2):
		if (arr1 == None and arr2 !=None) or (arr1!=None and arr2==None):
			return  False
		if arr1==arr2==None:
			return  True
		if len(arr1) !=len(arr2):
			return  False

		for i in range(len(arr1)):
			if arr1[i]!=arr2[i]:
				return  False

		return True

	def printArray(self,arr):
		if arr==None:
			return
		for i in range(len(arr)):
			print(arr[i]+" ")

	def main(self):
		testTime=50000
		maxSize = 100
		maxValue = 100
		succeed=True
		for i in range(testTime):
			arr1 = self.generateRandomArray(maxSize,maxValue)
			arr2 = copy.deepcopy(arr1)
			if  self.InversePairs(arr1)!=self.comparator(arr2):
				succeed=False
				print(arr1)
				print(arr2)
				break
		print("Nice!" if succeed else "Fucking")


s = Solution()
s.main()
