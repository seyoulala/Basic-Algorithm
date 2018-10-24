#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Author  : xuyinghao

import  numpy as np

class Solution:

    def PrintMatrix(self,Matrxi):
        if len(Matrxi)<=0:
            pass

        left = 0
        right = Matrxi.shape[1]
        top = 0
        bottom = Matrxi.shape[0]
        result = []
        while left<=right and top <= bottom:
            #从左向右遍历
            for i in range(left,right):
                result.append(Matrxi[top][i])
            #从上到下遍历
            for i in range(top+1,bottom):
                result.append(Matrxi[i][right-1])
            #如果要从右边到左边,肯定top！=bottom
            if top != bottom:
                for i in range(left,right-1)[::-1]:
                    result.append(Matrxi[bottom-1][i])
            #如果要从下到上，肯定从右到左边走过了，那么left！=right
            if left != right:
                for i in range(top+1,bottom-1)[::-1]:
                    result.append(Matrxi[i][left])
            left +=1
            right -=1
            top +=1
            bottom -=1
        return result


test_data = np.arange(1,17).reshape(4,4)
s= Solution()
print(test_data)
print(s.PrintMatrix(test_data))