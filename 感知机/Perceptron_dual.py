#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Author  : xuyinghao

import  numpy as np
import  matplotlib.pyplot  as plt
import  random

def sign(x):
    if x>0:
        return 1
    else:
        return -1


def train(X,y,iter_num,learning_rate):
    # 初始化w,b α
    w = 0.0
    b = 0.0
    m = len(X)
    alpha = [0]*m
    train_data = np.array(X)
    y = np.array(y)
    #预先计算gram 矩阵 xi·xj内积
    gram = np.matmul(train_data,train_data.T)
    for idx in range(iter_num):
        tmp = 0
        i =  int(np.random.randint(0,m,size=1))
        yi = y[i]
        for j in range(m):
            tmp+= alpha[j] * y[j] *gram[i,j]
        tmp = tmp + b
        if (yi* tmp)<=0:
            alpha[i] = alpha[i] + learning_rate
            b = b + learning_rate *yi
    for i in range(m):
        w+=alpha[i]*y[i]*train_data[i]
    return w,b,alpha,gram

def plot_points(X,y,w,b):
    plt.figure()
    x1 = np.linspace(0,8,100)
    x2 = (-b-w[0]*x1)/(w[1]+1e-10) #防止除0出错
    X = np.array(X)
    y = np.array(y)
    plt.plot(x1,x2,color='r',label='y1')
    for i in range(len(y)):
        if y[i] == 1:
            t1 = plt.scatter(X[i][0],X[i][1],s=50,marker='^',c=y[i],label='1')
        else:
            t2 = plt.scatter(X[i][0], X[i][1], s=50, marker='x',c=y[i],label='0')
    plt.legend([t1,t2],[1,0],loc='best')
    plt.show()

if __name__ == '__main__':
    data_x = [[1,3],
            [2,2],
            [3,8],
            [2,6],
            [2,1],
            [4,1],
            [6,2],
            [7,3]]
    data_y = [1,1,1,1,-1,-1,-1,-1]
    w,b,alpha,gram = train(data_x,data_y,100,0.01)
    plot_points(data_x,data_y,w,b)


