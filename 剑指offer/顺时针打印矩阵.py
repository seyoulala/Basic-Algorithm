#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Author  : xuyinghao

import  numpy as np

class Solution:
    def spiralOrder(self, matrix):
        if len(matrix)==0:
            return []

        top = 0
        left = 0
        right = len(matrix[0])-1
        bottom = len(matrix)-1
        result = []
        #逆时针打印矩阵
        while left<=right and top<=bottom:
            for i in range(left,right+1):
                result.append(matrix[top][i])
            #从上往下打印
            for i in range(top+1,bottom+1):
                result.append(matrix[i][right])
            #从右往左边打印
            if top !=bottom:
                for i in range(left,right)[::-1]:
                    result.append(matrix[bottom][i])
            if left!=right:
                for i in range(top+1,bottom)[::-1]:
                    result.append(matrix[i][left])

            left+=1
            right-=1
            top+=1
            bottom-=1

        return  result

test_data = np.arange(1,17).reshape(4,4)
s= Solution()
print(test_data)
print(s.PrintMatrix(test_data))
