### GCN

### 图卷积

![img](https://pic4.zhimg.com/80/v2-4013be2de0ecd8695e30b02b83a5bda3_hd.jpg)图4 图结构实例

### 图的定义

对于图，我们有以下特征定义：

对于图 ![[公式]](https://www.zhihu.com/equation?tex=G%3D%28V%2CE%29) ， ![[公式]](https://www.zhihu.com/equation?tex=V) 为节点的集合， ![[公式]](https://www.zhihu.com/equation?tex=E) 为边的集合，对于每个节点 ![[公式]](https://www.zhihu.com/equation?tex=i) ， 均有其特征 ![[公式]](https://www.zhihu.com/equation?tex=x_i) ，可以用矩阵 ![[公式]](https://www.zhihu.com/equation?tex=X_%7BN%2AD%7D) 表示。其中 ![[公式]](https://www.zhihu.com/equation?tex=N) 表示节点数， ![[公式]](https://www.zhihu.com/equation?tex=D) 表示每个节点的特征数，也可以说是特征向量的维度。

### 图卷积的形象化理解

在一头扎进图卷积公式之前，我们先从其他的角度理解一下这个操作的物理含义，有一个形象化的理解，我们在试图得到节点表示的时候，容易想到的最方便有效的手段就是利用它周围的节点，也就是它的邻居节点或者邻居的邻居等等，这种思想可以归结为一句话：

**图中的每个结点无时无刻不因为邻居和更远的点的影响而在改变着自己的状态直到最终的平衡，关系越亲近的邻居影响越大。**

实际上从邻居节点获取信息的思想在很多领域都有应用，例如word2vec，例如pagerank。关于这个点展开的内容文章[2]有非常详细的解释。

更加细节的如何从傅立叶变换到拉普拉斯算子到拉普拉斯矩阵的数学推倒可以转向博客[7]，为了避免数学功底没有那么强的初学者（比如我）被绕晕，我们先建立大纲，不要太发散。

### 图相关矩阵的定义

那么有什么东西来度量节点的邻居节点这个关系呢，学过图论的就会自然而然的想到邻接矩阵和拉普拉斯矩阵。举个简单的例子，对于下图中的左图（为了简单起见，举了无向图且边没有权重的例子）而言，它的度矩阵 ![[公式]](https://www.zhihu.com/equation?tex=D) ，邻接矩阵 ![[公式]](https://www.zhihu.com/equation?tex=A) 和拉普拉斯矩阵 ![[公式]](https://www.zhihu.com/equation?tex=L) 分别如下图所示，度矩阵 ![[公式]](https://www.zhihu.com/equation?tex=D) 只有对角线上有值，为对应节点的度，其余为0；邻接矩阵![[公式]](https://www.zhihu.com/equation?tex=A)只有在有边连接的两个节点之间为1，其余地方为0；拉普拉斯矩阵 ![[公式]](https://www.zhihu.com/equation?tex=L) 为 ![[公式]](https://www.zhihu.com/equation?tex=D-A) 。但需要注意的是，这是最简单的一种拉普拉斯矩阵，除了这种定义，还有接下来介绍的几种拉普拉斯矩阵。

![img](https://pic1.zhimg.com/80/v2-bc36fb838241c8f1e34b5d913d9b459c_hd.jpg)

图5 一个图的度矩阵，邻接矩阵和拉普拉斯矩阵



### 学习新特征

深度模型的本质是在学习特征的表示，对于图来说，我们也希望图模型能够从最开始的图特征出发学习到更抽象的特征表示。比如学习到了一个节点的高级特征表示，这个特征表示是根据图结构融合了邻居节点的特征学习得到的。然后这个特征表示就可以被用来进行节点的分类以及边的预测，那么图网络就是要学习新特征，特征的学习表示如下：
$$
H^{(k+1)} =f(H^{k},A)
$$
其中K表示网络的层数，H^k 表示的是第k层的特征，A表示邻接矩阵。

那么这个特征如何学习呢，可以从CNN中得到启发。

![img](https://pic1.zhimg.com/v2-61ffacb032934e1d971e07ebbc9f81ac_b.jpg)

CNN是这样学习新的特征表示的，首先对3x3的领域内特征进行变换(transform),使用的方法是$w_{i}x_{i}$,然后进行聚合操作(agg)，聚合的方法是$\sum_{i} {w_i}x_i$,类比到图学习表示，新的节点的特征是对邻居节点的特征进行变换然后进行聚合操作：
$$
H^{(k+1)} =f(H^{k},A) = \sigma(AH^{k}W^{k})
$$
其中$W^{k}$为权重矩阵，$\sigma$表示激活函数，其特征的学习方式也是对其领域内节点进行加权，然后进行求和来学习新的特征表示。

总结一下，我们可以将图的特征学习表示成如下步骤：

- 变换(transform)对当前的节点特征进行变换，这里就是简单的wx乘法形式
- 聚合(aggregate)聚合领域内的节点特征生成新的特征表示，这里就是简单的加法操作
- 激活(activate)对新生成的特征表示套上非线性函数增加其非线性。



### 图卷积的通式

任何一个图卷积层都可以写成这样一个非线性函数：

![[公式]](https://www.zhihu.com/equation?tex=H%5E%7Bl%2B1%7D+%3D+f%28H%5E%7Bl%7D%2CA%29)

![[公式]](https://www.zhihu.com/equation?tex=H%5E%7B0%7D%3DX) 为第一层的输入， ![[公式]](https://www.zhihu.com/equation?tex=X%5Cin+R%5E%7BN%2AD%7D) ， ![[公式]](https://www.zhihu.com/equation?tex=N) 为图的节点个数， ![[公式]](https://www.zhihu.com/equation?tex=D) 为每个节点特征向量的维度， ![[公式]](https://www.zhihu.com/equation?tex=A) 为邻接矩阵，不同模型的差异点在于函数 ![[公式]](https://www.zhihu.com/equation?tex=f) 的实现不同。

下面介绍几种具体的实现，但是每一种实现的参数大家都统称拉普拉斯矩阵。

### 实现一

![[公式]](https://www.zhihu.com/equation?tex=H%5E%7Bl%2B1%7D+%3D+%5Csigma+%28AH%5E%7Bl%7DW%5E%7Bl%7D%29)

其中 ![[公式]](https://www.zhihu.com/equation?tex=W%5E%7Bl%7D) 为第 ![[公式]](https://www.zhihu.com/equation?tex=l) 层的权重参数矩阵， ![[公式]](https://www.zhihu.com/equation?tex=%5Csigma%28%5Ccdot%29) 为非线性激活函数，例如ReLU。

这种思路是基于节点特征与其所有邻居节点有关的思想。邻接矩阵 ![[公式]](https://www.zhihu.com/equation?tex=A) 与特征 ![[公式]](https://www.zhihu.com/equation?tex=H) 相乘，等价于，某节点的邻居节点的特征相加。这样多层隐含层叠加，能利用多层邻居的信息。

但这样存在两个问题：

- **没有考虑节点自身对自己的影响,也就是在变换时没有考虑到自身节点的特征**
- **邻接矩阵**![[公式]](https://www.zhihu.com/equation?tex=A)**没有被规范化，**

因此实现二和实现三针对这两点进行了优化。

### 实现二

![[公式]](https://www.zhihu.com/equation?tex=H%5E%7Bl%2B1%7D+%3D+%5Csigma+%28LH%5E%7Bl%7DW%5E%7Bl%7D%29)

拉普拉斯矩阵 ![[公式]](https://www.zhihu.com/equation?tex=L%3DD-A) ，学名Combinatorial Laplacian，是针对实现一的问题1的改进：

- 引入了度矩阵，从而解决了没有考虑自身节点信息自传递的问题

  为什么拉普拉斯矩阵要定义成$L=D-A$这种形式？



 **2.3.1 Laplacian**

在数学中，拉普拉斯算子（Laplacian）是由欧几里得空间中的一个函数的梯度的散度给出的微分算子，通常有以下几种写法：![[公式]](https://www.zhihu.com/equation?tex=%5CDelta+%2C%5Cnabla%5E2%2C%5Cnabla+%5Ccdot+%5Cnabla)。所以对于任意函数 ![[公式]](https://www.zhihu.com/equation?tex=f) 来说，其拉普拉斯算子的定义为：

![[公式]](https://www.zhihu.com/equation?tex=%5CDelta+f+%3D+%5Cnabla%5E2+f+%3D+%5Cnabla+%5Ccdot+%5Cnabla+f+%5C%5C+%5C%5C)

这里引入了一个新的概念——散度，这里简单介绍下：

散度（Divergence）是向量分析的一个向量算子，将向量空间上的向量场（矢量场）对应到一个标量场。散度描述的是向量场里一个点是汇聚点还是发源点。值为正时表示该点为发源点，值为负时表示该点为汇聚点，值为零时表示该点无源。散度在物理上的含义可以理解为磁场、热源等。

回到正文，我们看下拉普拉斯算子在 n 维空间中的笛卡尔坐标系的数学定义：

![[公式]](https://www.zhihu.com/equation?tex=%5CDelta+f+%3D+%5Csum_%7Bi%3D1%7D%5En+%5Cfrac%7B%5Cpartial+%5E2+f%7D%7B%5Cpartial+x_i%5E2%7D+%5C%5C+%5C%5C)

数学表示为各个维度的二阶偏导数之和。

以一维空间为例：

![[公式]](https://www.zhihu.com/equation?tex=%5Cbegin%7Baligned%7D+%5Cfrac%7B%5Cpartial+%5E2+f%7D%7B%5Cpartial+x_i%5E2%7D+%26%3D+f%5E%7B%27%27%7D%28x%29+%5C%5C+%26%5Capprox+f%5E%7B%27%7D%28x%29+-+f%5E%7B%27%7D%28x-1%29+%5C%5C+%26%5Capprox+f%28x%2B1%29+-+f%28x%29+-%28f%28x%29+-+f%28x-1%29%29+%5C%5C+%26%3D+f%28x%2B1%29+%2B+f%28x-1%29%29+-+2f%28x%29++%5Cend%7Baligned%7D+%5C%5C+%5C%5C)

也就是说二阶导数近似于其二阶差分，可以理解为当前点对其在所有自由度上微扰之后获得的增益。这里自由度为 2，分别是 +1 和 -1 方向。

再以二维空间为例子：

![[公式]](https://www.zhihu.com/equation?tex=%5Cbegin%7Baligned%7D+%5CDelta+f%28x%2Cy%29+%26%3D+%5Cfrac%7B%5Cpartial+%5E2+f%7D%7B%5Cpartial+x%5E2%7D+%2B+%5Cfrac%7B%5Cpartial+%5E2+f%7D%7B%5Cpartial+y%5E2%7D++%5C%5C+%26%3D%5Bf%28x%2B1%2Cy%29+%2B+f%28x-1%2Cy%29%29+-+2f%28x%2Cy%29+%5D%2B%5Bf%28x%2Cy%2B1%29+%2B+f%28x%2Cy-1%29%29+-+2f%28x%2Cy%29%5D+%5C%5C+%26%3Df%28x%2B1%2Cy%29+%2B+f%28x-1%2Cy%29%29+%2B+f%28x%2Cy%2B1%29+%2B+f%28x%2Cy-1%29%29+-+4f%28x%2Cy%29++%5C%5C+%5Cend%7Baligned%7D+%5C%5C+%5C%5C)

看到上面可能大家会很可能很陌生，但是这个就是图像中的拉普拉斯卷积核：

![img](https://pic1.zhimg.com/v2-8ed1a50e431beefa73a59de4dc68acb8_b.jpg)

此时共有 4 个自由度 (1,0),(-1,0),(0,1),(0,-1)，当然如果对角线后其自由度可以为 8。

对此我们可以进行归纳：**「拉普拉斯算子是所有自由度上进行微小变化后所获得的增益」**。

我们将其推广到网络图中，考虑有 N 个节点的网络图，其自由度最大为 N，那么函数 ![[公式]](https://www.zhihu.com/equation?tex=f) 可以是 N 维的向量，即：

![[公式]](https://www.zhihu.com/equation?tex=f+%3D+%28f_1%2C...%2Cf_N%29+%5C%5C+%5C%5C)

其中，![[公式]](https://www.zhihu.com/equation?tex=f_i) 表示函数 ![[公式]](https://www.zhihu.com/equation?tex=f) 在网络图中节点 i 处的函数值，类比 ![[公式]](https://www.zhihu.com/equation?tex=f%28x%2Cy%29) 为函数 ![[公式]](https://www.zhihu.com/equation?tex=f) 在 (x,y) 的函数值。

在网络图中，两个节点的之间的增益为 ![[公式]](https://www.zhihu.com/equation?tex=f_i-f_j)，考虑加权图则有 ![[公式]](https://www.zhihu.com/equation?tex=w_%7Bij%7D%28f_i-f_j%29) ，那么对于节点 i 来说，总增益即为拉普拉斯算子在节点 i 的值：

![[公式]](https://www.zhihu.com/equation?tex=%5Cbegin%7Baligned%7D+++%5CDelta+%5Cboldsymbol%7Bf%7D_i+%26%3D+%5Csum_%7Bj+%5Cin+N_i%7D+%5Cfrac%7B%5Cpartial+f_i%7D%7B%5Cpartial+j%5E2%7D+%5C%5C+++%26+%5Capprox++%5Csum_%7Bj%7D+w_%7Bij%7D+%28f_i+-+f_j%29+%5C%5C+%26%3D++%5Csum_%7Bj%7D+w_%7Bij%7D+%28f_i+-+f_j%29+%5C%5C+++%26%3D+%28%5Csum_%7Bj%7D+w_%7Bij%7D%29+f_i+-+%5Csum_j+w_%7Bij%7D+f_j+%5C%5C+++%26%3Dd_if_i+-+w_%7Bi%3A%7Df_i+%5C%5C+++%5Cend%7Baligned%7D+%5C%5C+%5C%5C)

其中，![[公式]](https://www.zhihu.com/equation?tex=d_i%3D%5Csum_%7Bj%5Cin+N_i%7D+w_%7Bij%7D) 为节点 i 的度；上式第二行去掉了 ![[公式]](https://www.zhihu.com/equation?tex=j%5Cin+N_%7Bi%7D) 是因为 ![[公式]](https://www.zhihu.com/equation?tex=w_%7Bij%7D) 可以控制节点 i 的邻接矩阵。

对于任意 ![[公式]](https://www.zhihu.com/equation?tex=i%5Cin+N) 都成立，所以我们有：

![[公式]](https://www.zhihu.com/equation?tex=%5Cbegin%7Baligned%7D++++%5CDelta+%7Bf%7D+%3D%5Cleft%28+%7B%5Cmatrix%7B+%7B%5CDelta+%7Bf_1%7D%7D++%5Ccr++++++%5Cvdots+++%5Ccr+++++%7B%5CDelta+%7Bf_N%7D%7D++%5Ccr++++%7D+%7D+%5Cright%29+%26+%3D+%5Cleft%28+%7B%5Cmatrix%7B++++%7B%7Bd_1%7D%7Bf_1%7D+-+%7Bw_%7B1%3A%7D%7Df%7D++%5Ccr++++++%5Cvdots+++%5Ccr+++++%7B%7Bd_N%7D%7Bf_N%7D+-+%7Bw_%7BN%3A%7D%7Df%7D++%5Ccr++++%7D+%7D+%5Cright%29++%5Ccr++++%26++%3D%5Cleft%28+%7B%5Cmatrix%7B++++%7B%7Bd_1%7D%7D+%26++%5Ccdots++%26+0++%5Ccr++++++%5Cvdots++%26++%5Cddots++%26++%5Cvdots+++%5Ccr+++++0+%26++%5Ccdots++%26+%7B%7Bd_N%7D%7D++%5Ccr++++%7D+%7D+%5Cright%29++f+-+%5Cleft%28+%7B%5Cmatrix%7B++++%7B%7Bw_%7B1%3A%7D%7D%7D++%5Ccr++++++%5Cvdots+++%5Ccr+++++%7B%7Bw_%7BN%3A%7D%7D%7D++%5Ccr++++%7D+%7D+%5Cright%29f++++%5Ccr++%26%3D+diag%28%7Bd_i%7D%29f+-+%5Cmathbf%7BW%7Df++%5Ccr+++++%26%3D+%28%5Cmathbf%7BD%7D+-%5Cmathbf%7BW%7D%29f++%5Ccr+++++%26%3D+%5Cmathbf%7BL%7D+f+%5Ccr+%5Cend%7Baligned%7D+%5C%5C)

自此，我们便给出了图拉普拉斯矩阵的推导过程，这个公式的全称为：图拉普拉斯算子作用在由图节点信息构成的向量 ![[公式]](https://www.zhihu.com/equation?tex=f) 上得到的结果等于图拉普拉斯矩阵和向量 ![[公式]](https://www.zhihu.com/equation?tex=f) 的点积。拉普拉斯矩阵反映了当前节点对周围节点产生扰动时所产生的累积增益，直观上也可以理解为某一节点的权值变为其相邻节点权值的期望影响，形象一点就是拉普拉斯矩阵可以刻画局部的平滑度。

** Laplace Spectral decomposition**

拉普拉斯矩阵的谱分解就是矩阵的特征分解：

![[公式]](https://www.zhihu.com/equation?tex=%5Cmathbf%7BLu_k%7D+%3D+%5Clambda_k+%5Cmathbf%7B+u_k%7D%5C%5C+%5C%5C)

对于无向图来说，拉普拉斯矩阵是实对称矩阵，而实对称矩阵一定可以用正交矩阵进行正交相似对角化：

![[公式]](https://www.zhihu.com/equation?tex=%5Cmathbf%7BL%7D%3D%5Cmathbf%7BU%7D+%5Cmathbf%7B%5CLambda%7D+%5Cmathbf%7BU%7D%5E%7B-1%7D+%5C%5C+%5C%5C)

其中，![[公式]](https://www.zhihu.com/equation?tex=%5Cmathbf%7B%5CLambda%7D) 为特征值构成**「对角矩阵」**，![[公式]](https://www.zhihu.com/equation?tex=%5Cmathbf%7BU%7D) 为特征向量构成的**「正交矩阵」**。

又因为正交矩阵的逆等于正交矩阵的转置：![[公式]](https://www.zhihu.com/equation?tex=%5Cmathbf%7BU%7D%5E%7B-1%7D+%3D+%5Cmathbf%7BU%7D%5E%7BT%7D) ，所以我们有：

![[公式]](https://www.zhihu.com/equation?tex=%5Cmathbf%7BL%7D%3D%5Cmathbf%7BU%7D+%5Cmathbf%7B%5CLambda%7D+%5Cmathbf%7BU%7D%5E%7B-1%7D+%3D%5Cmathbf%7BU%7D+%5Cmathbf%7B%5CLambda%7D+%5Cmathbf%7BU%7D%5E%7BT%7D+%5C%5C+%5C%5C)

因为 L 是半正定矩阵，我们还可以有：

![[公式]](https://www.zhihu.com/equation?tex=%5Cbegin%7Baligned%7D+f%5ET+%5Cmathbf%7BL%7D+f++%26%3D+f%5ETDf+-+f%5ETWf++%5C%5C+%26%3D%5Csum_id_if_i%5E2+-+%5Csum_%7Bi%2Cj%7D+f_i+f_j+w_%7Bij%7D+++%5C%5C+%26%3D%5Cfrac%7B1%7D%7B2%7D%5Cbig%28%5Csum_i+d_i+f_i%5E2-2%5Csum_%7Bij%7Df_i+f_j+w_%7Bij%7D+%2B+%5Csum_id_i+f_i%5E2+++%5Cbig%29+%5C%5C+%26%3D+%5Cfrac%7B1%7D%7B2%7D%5Csum_%7Bi%2Cj%7D+w_%7Bij%7D+%28f_i+-+f_j%29%5E2+%5C%5C+%5Cend%7Baligned%7D++%5C%5C+%5C%5C)

其中，![[公式]](https://www.zhihu.com/equation?tex=f_i) 为节点 i 的信号。我们称 ![[公式]](https://www.zhihu.com/equation?tex=f%5ET+%5Cmathbf%7BL%7D+f+) 为图信号的总变差（Total Variation），可以刻画图信号整体的平滑度。

拉普拉斯的谱分解具有以下几点性质：

- 由于拉普拉斯矩阵以每行（列）元素之和为零，因此拉普拉斯矩阵的至少有一个特征值为 0，对应的特征向量 ![[公式]](https://www.zhihu.com/equation?tex=u_0+%3D+%5B1%EF%BC%8C1%EF%BC%8C%EF%BC%8C%E3%80%82+%E3%80%82+%E3%80%82+1%5D%5ET+%2F+%5Csqrt%7BN%7D)，且满足：![[公式]](https://www.zhihu.com/equation?tex=%5Cmathbf%7BL%7D+u_0+%3D+0+u_0)。
- 拉普拉斯矩阵的特征值都大于等于零，归一化的拉普拉斯矩阵的特征值区间为 [0, 2]；
- 如果有 n 个特征值为 0，则表示图有 n 个子图相互无连接；
- 特征值的总和为矩阵的迹，对于归一化的拉普拉斯矩阵，如果没有孤立节点或子图，其特征值为 N

### 实现三

![[公式]](https://www.zhihu.com/equation?tex=H%5E%7Bl%2B1%7D+%3D+%5Csigma+%28D%5E+%7B-%5Cfrac%7B1%7D%7B2%7D%7D%5Chat%7BA%7DD%5E+%7B-%5Cfrac%7B1%7D%7B2%7D%7DH%5E%7Bl%7DW%5E%7Bl%7D%29)

对于这里的拉普拉斯矩阵 ![[公式]](https://www.zhihu.com/equation?tex=L%5E%7Bsym%7D%3DD%5E+%7B-%5Cfrac%7B1%7D%7B2%7D%7D%5Chat%7BA%7DD%5E+%7B-%5Cfrac%7B1%7D%7B2%7D%7D%3DD%5E+%7B-%5Cfrac%7B1%7D%7B2%7D%7D%28D-A%29D%5E+%7B-%5Cfrac%7B1%7D%7B2%7D%7D%3DI_n-D%5E+%7B-%5Cfrac%7B1%7D%7B2%7D%7DAD%5E+%7B-%5Cfrac%7B1%7D%7B2%7D%7D) ，学名Symmetric normalized Laplacian，也有论文或者博客写 ![[公式]](https://www.zhihu.com/equation?tex=L%3DI_n%2BD%5E+%7B-%5Cfrac%7B1%7D%7B2%7D%7DAD%5E+%7B-%5Cfrac%7B1%7D%7B2%7D%7D) ， 就是一个符号的差别，但本质上还是实现一的两个问题进行的改进：

- **引入自身度矩阵，解决自传递问题；**
- **对邻接矩阵的归一化操作，通过对邻接矩阵两边乘以节点的度开方然后取逆得到。**具体到每一个节点对 ![[公式]](https://www.zhihu.com/equation?tex=i%EF%BC%8Cj) ，矩阵中的元素由下面的式子给出（对于无向无权图）：

![[公式]](https://www.zhihu.com/equation?tex=L_%7Bi%2C+j%7D%5E%7B%5Cmathrm%7Bsym%7D%7D%3A%3D%5Cleft%5C%7B%5Cbegin%7Barray%7D%7Bll%7D%7B1%7D+%26+%7B%5Ctext+%7B+if+%7D+i%3Dj+%5Ctext+%7B+and+%7D+%5Coperatorname%7Bdeg%7D%5Cleft%28v_%7Bi%7D%5Cright%29+%5Cneq+0%7D+%5C%5C+%7B-%5Cfrac%7B1%7D%7B%5Csqrt%7B%5Coperatorname%7Bdeg%7D%5Cleft%28v_%7Bi%7D%5Cright%29+%5Coperatorname%7Bdeg%7D%5Cleft%28v_%7Bj%7D%5Cright%29%7D%7D%7D+%26+%7B%5Ctext+%7B+if+%7D+i+%5Cneq+j+%5Ctext+%7B+and+%7D+v_%7Bi%7D+%5Ctext+%7B+is+adjacent+to+%7D+v_%7Bj%7D%7D+%5C%5C+%7B0%7D+%26+%7B%5Ctext+%7B+otherwise.+%7D%7D%5Cend%7Barray%7D%5Cright.)

其中 ![[公式]](https://www.zhihu.com/equation?tex=deg%28v_i%29%2Cdeg%28v_j%29) 分别为节点 ![[公式]](https://www.zhihu.com/equation?tex=i%2Cj) 的度，也就是度矩阵在节点 ![[公式]](https://www.zhihu.com/equation?tex=i%2Cj) 处的值。

**可能有一点比较疑惑的是怎么两边乘以一个矩阵的逆就归一化了？**这里需要复习到矩阵取逆的本质是做什么。

我们回顾下矩阵的逆的定义，对于式子 ![[公式]](https://www.zhihu.com/equation?tex=A%2AX%3DB) ，假如我们希望求矩阵X，那么当然是令等式两边都乘以 ![[公式]](https://www.zhihu.com/equation?tex=A%5E%7B-1%7D) ，然后式子就变成了 ![[公式]](https://www.zhihu.com/equation?tex=X%3DA%5E%7B-1%7D%2AA%2AX%3DA%5E%7B-1%7DB) 。

举个例子对于，单个节点运算来说，做归一化就是除以它节点的度，这样每一条邻接边信息传递的值就被规范化了，不会因为某一个节点有10条边而另一个只有1条边导致前者的影响力比后者大，因为做完归一化后者的权重只有0.1了，从单个节点上升到二维矩阵的运算，就是对矩阵求逆了，乘以矩阵的逆的本质，就是做矩阵除法完成归一化。但左右分别乘以节点i,j度的开方，就是考虑一条边的两边的点的度。

常见的拉普拉斯矩阵除了以上举的两种，还有![[公式]](https://www.zhihu.com/equation?tex=L%5E%7Brw%7D%3DD%5E+%7B-1%7D%5Chat%7BA%7D%3DD%5E+%7B-1%7D%28D-A%29%3DI_n-D%5E%7B-1%7DA) 等等[3][4]，归一化的方式有差别，根据论文[5]的实验，这些卷积核的形式并没有一种能够在任何场景下比其他的形式效果好，因此在具体使用的时候可以进行多种尝试，但主流的还是实现三，也就是大多数博客提到的。

### 另一种表述

上面是以矩阵的形式计算，可能会看起来非常让人疑惑，下面从单个节点的角度来重新看下这些个公式（本质是一样的，上文解释过，对于单个节点就是除法，对于矩阵就是乘以度矩阵的逆），对于第 ![[公式]](https://www.zhihu.com/equation?tex=l%2B1) 层的节点的特征 ![[公式]](https://www.zhihu.com/equation?tex=h%5E%7Bl%2B1%7D_i) ，对于它的邻接节点 ![[公式]](https://www.zhihu.com/equation?tex=j%5Cin%7BN%7D) ， ![[公式]](https://www.zhihu.com/equation?tex=N) 是节点 ![[公式]](https://www.zhihu.com/equation?tex=i) 的所有邻居节点的集合，可以通过以下公式计算得到：

![[公式]](https://www.zhihu.com/equation?tex=h%5E%7Bl%2B1%7D_%7Bv_i%7D%3D%5Csigma%28%5Csum_j%7B%5Cfrac%7B1%7D%7Bc_%7Bij%7D%7Dh%5El_%7Bv_j%7DW%5E%7Bl%7D%7D%29)

其中， ![[公式]](https://www.zhihu.com/equation?tex=c_%7Bi%2Cj%7D%3D%5Csqrt%7Bd_id_j%7D) ， ![[公式]](https://www.zhihu.com/equation?tex=j%5Cin+N%7Bi%7D) ， ![[公式]](https://www.zhihu.com/equation?tex=N%7Bi%7D) 为 ![[公式]](https://www.zhihu.com/equation?tex=i) 的邻居节点， ![[公式]](https://www.zhihu.com/equation?tex=d_i%2Cd_j) 为 ![[公式]](https://www.zhihu.com/equation?tex=i%2Cj) 的度，这跟上面的公式其实是等价的，所以有些地方的公式是这个，有些的上面那个。

