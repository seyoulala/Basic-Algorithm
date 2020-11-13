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



顶端的图是原始的Graph，中间的图表示的是状态向量和输出向量计算更新的图，底部的图表示的是等价的经过t次状态向量计算的图。

## 学习算法

GNN的学习就是估计参数 ![[公式]](https://www.zhihu.com/equation?tex=%5Cboldsymbol%7Bw%7D) ，使得函数 ![[公式]](https://www.zhihu.com/equation?tex=%5Cvarphi_%7B%5Cboldsymbol%7Bw%7D%7D) 能够近似估计训练集

![[公式]](https://www.zhihu.com/equation?tex=%5Cmathcal%7BL%7D%3D%5Cleft%5C%7B%5Cleft%28%5Cboldsymbol%7BG%7D_%7Bi%7D%2C+n_%7Bi%2C+j%7D%2C+%5Cboldsymbol%7Bt%7D_%7Bi%2C+j%7D%5Cright%29%7C+%5Cboldsymbol%7BG%7D_%7Bi%7D%3D%5Cleft%28%5Cboldsymbol%7BN%7D_%7Bi%7D%2C+%5Cboldsymbol%7BE%7D_%7Bi%7D%5Cright%29+%5Cin+%5Cmathcal%7BG%7D%5Cright.%3Bn_%7Bi%2C+j%7D+%5Cin+%5Cboldsymbol%7BN%7D_%7Bi%7D+%3B+%5Cboldsymbol%7Bt%7D_%7Bi%2C+j%7D+%5Cin+%5Cmathbb%7BR%7D%5E%7Bm%7D%2C+1+%5Cleq+i+%5Cleq+p%2C+1+%5Cleq+j+%5Cleq+q_%7Bi%7D+%5C%7D+%5C%5C) 

其中， ![[公式]](https://www.zhihu.com/equation?tex=q_i) 表示在图 ![[公式]](https://www.zhihu.com/equation?tex=G_%7Bi%7D) 中监督学习的节点个数，$t_{ij}$表示$G_i$中第j个节点的标签值。对于graph-focused的任务，需要增加一个特殊的节点，该节点用来作为目标节点，这样，graph-focused任务和node-focused任务都能统一到节点预测任务上，学习目标可以是最小化如下二次损失函数

![[公式]](https://www.zhihu.com/equation?tex=e_%7B%5Cboldsymbol%7Bw%7D%7D%3D%5Csum_%7Bi%3D1%7D%5E%7Bp%7D+%5Csum_%7Bj%3D1%7D%5E%7Bq_%7Bi%7D%7D%5Cleft%28%5Cboldsymbol%7Bt%7D_%7Bi%2C+j%7D-%5Cvarphi_%7B%5Cboldsymbol%7Bw%7D%7D%5Cleft%28%5Cboldsymbol%7BG%7D_%7Bi%7D%2C+n_%7Bi%2C+j%7D%5Cright%29%5Cright%29%5E%7B2%7D+%5C%5C) 

优化算法基于随机梯度下降的策略，优化步骤按照如下几步进行

- 按照迭代方程迭代 ![[公式]](https://www.zhihu.com/equation?tex=T) 次得到 ![[公式]](https://www.zhihu.com/equation?tex=x_%7Bn%7D%28t%29) ，此时接近不动点解： ![[公式]](https://www.zhihu.com/equation?tex=%5Cboldsymbol%7Bx%7D%28T%29+%5Capprox+%5Cboldsymbol%7Bx%7D) 。
- 计算参数权重的梯度 ![[公式]](https://www.zhihu.com/equation?tex=%5Cpartial+e_%7B%5Cboldsymbol%7Bw%7D%7D%28T%29+%2F+%5Cpartial+%5Cboldsymbol%7Bw%7D) 。
- 使用该梯度来更新权重 ![[公式]](https://www.zhihu.com/equation?tex=%5Cboldsymbol%7Bw%7D) 。





## Transition和Output函数实现

在GNN中，函数 ![[公式]](https://www.zhihu.com/equation?tex=g_%7B%5Cboldsymbol%7Bw%7D%7D) 不需要满足特定的约束，直接使用多层前馈神经网络，对于函数 ![[公式]](https://www.zhihu.com/equation?tex=f_%7B%5Cboldsymbol%7Bw%7D%7D) ，则需要着重考虑，因为 ![[公式]](https://www.zhihu.com/equation?tex=f_%7B%5Cboldsymbol%7Bw%7D%7D) 需要满足压缩映射的条件，而且与不动点计算相关。下面提出两种神经网络和不同的策略来满足这些需求

**1. Linear(nonpositional) GNN**：

对于节点状态的计算，将方程 ![[公式]](https://www.zhihu.com/equation?tex=%5Cbegin%7Barray%7D%7Bl%7D%7B%5Cboldsymbol%7Bx%7D_%7Bn%7D%3Df_%7B%5Cboldsymbol%7Bw%7D%7D%5Cleft%28%5Cboldsymbol%7Bl%7D_%7Bn%7D%2C+%5Cboldsymbol%7Bl%7D_%7B%5Cmathrm%7Bco%7D%5Bn%5D%7D%2C+%5Cboldsymbol%7Bx%7D_%7B%5Cmathrm%7Bne%7D%5Bn%5D%7D%2C+%5Cboldsymbol%7Bl%7D_%7B%5Cmathrm%7Bne%7D%5Cleft%5Bn%5Cright%5D%7D%5Cright%29%7D+%5C%7D%5Cend%7Barray%7D) 中的 ![[公式]](https://www.zhihu.com/equation?tex=f_%7B%5Cboldsymbol%7Bw%7D%7D) 改成如下形式
 ![[公式]](https://www.zhihu.com/equation?tex=%5Cboldsymbol%7Bx%7D_%7Bn%7D%3D%5Csum_%7Bu+%5Cin+%5Ctext+%7B+ne+%7D+%7C+n+%5D%7D+h_%7B%5Cboldsymbol%7Bw%7D%7D%5Cleft%28%5Cboldsymbol%7Bl%7D_%7Bn%7D%2C+%5Cboldsymbol%7Bl%7D_%7B%28n%2C+u%29%7D%2C+%5Cboldsymbol%7Bx%7D_%7Bu%7D%2C+%5Cboldsymbol%7Bl%7D_%7Bu%7D%5Cright%29%2C+%5Cquad+n+%5Cin+%5Cboldsymbol%7BN%7D+%5C%5C) 

相当于是对节点 ![[公式]](https://www.zhihu.com/equation?tex=n) 的每一个邻居节点使用 ![[公式]](https://www.zhihu.com/equation?tex=h_%7B%5Cboldsymbol%7Bw%7D%7D) ，并将得到的值求和来作为节点 ![[公式]](https://www.zhihu.com/equation?tex=n) 的状态。

由此，对上式中的函数 ![[公式]](https://www.zhihu.com/equation?tex=h_%7B%5Cboldsymbol%7Bw%7D%7D) 按照如下方式实现

![[公式]](https://www.zhihu.com/equation?tex=h_%7B%5Cboldsymbol%7Bw%7D%7D%5Cleft%28%5Cboldsymbol%7Bl%7D_%7Bn%7D%2C+%5Cboldsymbol%7Bl%7D_%7B%28n%2C+%5Cmathfrak%7Ba%7D%29%7D%2C+%5Cboldsymbol%7Bx%7D_%7Bu%7D%2C+%5Cboldsymbol%7Bl%7D_%7Bu%7D%5Cright%29+%3D+%5Cboldsymbol%7BA%7D_%7Bn%2C+u%7D+%5Cboldsymbol%7Bx%7D_%7Bu%7D%2B%5Cboldsymbol%7Bb%7D_%7Bn%7D+%5C%5C) 

其中，向量 ![[公式]](https://www.zhihu.com/equation?tex=%5Cboldsymbol%7Bb%7D_%7Bn%7D+%5Cin+%5Cmathbb%7BR%7D%5E%7Bs%7D) ，矩阵 ![[公式]](https://www.zhihu.com/equation?tex=%5Cboldsymbol%7BA%7D_%7Bn%2C+u%7D+%5Cin+%5Cmathbb%7BR%7D%5E%7Bs+%5Ctimes+s%7D) 定义为两个前向神经网络的输出。更确切地说，令产生矩阵 ![[公式]](https://www.zhihu.com/equation?tex=%5Cboldsymbol%7BA%7D_%7Bn%2C+u%7D) 的网络为*transition network*，产生向量 ![[公式]](https://www.zhihu.com/equation?tex=%5Cboldsymbol%7Bb%7D_%7Bn%7D) 的网络为*forcing network*

transition network表示为 ![[公式]](https://www.zhihu.com/equation?tex=%5Cphi_%7B%5Cboldsymbol%7Bw%7D%7D) 

![[公式]](https://www.zhihu.com/equation?tex=%5Cphi_%7B%5Cboldsymbol%7Bw%7D%7D+%3A+%5Cmathbb%7BR%7D%5E%7B2+l_%7BN%7D%2Bl_%7BE%7D%7D+%5Crightarrow+%5Cmathbb%7BR%7D%5E%7Bs%5E%7B2%7D%7D+%5C%5C) 

forcing network表示为 ![[公式]](https://www.zhihu.com/equation?tex=%5Crho_%7B%5Cboldsymbol%7Bw%7D%7D) 

![[公式]](https://www.zhihu.com/equation?tex=%5Crho_%7B%5Cboldsymbol%7Bw%7D%7D+%3A+%5Cmathbb%7BR%7D%5E%7Bl_%7BN%7D%7D+%5Crightarrow+%5Cmathbb%7BR%7D%5E%7Bs%7D+%5C%5C) 

由此，可以定义 ![[公式]](https://www.zhihu.com/equation?tex=%5Cboldsymbol%7BA%7D_%7Bn%2C+u%7D) 和 ![[公式]](https://www.zhihu.com/equation?tex=%5Cboldsymbol%7Bb%7D_%7Bn%7D) 

![[公式]](https://www.zhihu.com/equation?tex=%5Cbegin%7Baligned%7D+%5Cboldsymbol%7BA%7D_%7B%5Cboldsymbol%7Bn%7D%2C+%5Cboldsymbol%7Bu%7D%7D+%26%3D%5Cfrac%7B%5Cmu%7D%7Bs%7C%5Coperatorname%7Bne%7D%5Bu%5D%7C%7D+%5Ccdot+%5Cboldsymbol%7B%5CXi%7D+%5C%5C+%5Cboldsymbol%7Bb%7D_%7B%5Cboldsymbol%7Bw%7D%7D+%26%3D%5Crho_%7B%5Cboldsymbol%7Bw%7D%7D%5Cleft%28%5Cboldsymbol%7Bl%7D_%7Bn%7D%5Cright%29+%5Cend%7Baligned%7D+%5C%5C) 

其中， ![[公式]](https://www.zhihu.com/equation?tex=%5Cmu+%5Cin%280%2C1%29) ， ![[公式]](https://www.zhihu.com/equation?tex=%5CXi%3D%5Coperatorname%7Bresize%7D%5Cleft%28%5Cphi_%7B%5Cboldsymbol%7Bw%7D%7D%5Cleft%28%5Cboldsymbol%7Bl%7D_%7Bn%7D%2C+%5Cboldsymbol%7Bl%7D_%7B%28n%2C+u%29%7D%2C+%5Cboldsymbol%7Bl%7D_%7Bu%7D%5Cright%29%5Cright%29) ， ![[公式]](https://www.zhihu.com/equation?tex=%5Ctext%7Bresize%7D%28%5Ccdot%29) 表示将 ![[公式]](https://www.zhihu.com/equation?tex=s%5E2) 维的向量整理(reshape)成 ![[公式]](https://www.zhihu.com/equation?tex=s%5Ctimes%7Bs%7D) 的矩阵，也就是说，将transition network的输出整理成方形矩阵，然后乘以一个系数就得到 ![[公式]](https://www.zhihu.com/equation?tex=%5Cboldsymbol%7BA%7D_%7Bn%2C+u%7D) 。 ![[公式]](https://www.zhihu.com/equation?tex=%5Cboldsymbol%7Bb%7D_%7Bn%7D) 就是forcing network的输出。

在这里，假定 ![[公式]](https://www.zhihu.com/equation?tex=%5Cleft%5C%7C%5Cphi_%7B%5Cboldsymbol%7Bw%7D%7D%5Cleft%28%5Cboldsymbol%7Bl%7D_%7Bn%7D%2C+%5Cboldsymbol%7Bl%7D_%7B%28%5Cboldsymbol%7Bn%7D%2C+%5Cboldsymbol%7Bu%7D%29%7D%2C+%5Cboldsymbol%7Bl%7D_%7Bu%7D%5Cright%29%5Cright%5C%7C_%7B1%7D+%5Cleq+%5Cboldsymbol%7Bs%7D) ，这个可以通过设定transition function的激活函数来满足，比如设定激活函数为 ![[公式]](https://www.zhihu.com/equation?tex=tanh%28%29) 。在这种情况下， ![[公式]](https://www.zhihu.com/equation?tex=F_%7B%5Cboldsymbol%7Bw%7D%7D%28%5Cboldsymbol%7Bx%7D%2C+%5Cboldsymbol%7Bl%7D%29%3D%5Cboldsymbol%7BA%7D+%5Cboldsymbol%7Bx%7D%2B%5Cboldsymbol%7Bb%7D) ， ![[公式]](https://www.zhihu.com/equation?tex=%5Cboldsymbol%7BA%7D) 和 ![[公式]](https://www.zhihu.com/equation?tex=%5Cboldsymbol%7Bb%7D) 分别是 ![[公式]](https://www.zhihu.com/equation?tex=%5Cboldsymbol%7BA%7D_%7Bn%2C+u%7D) 的块矩阵形式和 ![[公式]](https://www.zhihu.com/equation?tex=%5Cboldsymbol%7Bb%7D_%7Bn%7D) 的堆叠形式，通过简单的代数运算可得

![[公式]](https://www.zhihu.com/equation?tex=%5Cbegin%7Baligned%7D%5Cleft%5C%7C%5Cfrac%7B%5Cpartial+F_%7B%5Cboldsymbol%7Bw%7D%7D%7D%7B%5Cpartial+%5Cboldsymbol%7Bx%7D%7D%5Cright%5C%7C_%7B1%7D+%26%3D%5C%7C%5Cboldsymbol%7BA%7D%5C%7C_%7B1%7D+%5Cleq+%5Cmax+_%7Bu+%5Cin+%5Cboldsymbol%7BN%7D%7D%5Cleft%28%5Csum_%7Bn+%5Cin+%5Coperatorname%7Bne%7D%5Bu%5D%7D%5Cleft%5C%7C%5Cboldsymbol%7BA%7D_%7Bn%2C+u%7D%5Cright%5C%7C_%7B1%7D%5Cright%29+%5C%5C+%26+%5Cleq+%5Cmax+_%7Bu+%5Cin+N%7D%5Cleft%28%5Cfrac%7B%5Cmu%7D%7Bs%7C%5Coperatorname%7Bne%7D%5Bu%5D%7C%7D+%5Ccdot+%5Csum_%7Bn+%5Cin+%5Cmathrm%7Bne%7D%5Bu%5D%7D%5C%7C%5Cmathbf%7B%5CXi%7D%5C%7C_%7B1%7D%5Cright%29+%5Cleq+%5Cmu+%5Cend%7Baligned%7D+%5C%5C) 

该式表示 ![[公式]](https://www.zhihu.com/equation?tex=F_%7B%5Cboldsymbol%7Bw%7D%7D) 对于任意的参数 ![[公式]](https://www.zhihu.com/equation?tex=%5Cboldsymbol%7Bw%7D) 是一个压缩映射。

> 矩阵 ![[公式]](https://www.zhihu.com/equation?tex=M) 的1-norm定义为
>  ![[公式]](https://www.zhihu.com/equation?tex=%5C%7CM%5C%7C_%7B1%7D%3D%5Cmax+_%7Bj%7D+%5Csum_%7Bi%7D%5Cleft%7Cm_%7Bi%2C+j%7D%5Cright%7C+%5C%5C) 

**2. Nonelinear(nonpositional) GNN**：在这个结构中， ![[公式]](https://www.zhihu.com/equation?tex=h_%7B%5Cboldsymbol%7Bw%7D%7D) 通过多层前馈网络实现，但是，并不是所有的参数 ![[公式]](https://www.zhihu.com/equation?tex=%5Cboldsymbol%7Bw%7D) 都会被使用，因为同样需要保证 ![[公式]](https://www.zhihu.com/equation?tex=F_%7B%5Cboldsymbol%7Bw%7D%7D) 是一个压缩映射函数，这个可以通过惩罚项来实现

![[公式]](https://www.zhihu.com/equation?tex=e_%7B%5Cboldsymbol%7Bw%7D%7D%3D%5Csum_%7Bi%3D1%7D%5E%7Bp%7D+%5Csum_%7Bj%3D1%7D%5E%7Bq_%7Bi%7D%7D%5Cleft%28%5Cboldsymbol%7Bt%7D_%7Bi%2C+j%7D-%5Cvarphi_%7B%5Cboldsymbol%7Bw%7D%7D%5Cleft%28%5Cboldsymbol%7BG%7D_%7Bi%7D%2C+n_%7Bi%2C+j%7D%5Cright%29%5Cright%29%5E%7B2%7D%2B%5Cbeta+L%5Cleft%28%5Cleft%5C%7C%5Cfrac%7B%5Cpartial+F_%7B%5Cboldsymbol%7Bw%7D%7D%7D%7B%5Cpartial+%5Cboldsymbol%7Bx%7D%7D%5Cright%5C%7C%5Cright%29+%5C%5C) 

其中，惩罚项 ![[公式]](https://www.zhihu.com/equation?tex=L%28y%29) 在 ![[公式]](https://www.zhihu.com/equation?tex=y%3E%5Cmu) 时为 ![[公式]](https://www.zhihu.com/equation?tex=%28y-%5Cmu%29%5E2) ，在 ![[公式]](https://www.zhihu.com/equation?tex=y%5Cle%7B%5Cmu%7D) 时为0，参数 ![[公式]](https://www.zhihu.com/equation?tex=%5Cmu%5Cin%280%2C1%29) 定义为希望的 ![[公式]](https://www.zhihu.com/equation?tex=F_%7B%5Cboldsymbol%7Bw%7D%7D) 的压缩系数。

## 实验结果

论文将GNN模型在三个任务上进行了实验：子图匹配(subgraph matching)任务，诱变(mutagenesis)任务和网页排序(web page ranking)任务。在这些任务上使用linear和nonlinear的模型测试，其中nonlinear模型中的激活函数使用sigmoid函数。

子图匹配任务为在一个大图 ![[公式]](https://www.zhihu.com/equation?tex=G) 上找到给定的子图 ![[公式]](https://www.zhihu.com/equation?tex=S) (标记出属于子图的节点)，也就是说，函数 ![[公式]](https://www.zhihu.com/equation?tex=%5Ctau) 必须学习到，如果 ![[公式]](https://www.zhihu.com/equation?tex=n_%7Bi%2Cj%7D) 属于子图 ![[公式]](https://www.zhihu.com/equation?tex=S) ，那么 ![[公式]](https://www.zhihu.com/equation?tex=%5Ctau%28G_i%2Cn_%7Bi%2Cj%7D%29%3D1) ，否则， ![[公式]](https://www.zhihu.com/equation?tex=%5Ctau%28G_i%2Cn_%7Bi%2Cj%7D%29%3D-1) 。实验结果中，nonlinear模型的效果要好于linear模型的效果，两个模型都要比FNN模型效果更好。

诱变问题任务是对化学分子进行分类，识别出诱变化合物，采用二分类方法。实验结果是nonlinear效果较好，但不是最好。

网页排序任务是学会网页排序。实验表明虽然训练集只包含50个网页，但是仍然没有产生过拟合的现象。

