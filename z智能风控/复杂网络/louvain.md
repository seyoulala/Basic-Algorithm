### Fast unfolding of communities in large networks

Louvain是基于模块度（Modularity）的社区发现算法，通过模块度来衡量一个社区的紧密程度。如果一个节点加入到某一社区中会使得该社区的模块度有最大程度的增加，则该节点就应当属于该社区。如果加入其它社区后没有使其模块度增加，则留在自己当前社区中。

## 1.1 模块度

**<1>模块度公式**

模块度Q的物理意义：社区内节点的连边数与随机情况下的边数之差，定义函数如下：
$$
Q = \frac{1}{2m} \times \sum_{i,j}[A_{ij} - \frac{k_ik_j}{2m}]\delta(c_i,c_j)
$$

$$
\delta(u,v) = \begin{cases} 1 &\text{when u == v} \\ 0 &\text {}else \end{cases}
$$

其中

![A_ij](https://math.jianshu.com/math?formula=A_ij) :节点 i 和节点 j 之间边的权重

![K_i](https://math.jianshu.com/math?formula=K_i) ：所有与节点i相连的边的权重之和

![C_i](https://math.jianshu.com/math?formula=C_i) ：节点i所属的社区

![m](https://math.jianshu.com/math?formula=m) ： 图中所有边的权重之和

**<2> 模块度公式变形**

在此公式中，只有节点i和节点j属于同一社区，公式才有意义，所以该公式是衡量的某一社区内的紧密度。对于该公式的简化变形如下：
$$
Q = \frac{1}{2m} \times \sum_{i,j}[A_{i,j} - \frac{k_ik_j}{2m}]\delta(c_i,c_j) \\ = \frac{1}{2m}[\sum_{i,j}A_{i,j} - \frac{\sum_ik_i \sum_jk_j}{2m}]\delta(c_i,c_j) \\ = \frac{1}{2m} \sum_c[\sum{in} - \frac{{\sum{tot}}^{2}}{2m}]
$$
（中间是将Σ移到括号中，第三行是符号的变换）

![\Sigma_{in}](https://math.jianshu.com/math?formula=%5CSigma_%7Bin%7D) 表示： 社区c内的边的权重之和

![\Sigma_{k_n}](https://math.jianshu.com/math?formula=%5CSigma_%7Bk_n%7D) 表示： 所有与社区c内节点相连的边的权重之和（因为i属于社区c）包括社区内节点与节点i的边和社区外节点与节点i的边。

![\Sigma_{k_j}](https://math.jianshu.com/math?formula=%5CSigma_%7Bk_j%7D) 表示： 所有与社区c内节点相连的边的权重之和（因为j属于社区c）包括社区内节点与节点j的边和社区外节点与节点j的边。

![\Sigma_{tot}](https://math.jianshu.com/math?formula=%5CSigma_%7Btot%7D) 代替![\Sigma_{k_i}](https://math.jianshu.com/math?formula=%5CSigma_%7Bk_i%7D) 和 ![\Sigma_{k_j}](https://math.jianshu.com/math?formula=%5CSigma_%7Bk_j%7D)。（即社区c内边权重和 + 社区c与其他社区连边的权重和）

**<3> 求解模块度变化**

在Louvain算法中不需要求每个社区具体的模块度，只需要比较社区中加入某个节点之后的模块度变化，所以需要求解△Q。将节点i分配到某一社区中，社区的模块度变化为：
$$
\Delta{Q} = [\frac{\sum_{in} + k_{i,in}}{2m} -({\frac{\sum_{tot} + k_i}{2m}})^{2}] - [\frac{\sum_{in}}{2m} - (\frac{\sum_{tot}}{2m})^{2} - (\frac{k_i}{2m})^{2}] \\~\\ = [\frac{k_{i,in}}{2m} - \frac{\sum_{tot}k_i}{2m^2}]
$$
其中

![k_{i,in}](https://math.jianshu.com/math?formula=k_%7Bi%2Cin%7D) ： 社区内所有节点与节点i连边权重之和（对应新社区的实际内部权重和乘以2，因为Ki_in 对于社区内所有的顶点i，每条边其实被计算了两次）

![K_i](https://math.jianshu.com/math?formula=K_i)   ： 所有与节点 i 相连的边的权重之和

$\frac{1}{2m}$该公式把公共系数提出来，$[k_{i,in} - \sum_{tot} \times \frac{k_i}{m}]实现时只需求即可$。



## 1.2 算法基本流程

Louvain算法包括两个阶段，其流程就是这两个阶段的迭代过程。

**阶段一：**不断地遍历网络图中的节点，通过比较节点给每个邻居社区带来的模块度的变化，将单个节点加入到能够使Modulaity模块度有最大增量的社区中。
 （比如节点v分别加入到社区A、B、C中，使得三个社区的模块度增量为-1， 1， 2， 则节点v最终应该加入到社区C中）

**阶段二：**对第一阶段进行处理，将属于同一社区的顶点合并为一个大的超点重新构造网络图，即一个社区作为图的一个新的节点。此时两个超点之间边的权重是两个超点内所有原始顶点之间相连的边权重之和，即两个社区之间的边权重之和。（这里不好理解，以图辅助理解）

下面是对第一二阶段的实例介绍。

![img](/Volumes/disk2/Basic-Algorithm/z智能风控/img/louvain.png)



第一阶段遍历图中节点加入到其所属社区中，得到中间的图，形成四个社区；

第二节点对社区内的节点进行合并成一个超级节点，社区节点有自连边，其权重为社区内部所有节点间相连的边的权重之和的2倍，社区之间的边为两个社区间顶点跨社区相连的边的权重之和，如红色社区和浅绿色社区之间通过（8,11）、（10，11）、（10,13）相连，所以两个社区之间边的权重为3。

*注：为什么社区内的权重为所有内部结点连边权重的两倍，因为Kin的概念是社区内所有节点与节点i的连边和，在计算某一社区的Kin时，实际上每条边都被其两端的顶点计算了一次，一共被计算了两次。*

整个Louvain算法就是不断迭代第一阶段和第二阶段，直到算法稳定（图的模块度不再变化）或者到达最大迭代次数



