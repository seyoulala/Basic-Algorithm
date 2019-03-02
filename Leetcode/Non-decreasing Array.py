#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Date    : 2019-01-03 22:08:02
# @Author  : xuyinghao (xyh650209@163.com)
# @Link    : https://github.com/seyoulala/Basic-Algorithm
# @Version : $Id$


class Solution:
    def checkPossibility(self, nums):
        """
        :type nums: List[int]
        :rtype: bool
        """
        change = 0
        for i in range(len(nums) - 1):
            if nums[i] > nums[i + 1]:
                change += 1
                if change <= 1:
                    if i > 0:
                        if nums[i + 1] >= nums[i - 1]:
                            nums[i] = nums[i + 1]
                        else:
                            nums[i + 1] = nums[i]
                    else:
                        nums[i] = nums[i + 1]
                else:
                    return False
        return True


s = Solution()
print(s.checkPossibility([4, 2, 3]))
