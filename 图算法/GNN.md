### GNN

GNN模型**基于信息传播机制，每一个节点通过相互交换信息来更新自己的节点状态，直到达到某一个稳定值**，GNN的输出就是在每个节点处，根据当前节点状态分别计算输出。有如下定义：

- 一个图 ![[公式]](https://www.zhihu.com/equation?tex=G) 表示为一对 ![[公式]](https://www.zhihu.com/equation?tex=%28%5Cboldsymbol%7BN%7D%2C+%5Cboldsymbol%7BE%7D%29) ，其中， ![[公式]](https://www.zhihu.com/equation?tex=%5Cboldsymbol%7BN%7D) 表示节点集合， ![[公式]](https://www.zhihu.com/equation?tex=%5Cboldsymbol%7BE%7D) 表示边集。
- ![[公式]](https://www.zhihu.com/equation?tex=ne%5Bn%5D) 表示节点 ![[公式]](https://www.zhihu.com/equation?tex=n) 的邻居节点集合。
-  ![[公式]](https://www.zhihu.com/equation?tex=co%5Bn%5D) 表示以节点 ![[公式]](https://www.zhihu.com/equation?tex=n) 为顶点的所有边集合。
- ![[公式]](https://www.zhihu.com/equation?tex=%5Cboldsymbol%7Bl%7D_%7Bn%7D+%5Cin+%5Cmathbb%7BR%7D%5E%7Bl_%7BN%7D%7D) 表示节点 ![[公式]](https://www.zhihu.com/equation?tex=n) 的特征向量。
-  ![[公式]](https://www.zhihu.com/equation?tex=%5Cboldsymbol%7Bl%7D_%7B%5Cleft%28n_%7B1%7D%2C+n_%7B2%7D%5Cright%29%7D+%5Cin+%5Cmathbb%7BR%7D%5E%7Bl_%7BE%7D%7D) 表示边 ![[公式]](https://www.zhihu.com/equation?tex=%28n_1%2Cn_2%29) 的特征向量。
-  ![[公式]](https://www.zhihu.com/equation?tex=%5Cboldsymbol%7Bl%7D) 表示所有特征向量叠在一起的向量。

假设存在一个图-节点对的集合 ![[公式]](https://www.zhihu.com/equation?tex=%5Cmathcal%7BD%7D%3D%5Cmathcal%7BG%7D+%5Ctimes+%5Cmathcal%7BN%7D) ， ![[公式]](https://www.zhihu.com/equation?tex=%5Cmathcal%7BG%7D) 表示图的集合， ![[公式]](https://www.zhihu.com/equation?tex=%5Cmathcal%7BN%7D) 表示节点集合，**图领域问题可以表示成一个有如下数据集的监督学习框架**

![[公式]](https://www.zhihu.com/equation?tex=%5Cmathcal%7BL%7D%3D%5Cleft%5C%7B%5Cleft%28%5Cboldsymbol%7BG%7D_%7Bi%7D%2C+n_%7Bi%2C+j%7D%2C+%5Cboldsymbol%7Bt%7D_%7Bi%2C+j%7D%5Cright%29%7C+%5Cboldsymbol%7BG%7D_%7Bi%7D%3D%5Cleft%28%5Cboldsymbol%7BN%7D_%7Bi%7D%2C+%5Cboldsymbol%7BE%7D_%7Bi%7D%5Cright%29+%5Cin+%5Cmathcal%7BG%7D%5Cright.%3Bn_%7Bi%2C+j%7D+%5Cin+%5Cboldsymbol%7BN%7D_%7Bi%7D+%3B+%5Cboldsymbol%7Bt%7D_%7Bi%2C+j%7D+%5Cin+%5Cmathbb%7BR%7D%5E%7Bm%7D%2C+1+%5Cleq+i+%5Cleq+p%2C+1+%5Cleq+j+%5Cleq+q_%7Bi%7D+%5C%7D+%5C%5C)
其中， ![[公式]](https://www.zhihu.com/equation?tex=n_%7Bi%2C+j%7D+%5Cin+%5Cboldsymbol%7BN%7D_%7Bi%7D) ​表示集合 ![[公式]](https://www.zhihu.com/equation?tex=%5Cboldsymbol%7BN%7D_%7Bi%7D+%5Cin+%5Cmathcal%7BN%7D) ​中的第​ ![[公式]](https://www.zhihu.com/equation?tex=j) 个节点，​ ![[公式]](https://www.zhihu.com/equation?tex=%5Cboldsymbol%7Bt%7D_%7Bi%2C+j%7D) 表示节点 ![[公式]](https://www.zhihu.com/equation?tex=n_%7Bij%7D) ​的期望目标(即标签)。

节点 ![[公式]](https://www.zhihu.com/equation?tex=n) 的状态用 ![[公式]](https://www.zhihu.com/equation?tex=%5Cboldsymbol%7Bx%7D_%7Bn%7D+%5Cin+%5Cmathbb%7BR%7D%5E%7Bs%7D) 表示，该节点的输出用 ![[公式]](https://www.zhihu.com/equation?tex=%5Cboldsymbol%7Bo%7D_%7B%5Cboldsymbol%7Bn%7D%7D) 表示， ![[公式]](https://www.zhihu.com/equation?tex=f_%7B%5Cboldsymbol%7Bw%7D%7D) 为*local transition function*， ![[公式]](https://www.zhihu.com/equation?tex=g_%7B%5Cboldsymbol%7Bw%7D%7D) 为*local output function*，那么 ![[公式]](https://www.zhihu.com/equation?tex=%5Cboldsymbol%7Bx%7D_%7Bn%7D) 和 ![[公式]](https://www.zhihu.com/equation?tex=%5Cboldsymbol%7Bo%7D_%7B%5Cboldsymbol%7Bn%7D%7D) 的更新方式如下

![[公式]](https://www.zhihu.com/equation?tex=%5Cbegin%7Barray%7D%7Bl%7D%7B%5Cboldsymbol%7Bx%7D_%7Bn%7D%3Df_%7B%5Cboldsymbol%7Bw%7D%7D%5Cleft%28%5Cboldsymbol%7Bl%7D_%7Bn%7D%2C+%5Cboldsymbol%7Bl%7D_%7B%5Cmathrm%7Bco%7D%5Bn%5D%7D%2C+%5Cboldsymbol%7Bx%7D_%7B%5Cmathrm%7Bne%7D%5Bn%5D%7D%2C+%5Cboldsymbol%7Bl%7D_%7B%5Cmathrm%7Bne%7D%5Cleft%5Bn%5Cright%5D%7D%5Cright%29%7D+%5C%5C+%7B%5Cboldsymbol%7Bo%7D_%7Bn%7D%3Dg_%7B%5Cboldsymbol%7Bw%7D%7D%5Cleft%28%5Cboldsymbol%7Bx%7D_%7Bn%7D%2C+%5Cboldsymbol%7Bl%7D_%7Bn%7D%5Cright%29%7D%5Cend%7Barray%7D%5Clabel%7Beq%3A30%7D+%5C%5C)

其中， ![[公式]](https://www.zhihu.com/equation?tex=F_%7B%5Cboldsymbol%7Bw%7D%7D) 为*global transition function*， ![[公式]](https://www.zhihu.com/equation?tex=G_%7B%5Cboldsymbol%7Bw%7D%7D) 为*global output function*，分别是 ![[公式]](https://www.zhihu.com/equation?tex=f_%7B%5Cboldsymbol%7Bw%7D%7D) 和 ![[公式]](https://www.zhihu.com/equation?tex=g_%7B%5Cboldsymbol%7Bw%7D%7D) 的叠加形式。

根据Banach的不动点理论，假设 ![[公式]](https://www.zhihu.com/equation?tex=F_%7B%5Cboldsymbol%7Bw%7D%7D) 是一个压缩映射函数，那么上面式子有唯一不动点解，而且可以通过迭代方式逼近该不动点

![[公式]](https://www.zhihu.com/equation?tex=%5Cboldsymbol%7Bx%7D%28t%2B1%29%3DF_%7B%5Cboldsymbol%7Bw%7D%7D%28%5Cboldsymbol%7Bx%7D%28t%29%2C+%5Cboldsymbol%7Bl%7D%29+%5C%5C)

其中， ![[公式]](https://www.zhihu.com/equation?tex=%5Cboldsymbol%7Bx%7D%28t%29) 表示 ![[公式]](https://www.zhihu.com/equation?tex=%5Cboldsymbol%7Bx%7D) 在第 ![[公式]](https://www.zhihu.com/equation?tex=t) 个迭代时刻的值，对于任意初值，迭代的误差是以指数速度减小的，使用迭代的形式写出状态和输出的更新表达式为

![[公式]](https://www.zhihu.com/equation?tex=%5Cbegin%7Baligned%7D+%5Cboldsymbol%7Bx%7D_%7Bn%7D%28t%2B1%29+%26%3Df_%7B%5Cboldsymbol%7Bw%7D%7D%5Cleft%28%5Cboldsymbol%7Bl%7D_%7Bn%7D%2C+%5Cboldsymbol%7Bl%7D_%7B%5Cmathrm%7Bco%7D%5Bn%5D%7D%2C+%5Cboldsymbol%7Bx%7D_%7B%5Cmathrm%7Bne%7D%5Bn%5D%7D%28t%29%2C+%5Cboldsymbol%7Bl%7D_%7B%5Cmathrm%7Bne%7D%5Bn%5D%7D%5Cright%29+%5C%5C+%5Cboldsymbol%7Bo%7D_%7Bn%7D%28t%29+%26%3Dg_%7B%5Cboldsymbol%7Bw%7D%7D%5Cleft%28%5Cboldsymbol%7Bx%7D_%7Bn%7D%28t%29%2C+%5Cboldsymbol%7Bl%7D_%7Bn%7D%5Cright%29%2C+%5Cquad+n+%5Cin+%5Cboldsymbol%7BN%7D+%5Cend%7Baligned%7D+%5C%5C)

GNN的信息传播流图以及等效的网络结构如下图所示

![img](https://pic1.zhimg.com/80/v2-8cafe036050da7a3a7d8f2fdd86b8ee8_hd.jpg)



对于