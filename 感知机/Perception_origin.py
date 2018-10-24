#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Author  : xuyinghao

import  numpy as np
import  random
import  matplotlib.pyplot as plt
def sign(x):
    if x>0:
        return 1
    else:
        return -1


def perception(data,learning_rate):
    #初始化参数w,b
    weight = [0,0]
    b = 0

    for i in range(100):
        train_data = random.choice(data) # 从训练集中随机取一个点
        loss = (weight[0]*train_data[0] + weight[1]*train_data[1] + b)*train_data[2]

        if sign(loss) == -1:
            weight[0] = weight[0] + learning_rate*train_data[2]*train_data[0]
            weight[1] = weight[1] + learning_rate*train_data[2]*train_data[1]
            b = b + learning_rate*train_data[2]


    return weight,b

def plot(data,w,b):
    plt.figure()
    x1 =  np.linspace(0,10,100)
    x2 = -1*(w[0]*x1 +b) /(w[1]+1e-10)
    plt.plot(x1,x2,color='r',label='y1')
    for i in range(len(data)):
        if data[i][-1] ==1:
            plt.scatter(data[i][0],data[i][1],s=50,c=data[i][-1],label='1',marker='x')
        else:
            plt.scatter(data[i][0],data[i][1],s=50,c=data[i][-1],label='0')
    plt.legend(loc='best')
    plt.show()






if __name__ =='__main__':
    train_data = [[3,3,1],
                  [4,3,1],
                  [1,1,-1]]

    w,b = perception(train_data,1)
    plot(train_data,w,b)
