#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Author  : xuyinghao
class Solution:
    def hasPath(self, matrix, rows, cols, path):
        # write code here
        if not matrix:
            return False
        if not path:
            return True
        x = [list(matrix[cols * i:cols * i + cols]) for i in range(rows)]
        for i in range(rows):
            for j in range(cols):
                if self.exit_help(x, i, j, path):
                    return True
        return False

    def exit_help(self, matrix, i, j, path):
        if matrix[i][j] == path[0]:
            if not path[1:]:
                return True
            matrix[i][j] = ''
            if i > 0 and self.exit_help(matrix, i - 1, j, path[1:]):
                return True
            if i < len(matrix) - 1 and self.exit_help(matrix, i + 1, j, path[1:]):
                return True
            if j > 0 and self.exit_help(matrix, i, j - 1, path[1:]):
                return True
            if j < len(matrix[0]) - 1 and self.exit_help(matrix, i, j + 1, path[1:]):
                return True
            matrix[i][j] = path[0]
            return False
        return False


s = Solution()
ifTrue = s.hasPath("ABCESFCSADEE", 3, 4, "ABCCED")
ifTrue2 = s.hasPath("ABCEHJIGSFCSLOPQADEEMNOEADIDEJFMVCEIFGGS", 5, 8, "SGGFIECVAASABCEHJIGQEM")
print(ifTrue2)