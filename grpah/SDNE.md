### Structural Deep Network Embedding

#### 想要解决什么问题？

不管是Line，Deepwalk还是node2vec，基本上都训练的时候都是采用skipgram。这样就不可避免的使用了shallow model。然而对于实际的网络数据，网络的结构通常都是高度复杂的。因此使用shallow model很难很好的捕捉的网络的结构特征。得到的节点representation也能有很好的表示能力。同时网络顶点之间的一阶相似度和二阶相似度各自表示了网络局部结构信息和网络全局的信息。之前的Line虽然分别对一阶相似度和二阶相似度设计了相应的损失函数。但最终优化的时候却是分开进行优化的，最后使用的时候简单的将向量进行拼接。为了解决上诉两个问题。SDNE提出引入深度神经网络来捕捉网络的高度非线性结构。同时将顶点的一阶相似度和二阶相似度同时进行优化。

#### 和之前的方法有什么区别？

1.将深度学习引入embedding的学习中，主要体现在autoencoder的使用。

2.将顶点之间的一阶相似度和二阶相似度同时进行优化。

#### 模型细节

为了捕捉到网络的复杂的非线性特征，SDNE引入了深度学习框架。模型的框架如下图所示。

<img src="/Users/eason/Library/Application Support/typora-user-images/image-20201203142157370.png" alt="image-20201203142157370" style="zoom:50%;" />

首先看图中的左半部分，紫色部分表示autoencoder中的encoder部分，蓝色部分表示decoder部分。顶点的输入向量xi

经过encoder部分得到$y^k$,这个向量就是顶点最后的representation。这个向量可以用于之后的监督学习用于顶点之间一阶相似度的学习。然后$y^k$经过decode的解码得到$\hat{x_i}$,这个向量用于二阶相似度的学习。

##### 二阶相似度

我们知道二阶相似度描述的是顶点对领居节点的重叠情况，那么可以将节点$x_i$和其它节点的关系通过$s_i=\{s_{i,j}\}_{j=1}^n,s_{ij}>0$，如果节点和节点j之间有直连边的话。没有直连边那么sij=0。因此$s_i$就表示了节点i的领居结构关系。然后我们将$x_i=s_i$输入网络中，先通过encoder来进行编码，然后使用decoder来进行解码，目标是使用decoder进行解码时重构误差尽可能小。因为两个节点如果邻居结构相似的话，那么其最后经过encoder编码得到的向量也会相似。


$$
y_{i}^{(1)}=\sigma(W^{(1)})x_i+b^{(1)} \\
y_{i}^{(k)}=\sigma(W^{(k)})x_i+b^{(k)},k=2,...,K \\
L = \sum_{i=1}^n||\hat{x_i}-x_i||_2^2
$$
通过上式，我们可以进行中间向量的学习，但是我们注意到，由于网络的稀疏性，很多节点之间是没有直接相连的边的，因此$s_i$中0元素的数量将会大于非零元素的数量。如果我们就这样直接$s_i$作为特征输入的话，模型最后只会更关注0元素而忽略了非0元素，因此我们需要对非零元素添加一个惩罚项，使得最后模型更关注非0元素的学习。通过给非0元素施加一个惩罚项，得到下面的公式:
$$
L_{2nd} = \sum_{i=1}^n||(\hat{x_i}-x_i)\bigodot b_i ||_2^2
$$
$b_i=\{b_{i,j}\}_{j=1}^n，s_{ij}=0,b_{ij}=1,s_{ij}>0,b_{ij}=\beta$,

##### 一阶相似度

为了学习节点之间的一阶相似度从而捕获到网络结构的一阶相似度。网络中节点间若有边相连，那么它们可能是相似的节点。同时边权越强那么节点间就越相似。所以节点边权可以作为一种监督信息，然后通过优化下面的式子来进行学习。
$$
L_{1nd}=\sum_{i,j=1}^n{s_{ij}||y_i-y_j||_2^2}
$$
综上，为了同时优化一阶相似度和二阶相似度，最后的损失函数如下:


$$
L_{mix}=L_{2nd}+\alpha L_{1st}+vL_{reg} \\
= ||(\hat{X}-X)\bigodot B||_F^2 +\alpha \sum_{i,j=1}^n{s_{ij}||y_i-y_j||_2^2} +vL_{reg}
$$
其中L_reg为L2惩罚项，目的是为了防止模型的过拟合.
$$
L_{reg}=\frac{1}{2}\sum_{k=1}^K(||W^{k}||_F^2+||\hat{W}^{k}||_F^2)
$$


<img src="/Users/eason/Library/Application Support/typora-user-images/image-20201203173223429.png" alt="image-20201203173223429" style="zoom:50%;" />

#### 总结

1. SDNE通过引入神经网络，利用神经网络的强大的非线性拟合能力来捕捉网络的高度非线性结构

2. SDNE将节点之间的一阶相似度和二阶相似度同时进行优化。



##### Laplacian Eigenmaps

下面先介绍Laplacian Eigenmaps具体操作过程：

- Step 1 寻找近邻，构建邻接图

同LLE，这里可以通过 ![[公式]](https://www.zhihu.com/equation?tex=%5Cepsilon) -neighborhoods和k-nearest-neighbors来选择近邻。对于前者，如果 ![[公式]](https://www.zhihu.com/equation?tex=x_i) 是 ![[公式]](https://www.zhihu.com/equation?tex=x_j) 的近邻，那么反过来亦然，对于后者则没有这种对称性，所以为了满足对称性，后者放松约束，**只要使得 ![[公式]](https://www.zhihu.com/equation?tex=x_j+%5Cin+%5Cmathcal+N_k%28x_i%29) 或者 ![[公式]](https://www.zhihu.com/equation?tex=x_i+%5Cin+%5Cmathcal+N_k%28x_j%29) 即可认为有一条边**；前者可能会导致图中产生许多个小的连通分量，而后者不会。

将每个数据点看作一个顶点，将近邻对用一条边连接起来，这样就构成了一张图，准确来说如果利用k-nearest-neighbors的方法来选择近邻对，得到的是一张有向图，但是经过上面加粗部分的操作，可以看作是无向图。

- Step 2 给边赋权值，构建带权图

根据顶点之间的关系来给图之间赋权值，有以下两种方式。第一种，利用Heat Kernel，即：

![[公式]](https://www.zhihu.com/equation?tex=W_%7Bij%7D+%3D+%5Cexp+%5Cleft%28+-%5Cfrac%7B%5CVert+x_i+-+x_j+%5CVert_2%5E2%7D%7Bt%7D+%5Cright%29+%2C+%5Cqquad+Connected%28x_i%2C+x_j%29%5C%5C+W_%7Bij%7D+%3D+0%2C+%5Cqquad+NotConnected%28x_i%2C+x_j%29)

另外 一种方式就是简单地取 1 和 0，即：

![[公式]](https://www.zhihu.com/equation?tex=W_%7Bij%7D+%3D+1%2C+%5Cqquad+Connected%28x_i%2C+x_j%29%5C%5C+W_%7Bij%7D+%3D+0%2C+%5Cqquad+NotConnected%28x_i%2C+x_j%29)

当 ![[公式]](https://www.zhihu.com/equation?tex=t+%5Crightarrow+%2B%5Cinfty) ，两者等价。一般来说选取第一种方案比较好。**得到的 ![[公式]](https://www.zhihu.com/equation?tex=W) 是对称阵**。

- Step 3 Eigenmaps

计算图的Laplacian Matrix，即 ![[公式]](https://www.zhihu.com/equation?tex=L+%3D+D+-+W) ，其中 ![[公式]](https://www.zhihu.com/equation?tex=D_%7Bii%7D+%3D+%5Csum_j+W_%7Bji%7D) ， ![[公式]](https://www.zhihu.com/equation?tex=D) 是对角矩阵，第 i 个对角元素是图权值矩阵 ![[公式]](https://www.zhihu.com/equation?tex=W) 第 i 列的和。下面计算广义特征值问题：

![[公式]](https://www.zhihu.com/equation?tex=Lf+%3D+%5Clambda+Df+%5C%5C)

取 最小的d + 1个特征值对应的特征向量，去除最小的特征值 0 对应的特征向量，得到：

![[公式]](https://www.zhihu.com/equation?tex=Y+%3D+%5Bf_1%3B+f_2%3B+%5Ccdots%3B+f_d%5D+%5Cin+R%5E%7Bn%5Ctimes+d%7D+%5C%5C)

上面给出了Laplacian Eigenmaps的算法过程，可以看出其主要思想是：**寻找近邻，构建邻接图，Laplacian Matrix特征值分解**。和LLE的过程比较相似，只不过LLE是基于近邻重构的思想，而LE在做什么我们目前还不清楚，所以下面来看看LE背后的原理是什么。

LE首先将数据点转换为一张图 ![[公式]](https://www.zhihu.com/equation?tex=G+%3D+%28V%2C+E%29) ，近邻样本之间有一条边，是无向图，并且每条边都有权重。LE要做的就是在低维空间寻找一组表示 ![[公式]](https://www.zhihu.com/equation?tex=Y+%3D+%5By_1%3By_2%3B%5Ccdots%3By_n%5D%5ET+%5Cin+R%5E%7Bn%5Ctimes+d%7D) ，使得近邻关系和高维空间尽可能一致 ，假如 ![[公式]](https://www.zhihu.com/equation?tex=x_i) 与 ![[公式]](https://www.zhihu.com/equation?tex=x_j) 离得比较近（ ![[公式]](https://www.zhihu.com/equation?tex=W_%7Bij%7D) 比较大），那么对应的 ![[公式]](https://www.zhihu.com/equation?tex=y_i) 与 ![[公式]](https://www.zhihu.com/equation?tex=y_j) 也应该比较近（如果二者离得远，那么乘以 ![[公式]](https://www.zhihu.com/equation?tex=W_%7Bij%7D) 带来 的损失就会很大），所以使用下面的优化方案：

![[公式]](https://www.zhihu.com/equation?tex=%5Cmin_Y%5Cfrac%7B1%7D%7B2%7D%5Csum_%7Bi%3D1%7D%5En+%5Csum_%7Bj%3D1%7D%5En+W_%7Bij%7D%5CVert+y_i+-+y_j+%5CVert_2%5E2+%5C%5C)

而上式使用矩阵形式即为：

![[公式]](https://www.zhihu.com/equation?tex=%5Cmin_Y%5Cfrac%7B1%7D%7B2%7D%5Csum_%7Bi%3D1%7D%5En+%5Csum_%7Bj%3D1%7D%5En+W_%7Bij%7D%5CVert+y_i+-+y_j+%5CVert_2%5E2+%3D+%5Cmin_Y+%5Cfrac%7B1%7D%7B2%7Dtr%5Cleft%28+Y%5ET%28D-W%29Y%5Cright%29%5C%5C)

同样道理，我们也对 ![[公式]](https://www.zhihu.com/equation?tex=Y) 施加一个约束：

![[公式]](https://www.zhihu.com/equation?tex=Y%5ETDY+%3D+I%5E%7Bd%5Ctimes+d%7D+%5C%5C)

这是对不同的 ![[公式]](https://www.zhihu.com/equation?tex=y_i) 要求不同的模的大小，因为图中有的结点比较重要（ ![[公式]](https://www.zhihu.com/equation?tex=D_%7Bii%7D) 比较大 ），相反有的则不是很重要。给定上面的优化目标和约束条件，问题就可以转化为求广义特征值问题：

![[公式]](https://www.zhihu.com/equation?tex=Lf+%3D+%5Clambda+Df+%5C%5C)









