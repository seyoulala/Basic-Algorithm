<img src="https://pic3.zhimg.com/v2-35393b75f51c81bb3c09774e76a7d91c_r.jpg" alt="【机器学习】逻辑回归（非常详细）" style="zoom:50%;" />



逻辑回归是一个非常经典的算法，其中也包含了非常多的细节，曾看到一句话：如果面试官问你熟悉哪个机器学习模型，可以说 SVM，但千万别说 LR，因为细节真的太多了。

秉持着精益求精的工匠精神不断对笔记进行修改和改进，本着开源精神帮助大家一起学习。欢迎大家在阅读的过程中提出修改建议，我会非常感激。如果文章有帮助的话，希望能点个赞。

## 1. 模型介绍

Logistic Regression 虽然被称为回归，但其实际上是分类模型，并常用于二分类。Logistic Regression 因其简单、可并行化、可解释强深受工业界喜爱。

Logistic 回归的本质是：假设数据服从这个分布，然后使用极大似然估计做参数的估计。

### 1.1 Logistic 分布

Logistic 分布是一种连续型的概率分布，其**分布函数**和**密度函数**分别为：   

![[公式]](https://www.zhihu.com/equation?tex=F%28x%29+%3D+P%28X+%5Cleq+x%29%3D%5Cfrac%7B1%7D%7B1%2Be%5E%7B-%28x-%5Cmu%29%2F%5Cgamma%7D%7D+%5C%5C+f%28x%29+%3D+F%5E%7B%27%7D%28X+%5Cleq+x%29%3D%5Cfrac%7Be%5E%7B-%28x-%5Cmu%29%2F%5Cgamma%7D%7D%7B%5Cgamma%281%2Be%5E%7B-%28x-%5Cmu%29%2F%5Cgamma%7D%29%5E%7B2%7D%7D+%5C%5C) 

其中， ![[公式]](https://www.zhihu.com/equation?tex=%5Cmu) 表示**位置参数**， ![[公式]](https://www.zhihu.com/equation?tex=%5Cgamma%3E0) 为**形状参数**。我们可以看下其图像特征：



![img](https://pic2.zhimg.com/v2-b15289fd1162a807e11949e5396c7989_b.jpg)![img](https://pic2.zhimg.com/80/v2-b15289fd1162a807e11949e5396c7989_1440w.jpg)



Logistic 分布是由其位置和尺度参数定义的连续分布。Logistic 分布的形状与正态分布的形状相似，但是 Logistic 分布的尾部更长，所以我们可以使用 Logistic 分布来建模比正态分布具有更长尾部和更高波峰的数据分布。在深度学习中常用到的 Sigmoid 函数就是 Logistic 的分布函数在 ![[公式]](https://www.zhihu.com/equation?tex=%5Cmu%3D0%2C+%5Cgamma%3D1) 的特殊形式。

### 1.2 Logistic 回归

之前说到 Logistic 回归主要用于分类问题，我们以二分类为例，对于所给数据集假设存在这样的一条直线可以将数据完成线性可分。



![img](https://pic3.zhimg.com/v2-34f3997ae1975cd620a8514e3954fa9e_b.jpg)![img](https://pic3.zhimg.com/80/v2-34f3997ae1975cd620a8514e3954fa9e_1440w.jpg)



决策边界可以表示为 ![[公式]](https://www.zhihu.com/equation?tex=w_1x_1%2Bw_2x_2%2Bb%3D0) ，假设某个样本点 ![[公式]](https://www.zhihu.com/equation?tex=h_w%28x%29+%3D+w_1x_1%2Bw_2x_2%2Bb+%3E+0) 那么可以判断它的类别为 1，这个过程其实是感知机。

Logistic 回归还需要加一层，它要找到分类概率 P(Y=1) 与输入向量 x 的直接关系，然后通过比较概率值来判断类别。

考虑二分类问题，给定数据集

![[公式]](https://www.zhihu.com/equation?tex=+D%3D%7B%28x_%7B1%7D%2C+y_%7B1%7D%29%2C%28x_%7B2%7D%2Cy_%7B2%7D%29%2C%5Ccdots%2C%28x_%7BN%7D%2C+y_%7BN%7D%29%7D%2C+x_%7Bi%7D+%5Csubseteq+R%5E%7Bn%7D%2C+y_%7Bi%7D+%5Cin+%7B0%2C1%7D%2Ci%3D1%2C2%2C%5Ccdots%2CN+++%5C%5C) 

考虑到 ![[公式]](https://www.zhihu.com/equation?tex=w%5E%7BT%7Dx%2Bb) 取值是连续的，因此它不能拟合离散变量。可以考虑用它来拟合条件概率 ![[公式]](https://www.zhihu.com/equation?tex=p%28Y%3D1%7Cx%29) ，因为概率的取值也是连续的。

但是对于 ![[公式]](https://www.zhihu.com/equation?tex=w+%5Cne+0) （若等于零向量则没有什么求解的价值）， ![[公式]](https://www.zhihu.com/equation?tex=w%5E%7BT%7Dx%2Bb) 取值为 ![[公式]](https://www.zhihu.com/equation?tex=R) ，不符合概率取值为 0 到 1，因此考虑采用广义线性模型。

最理想的是单位阶跃函数： 

![[公式]](https://www.zhihu.com/equation?tex=p%28y%3D1+%7C+x%29%3D%5Cbegin%7Bcases%7D+0%2C%26+z%5Clt+0+%5C%5C+0.5%2C%26+z+%3D+0%5C%5C+1%2C%26+z%5Cgt+0%5C+%5Cend%7Bcases%7D+%2C%5Cquad+z%3Dw%5ET+x%2Bb++%5C%5C) 

但是这个阶跃函数不可微，对数几率函数是一个常用的替代函数： 

![[公式]](https://www.zhihu.com/equation?tex=+y+%3D+%5Cfrac%7B1%7D%7B1%2Be%5E%7B-%28w%5E%7BT%7D+x+%2B+b%29%7D%7D++%5C%5C) 

于是有： 

![[公式]](https://www.zhihu.com/equation?tex=+ln+%5Cfrac%7By%7D%7B1%E2%88%92y%7D+%3D+w%5E%7BT%7Dx+%2B+b+%5C%5C) 

我们将 y 视为 x 为正例的概率，则 1-y 为 x 为其反例的概率。两者的比值称为**几率（odds）**，指该事件发生与不发生的概率比值，若事件发生的**概率**为 p。则对数几率：

![[公式]](https://www.zhihu.com/equation?tex=+ln%28odds%29+%3D+ln+%5Cfrac%7By%7D%7B1%E2%88%92y%7D++%5C%5C) 

将 y 视为类后验概率估计，重写公式有： 

![[公式]](https://www.zhihu.com/equation?tex=w%5E%7BT%7D+x+%2B+b+%3D+ln%5Cfrac%7BP%28Y%3D1%7Cx%29%7D%7B1-P%28Y%3D1%7Cx%29%7D+%5C%5C+P%28Y%3D1%7Cx%29+%3D+%5Cfrac%7B1%7D%7B1%2Be%5E%7B-%28w%5E%7BT%7D+x+%2B+b%29%7D%7D+%5C%5C) 

也就是说，输出 Y=1 的对数几率是由输入 x 的**线性函数**表示的模型，这就是**逻辑回归模型**。当 ![[公式]](https://www.zhihu.com/equation?tex=w%5E%7BT%7Dx%2Bb) 的值越接近正无穷， ![[公式]](https://www.zhihu.com/equation?tex=P%28Y%3D1%7Cx%29+) 概率值也就越接近 1。因此**逻辑回归的思路**是，先拟合决策边界(不局限于线性，还可以是多项式)，再建立这个边界与分类的概率联系，从而得到了二分类情况下的概率。

在这我们思考个问题，我们使用对数几率的意义在哪？通过上述推导我们可以看到 Logistic 回归实际上是使用线性回归模型的预测值逼近分类任务真实标记的对数几率，其优点有：

1. 直接对**分类的概率**建模，无需实现假设数据分布，从而避免了假设分布不准确带来的问题（区别于生成式模型）；
2. 不仅可预测出类别，还能得到该**预测的概率**，这对一些利用概率辅助决策的任务很有用；
3. 对数几率函数是**任意阶可导的凸函数**，有许多数值优化算法都可以求出最优解。

### 1.3 代价函数

逻辑回归模型的数学形式确定后，剩下就是如何去求解模型中的参数。在统计学中，常常使用极大似然估计法来求解，即找到一组参数，使得在这组参数下，我们的数据的似然度（概率）最大。

设： 

![[公式]](https://www.zhihu.com/equation?tex=%5Cbegin%7Baligned%7D+P%28Y%3D1%7Cx%29+%26%3D+p%28x%29+%5C%5C++P%28Y%3D0%7Cx%29+%26%3D+1-+p%28x%29+%5Cend%7Baligned%7D%5C%5C) 

似然函数： 

![[公式]](https://www.zhihu.com/equation?tex=L%28w%29%3D%5Cprod%5Bp%28x_%7Bi%7D%29%5D%5E%7By_%7Bi%7D%7D%5B1-p%28x_%7Bi%7D%29%5D%5E%7B1-y_%7Bi%7D%7D++%5C%5C) 

为了更方便求解，我们对等式两边同取对数，写成对数似然函数： 

![[公式]](https://www.zhihu.com/equation?tex=+%5Cbegin%7Baligned%7D+L%28w%29%26%3D%5Csum%5By_%7Bi%7Dlnp%28x_%7Bi%7D%29%2B%281-y_%7Bi%7D%29ln%281-p%28x_%7Bi%7D%29%29%5D+%5C%5C+%26%3D%5Csum%5By_%7Bi%7Dln%5Cfrac%7Bp%28x_%7Bi%7D%29%7D%7B1-p%28x_%7Bi%7D%29%7D%2Bln%281-p%28x_%7Bi%7D%29%29%5D++%5C%5C+%26%3D%5Csum%5By_%7Bi%7D%28w+%5Ccdot+x_%7Bi%7D%29+-+ln%281%2Be%5E%7Bw+%5Ccdot+x_%7Bi%7D%7D%29%5D+%5Cend%7Baligned%7D+%5C%5C) 

在机器学习中我们有损失函数的概念，其衡量的是模型预测错误的程度。如果取整个数据集上的平均对数似然损失，我们可以得到:  

![[公式]](https://www.zhihu.com/equation?tex=J%28w%29%3D-%5Cfrac%7B1%7D%7BN%7DlnL%28w%29+%5C%5C) 

即在逻辑回归模型中，我们**最大化似然函数**和**最小化损失函数**实际上是等价的。

### 1.4 求解

求解逻辑回归的方法有非常多，我们这里主要聊下梯度下降和牛顿法。优化的主要目标是找到一个方向，参数朝这个方向移动之后使得损失函数的值能够减小，这个方向往往由一阶偏导或者二阶偏导各种组合求得。逻辑回归的损失函数是：

![[公式]](https://www.zhihu.com/equation?tex=J%28w%29+%3D++-%5Cfrac%7B1%7D%7Bn%7D%28%5Csum_%7Bi%3D1%7D%5En%28y_ilnp%28x_i%29%2B%281-y_i%29ln%281-p%28x_i%29%29%29+%5C%5C) 

1. 随机梯度下降

梯度下降是通过 J(w) 对 w 的一阶导数来找下降方向，并且以迭代的方式来更新参数，更新方式为 : 

![[公式]](https://www.zhihu.com/equation?tex=+g_i+%3D+%5Cfrac%7B%5Cpartial+J%28w%29%7D+%7B%5Cpartial+w_i%7D+%3D%28p%28x_i%29-y_i%29x_i+%5C%5C+w%5E%7Bk%2B1%7D_i%3Dw%5Ek_i-%5Calpha+g_i) 

其中 k  为迭代次数。每次更新参数后，可以通过比较 ![[公式]](https://www.zhihu.com/equation?tex=+%7C%7CJ%28w%5E%7Bk%2B1%7D%29%E2%88%92J%28w%5Ek%29%7C%7C+) 小于阈值或者到达最大迭代次数来停止迭代。

\2. 牛顿法

牛顿法的基本思路是，**在现有极小点估计值的附近对 f(x) 做二阶泰勒展开，进而找到极小点的下一个估计值**。假设 ![[公式]](https://www.zhihu.com/equation?tex=w%5Ek) 为当前的极小值估计值，那么有： 

![[公式]](https://www.zhihu.com/equation?tex=+%5Cvarphi+%28w%29+%3D+J%28w%5Ek%29+%2B+J%5E%7B%27%7D%28w%5Ek%29%28w-w%5Ek%29%2B%5Cfrac%7B1%7D%7B2%7DJ%5E%7B%22%7D%28w%5Ek%29%28w-w%5Ek%29%5E2++%5C%5C) 

然后令 ![[公式]](https://www.zhihu.com/equation?tex=%CF%86%5E%7B%27%7D%28w%29%3D0) ，得到了 ![[公式]](https://www.zhihu.com/equation?tex=+w%5E%7Bk%2B1%7D%3Dw%5E%7Bk%7D%E2%88%92%5Cfrac%7BJ%5E%7B%27%7D%28w%5Ek%29%7D%7BJ%5E%7B%22%7D%28w%5Ek%29%7D) 。因此有迭代更新式： 

![[公式]](https://www.zhihu.com/equation?tex=w%5E%7Bk%2B1%7D+%3D+w%5E%7Bk%7D+-+%5Cfrac%7BJ%5E%7B%27%7D%28w%5E%7Bk%7D%29%7D%7BJ%5E%7B%22%7D%28w%5E%7Bk%7D%29%7D+%3D+w%5E%7Bk%7D+-+H_%7Bk%7D%5E%7B-1%7D%5Ccdot+g_%7Bk%7D+%5C%5C) 

其中 ![[公式]](https://www.zhihu.com/equation?tex=H_%7Bk%7D%5E%7B-1%7D) 为海森矩阵： 

![[公式]](https://www.zhihu.com/equation?tex=H_%7Bmn%7D+%3D+%5Cfrac+%7B%5Cpartial%5E2+J%28w%29%7D+%7B%5Cpartial+w_%7Bm%7D+%5Cpartial+w_%7Bn%7D%7D+%3Dh_%7Bw%7D%28x%5E%7B%28i%29%7D%29%281-p_%7Bw%7D%28x%5E%7B%28i%29%7D%29%29x%5E%7B%28i%29%7D_mx%5E%7B%28i%29%7D_n++%5C%5C) 

此外，这个方法需要目标函数是二阶连续可微的，本文中的 J(w) 是符合要求的。

### 1.5 正则化

正则化是一个通用的算法和思想，所以会产生过拟合现象的算法都可以使用正则化来避免过拟合。

在经验风险最小化的基础上（也就是训练误差最小化），尽可能采用简单的模型，可以有效提高泛化预测精度。如果模型过于复杂，变量值稍微有点变动，就会引起预测精度问题。正则化之所以有效，就是因为其降低了特征的权重，使得模型更为简单。

正则化一般会采用 L1 范式或者 L2 范式，其形式分别为 ![[公式]](https://www.zhihu.com/equation?tex=%CE%A6%28w%29%3D%7C%7Cx%7C%7C_1) 和 ![[公式]](https://www.zhihu.com/equation?tex=%CE%A6%28w%29%3D%7C%7Cx%7C%7C_2+) 。

1. L1 正则化

LASSO 回归，相当于为模型添加了这样一个先验知识：w 服从零均值拉普拉斯分布。  首先看看拉普拉斯分布长什么样子： 

![[公式]](https://www.zhihu.com/equation?tex=f%28w%7C%5Cmu%2Cb%29%3D%5Cfrac%7B1%7D%7B2b%7D%5Cexp+%5Cleft+%28+-%5Cfrac%7B%7Cw-%5Cmu%7C%7D%7Bb%7D%5Cright+%29%5C%5C) 

由于引入了先验知识，所以似然函数这样写：  

![[公式]](https://www.zhihu.com/equation?tex=+%5Cbegin%7Baligned%7D+L%28w%29%26%3DP%28y%7Cw%2Cx%29P%28w%29%5C%5C+%26%3D%5Cprod_%7Bi%3D1%7D%5ENp%28x_i%29%5E%7By_i%7D%281-p%28x_i%29%29%5E%7B1-y_i%7D%5Cprod_%7Bj%3D1%7D%5Ed+%5Cfrac%7B1%7D%7B2b%7D%5Cexp+%5Cleft+%28%7B-%5Cfrac%7B%7Cw_j%7C%7D%7Bb%7D%7D+%5Cright+%29+%5Cend%7Baligned%7D++%5C%5C) 

 取 log 再取负，得到目标函数：

![[公式]](https://www.zhihu.com/equation?tex=-%5Cln+L%28w%29%3D-%5Csum_i+%5By_i%5Cln+p%28x_i%29%2B%281-y_i%29ln%281-p%28x_i%29%29%5D%2B%5Cfrac%7B1%7D%7B2b%5E2%7D%5Csum_j%7Cw_j%7C++%5C%5C) 

等价于原始损失函数的后面加上了 L1 正则，因此 L1 正则的本质其实是为模型增加了“**模型参数服从零均值拉普拉斯分布**”这一先验知识。

\2. L2 正则化

Ridge 回归，相当于为模型添加了这样一个先验知识：w 服从零均值正态分布。 

首先看看正态分布长什么样子： 

![[公式]](https://www.zhihu.com/equation?tex=f%28w%7C%5Cmu%2C%5Csigma%29%3D%5Cfrac%7B1%7D%7B%5Csqrt%7B2%5Cpi%7D%5Csigma%7D%5Cexp+%5Cleft+%28+-%5Cfrac%7B%28w-%5Cmu%29%5E2%7D%7B2%5Csigma%5E2%7D%5Cright+%29++%5C%5C) 

由于引入了先验知识，所以似然函数这样写：

![[公式]](https://www.zhihu.com/equation?tex=%5Cbegin%7Baligned%7D+L%28w%29%26%3DP%28y%7Cw%2Cx%29P%28w%29%5C%5C+%26%3D%5Cprod_%7Bi%3D1%7D%5ENp%28x_i%29%5E%7By_i%7D%281-p%28x_i%29%29%5E%7B1-y_i%7D%5Cprod_%7Bj%3D1%7D%5Ed+%5Cfrac%7B1%7D%7B%5Csqrt%7B2%5Cpi%7D%5Csigma%7D%5Cexp+%5Cleft+%28%7B-%5Cfrac%7Bw_j%5E2%7D%7B2%5Csigma%5E2%7D%7D+%5Cright+%29%5C%5C+%26%3D%5Cprod_%7Bi%3D1%7D%5ENp%28x_i%29%5E%7By_i%7D%281-p%28x_i%29%29%5E%7B1-y_i%7D+%5Cfrac%7B1%7D%7B%5Csqrt%7B2%5Cpi%7D%5Csigma%7D%5Cexp+%5Cleft+%28%7B-%5Cfrac%7Bw%5ETw%7D%7B2%5Csigma%5E2%7D%7D+%5Cright+%29+%5Cend%7Baligned%7D+%5C%5C) 

取 ln 再取负，得到目标函数：

![[公式]](https://www.zhihu.com/equation?tex=-%5Cln+L%28w%29%3D-%5Csum_i+%5By_i%5Cln+p%28x_i%29%2B%281-y_i%29ln%281-p%28x_i%29%29%5D%2B%5Cfrac%7B1%7D%7B2%5Csigma%5E2%7Dw%5ETw+%5C%5C) 

等价于原始的损失函数后面加上了 L2 正则，因此 L2 正则的本质其实是为模型增加了“**模型参数服从零均值正态分布**”这一先验知识。

\3. L1 和 L2 的区别

从上面的分析中我们可以看到，L1 正则化增加了所有权重 w 参数的绝对值之和逼迫更多 w 为零，也就是变稀疏（ L2 因为其导数也趋 0, 奔向零的速度不如 L1 给力了）。我们对稀疏规则趋之若鹜的一个关键原因在于它能**实现特征的自动选择**。一般来说，大部分特征 x_i 都是和最终的输出 y_i 没有关系或者不提供任何信息的。在最小化目标函数的时候考虑 x_i 这些额外的特征，虽然可以获得更小的训练误差，但在预测新的样本时，这些没用的特征权重反而会被考虑，从而干扰了对正确 y_i 的预测。L1 正则化的引入就是为了完成特征自动选择的光荣使命，它会学习地去掉这些无用的特征，也就是把这些特征对应的权重置为 0。

L2 正则化中增加所有权重 w 参数的平方之和，逼迫所有 w 尽可能趋向零但不为零（L2 的导数趋于零）。因为在未加入 L2 正则化发生过拟合时，拟合函数需要顾忌每一个点，最终形成的拟合函数波动很大，在某些很小的区间里，函数值的变化很剧烈，也就是某些 w 值非常大。为此，L2 正则化的加入就惩罚了权重变大的趋势。

我们以二维样本为例，图解阐述加入 L1 正则化和 L2 正则化之后目标函数求解时发生的变化。

- 原函数曲线等高线（同颜色曲线上，每一组 ![[公式]](https://www.zhihu.com/equation?tex=w_1%2Cw_2) 带入后值都相同)



![img](https://pic1.zhimg.com/v2-896a01ead6aee864250941a64e7931e4_b.jpg)![img](https://pic1.zhimg.com/80/v2-896a01ead6aee864250941a64e7931e4_1440w.jpg)



那现在我们看下加了 L1 正则化和 L2 正则化之后，目标函数求解的时候，最终解会有什么变化。



![img](https://pic4.zhimg.com/v2-91986c70dab4d152339ea085321c6f3f_b.jpg)![img](https://pic4.zhimg.com/80/v2-91986c70dab4d152339ea085321c6f3f_1440w.jpg)



从上边两幅图中我们可以看出：

- 如果不加 L1 和 L2 正则化的时候，对于线性回归这种目标函数凸函数的话，我们最终的结果就是最里边的紫色的小圈圈等高线上的点。
- 当加入 L1 正则化的时候，我们先画出 ![[公式]](https://www.zhihu.com/equation?tex=%7Cw_1%7C%2B%7Cw_2%7C%3DF+) 的图像，也就是一个菱形，代表这些曲线上的点算出来的 ![[公式]](https://www.zhihu.com/equation?tex=L_1) 范数 ![[公式]](https://www.zhihu.com/equation?tex=%7Cw_1%7C%2B%7Cw_2%7C+) 都为 F。那我们现在的目标是不仅是原曲线算的值要小（越来越接近中心的紫色圈圈），还要使得这个菱形越小越好（F 越小越好）。那么还和原来一样的话，过中心紫色圈圈的那个菱形明显很大，因此我们要取到一个恰好的值。那么如何求值呢？



![img](https://pic4.zhimg.com/v2-efc752bd6d1ce09dbf2e18b9766570eb_b.jpg)![img](https://pic4.zhimg.com/80/v2-efc752bd6d1ce09dbf2e18b9766570eb_1440w.jpg)



1. 以同一条原曲线目标等高线来说，现在以最外圈的红色等高线为例，我们看到，对于红色曲线上的每个点都可做一个菱形，根据上图可知，当这个菱形与某条等高线相切（仅有一个交点）的时候，这个菱形最小，上图相割对比较大的两个菱形对应的 L1 范数更大。用公式说这个时候能使得在相同的 ![[公式]](https://www.zhihu.com/equation?tex=%5Cfrac%7B1%7D%7BN%7D++%5Csum_%7Bi+%3D+1%7D%5EN%7B%28y_i+-w%5ET+x_i%29%5E2+%7D) ，由于相切的时候的  ![[公式]](https://www.zhihu.com/equation?tex=C%7C%7Cw%7C%7C_%7B1%7D+) 小，即 ![[公式]](https://www.zhihu.com/equation?tex=%7Cw_1%7C%2B%7Cw_2%7C)所以能够使得![[公式]](https://www.zhihu.com/equation?tex=%5Cfrac%7B1%7D%7BN%7D++%5Csum%7Bi+%3D+1%7D%5EN%7B%28y_i+-w%5ET+x_i%29%5E2+%7D%2B+C%7C%7Cw%7C%7C_%7B1%7D) 更小；
2. 有了第一条的说明我们可以看出，最终加入 L1 范数得到的解一定是某个菱形和某条原函数等高线的切点。现在有个比较重要的结论来了，**我们经过观察可以看到，几乎对于很多原函数等高曲线，和某个菱形相交的时候及其容易相交在坐标轴（比如上图），也就是说最终的结果，解的某些维度及其容易是 0，比如上图最终解是** ![[公式]](https://www.zhihu.com/equation?tex=w%3D%280%2Cx%29) **，这也就是我们所说的 L1 更容易得到稀疏解（解向量中 0 比较多）的原因；**
3. 当然光看着图说，L1 的菱形更容易和等高线相交在坐标轴一点都没说服力，只是个感性的认识，我们接下来从更严谨的方式来证明，简而言之就是假设现在我们是一维的情况下 ![[公式]](https://www.zhihu.com/equation?tex=h%28w%29+%3D+f%28w%29+%2B+C%7Cw%7C) ，其中 h(w) 是目标函数， ![[公式]](https://www.zhihu.com/equation?tex=f%28w%29+)  是没加 L1 正则化项前的目标函数， ![[公式]](https://www.zhihu.com/equation?tex=C%7Cw%7C) 是 L1 正则项，要使得 0 点成为最值可能的点，虽然在 0 点不可导，但是我们只需要让 0 点左右的导数异号，即 ![[公式]](https://www.zhihu.com/equation?tex=h_%7Bl%7D%5E%7B%27%7D%280%29++h_%7Br%7D%5E%7B%27%7D%280%29+%3D+%28f%5E%7B%27%7D%280%29+%2B+C%29%28f%5E%7B%27%7D%280%29+-+C%29+%3C+0+)  即可也就是 ![[公式]](https://www.zhihu.com/equation?tex=+C+%3E%7Cf%5E%7B%27%7D%280%29%7C) 的情况下，0 点都是可能的最值点。

当加入 L2 正则化的时候，分析和 L1 正则化是类似的，也就是说我们仅仅是从菱形变成了圆形而已，同样还是求原曲线和圆形的切点作为最终解。当然与 L1 范数比，我们这样求的 L2 范数的**从图上来看，不容易交在坐标轴上，但是仍然比较靠近坐标轴。因此这也就是我们老说的，L2 范数能让解比较小（靠近 0），但是比较平滑（不等于 0）。**

综上所述，我们可以看见，加入正则化项，在最小化经验误差的情况下，可以让我们选择解更简单（趋向于 0）的解。

结构风险最小化：在经验风险最小化的基础上（也就是训练误差最小化），尽可能采用简单的模型，以此提高泛化预测精度。

**因此，加正则化项就是结构风险最小化的一种实现。**

**正则化之所以能够降低过拟合的原因在于，正则化是结构风险最小化的一种策略实现。**

**简单总结下**：

给 loss function 加上正则化项，能使新得到的优化目标函数 ![[公式]](https://www.zhihu.com/equation?tex=h+%3D+f%2B%7C%7Cw%7C%7C+) ，需要在 f 和 ||w|| 中做一个权衡，如果还像原来只优化 f 的情况下，那可能得到一组解比较复杂，使得正则项 ||w|| 比较大，那么 h 就不是最优的，因此可以看出加正则项能让解更加简单，符合奥卡姆剃刀理论，同时也比较符合在偏差和方差（方差表示模型的复杂度）分析中，通过降低模型复杂度，得到更小的泛化误差，降低过拟合程度。

L1 正则化就是在 loss function 后边所加正则项为 L1 范数，加上 L1 范数容易得到稀疏解（0 比较多）。L2 正则化就是 loss function 后边所加正则项为 L2 范数的平方，加上 L2 正则相比于 L1 正则来说，得到的解比较平滑（不是稀疏），但是同样能够保证解中接近于 0（但不是等于 0，所以相对平滑）的维度比较多，降低模型的复杂度。

### 1.6 并行化

从逻辑回归的求解方法中我们可以看到，无论是随机梯度下降还是牛顿法，或者是没有提到的拟牛顿法，都是需要计算梯度的，因此逻辑回归的并行化最主要的就是对目标函数梯度计算的并行化。

我们看到目标函数的梯度向量计算中只需要进行向量间的点乘和相加，可以很容易将每个迭代过程拆分成相互独立的计算步骤，由不同的节点进行独立计算，然后归并计算结果。

下图是一个标签和样本矩阵，行为特征向量，列为特征维度。



![img](https://pic3.zhimg.com/v2-9c5aea83687172eb7d4756397bc2669e_b.jpg)![img](https://pic3.zhimg.com/80/v2-9c5aea83687172eb7d4756397bc2669e_1440w.jpg)



样本矩阵按行划分，将样本特征向量分布到不同的计算节点，由各计算节点完成自己所负责样本的点乘与求和计算，然后将计算结果进行归并，则实现了按行并行的 LR。按行并行的 LR 解决了样本数量的问题，但是实际情况中会存在针对高维特征向量进行逻辑回归的场景，仅仅按行进行并行处理，无法满足这类场景的需求，因此还需要按列将高维的特征向量拆分成若干小的向量进行求解。



![img](https://pic3.zhimg.com/v2-649613856d724587cfe627ef1870a826_b.jpg)![img](https://pic3.zhimg.com/80/v2-649613856d724587cfe627ef1870a826_1440w.jpg)



并行计算总共会被分为两个并行化计算步骤和两个结果归并步骤：

**步骤一：**各节点并行计算点乘，计算 ![[公式]](https://www.zhihu.com/equation?tex=d_%7B%28r%2Cc%29%2Ck%2Ct%7D+%3D+W%5ET_%7Bc%2Ct%7DX_%7B%28r%2Cc%29%2Ck%7D+) ，其中 ![[公式]](https://www.zhihu.com/equation?tex=+k%3D1%2C2%E2%80%A6M%2Fm) ， ![[公式]](https://www.zhihu.com/equation?tex=d_%7B%28r%2Cc%29%2Ck%2Ct%7D) 表示第 t 次迭代中节点 ![[公式]](https://www.zhihu.com/equation?tex=%28r%2Cc%29) 上的第 k 个特征向量与特征权重分量的点乘， ![[公式]](https://www.zhihu.com/equation?tex=W_%7Bc%2Ct%7D) 为第 t 次迭代中特征权重向量在第 c 列节点上的分量； **步骤二：**对行号相同的节点归并点乘结果： 

![[公式]](https://www.zhihu.com/equation?tex=d_%7Br%2Ck%2Ct%7D%3DW%5ET_t+X_%7Br%2Ck%7D%3D%5Csum_%7Bc%3D1%7D%5En+d_%7B%28r%2Cc%29%2Ck%2Ct%7D%3D%5Csum_%7Bc%3D1%7D%5En+W_%7Bc%2Ct%7D%5ETX_%7B%28r%2Cc%29%2Ck%7D++%5C%5C) 

![img](https://pic3.zhimg.com/v2-6b5f725a2893d4fa28a2ddb17db4c756_b.jpg)![img](https://pic3.zhimg.com/80/v2-6b5f725a2893d4fa28a2ddb17db4c756_1440w.jpg)



**步骤三：**各节点独立算标量与特征向量相乘： 

![[公式]](https://www.zhihu.com/equation?tex=G_%7B%28r%2Cc%29%2Ct%7D%3D%5Csum_%7Bk%3D1%7D%5E%7BM%2Fm%7D%5B%5Csigma%28y_%7Br%2Ck%7Dd_%7Br%2Ck%2Ct%7D%29-1%5Dy_%7Br%2Ck%7DX_%7B%28r%2Cc%29%2Ck%7D++%5C%5C) 

![[公式]](https://www.zhihu.com/equation?tex=+G_%7B%28r%2Cc%29%2Ct%7D) 可以理解为由第 r 行节点上部分样本计算出的目标函数梯度向量在第 c 列节点上的分量。

**步骤四：**对列号相同的节点进行归并： 

![[公式]](https://www.zhihu.com/equation?tex=G_%7Bc%2Ct%7D%3D%5Csum_%7Br%3D1%7D%5Em+G_%7B%28r%2Cc%29%2Ct%7D++%5C%5C) 

![[公式]](https://www.zhihu.com/equation?tex=G_%7Bc%2Ct%7D) 就是目标函数的梯度向量 ![[公式]](https://www.zhihu.com/equation?tex=G_t+) 在第 c 列节点上的分量，对其进行归并得到目标函数的梯度向量： 

![[公式]](https://www.zhihu.com/equation?tex=G_t%3D%3CG_%7B1%2Ct%7D%2C...%2CG_%7Bc%2Ct%7D...G_%7Bn%2Ct%7D%3E+%5C%5C) 

这个过程如下图所示：



![img](https://pic1.zhimg.com/v2-a7cc0b79e62018e1a62dfcab5435e8f4_b.jpg)![img](https://pic1.zhimg.com/80/v2-a7cc0b79e62018e1a62dfcab5435e8f4_1440w.jpg)



所以并行计算 LR 的流程如下所示。



![img](https://pic1.zhimg.com/v2-d93c4826068dbca6030cb7ca895102a0_b.jpg)![img](https://pic1.zhimg.com/80/v2-d93c4826068dbca6030cb7ca895102a0_1440w.jpg)



所以并行 LR 实际上就是在求解损失函数最优解的过程中，针对寻找损失函数下降方向中的梯度方向计算作了并行化处理，而在利用梯度确定下降方向的过程中也可以采用并行化。

## 2. 与其他模型的对比

### 2.1 与线性回归

逻辑回归是在线性回归的基础上加了一个 Sigmoid 函数（非线形）映射，使得逻辑回归称为了一个优秀的分类算法。本质上来说，两者都属于广义线性模型，但他们两个要解决的问题不一样，逻辑回归解决的是分类问题，输出的是离散值，线性回归解决的是回归问题，输出的连续值。

我们需要明确 Sigmoid 函数到底起了什么作用：

- 线性回归是在实数域范围内进行预测，而分类范围则需要在 [0,1]，逻辑回归减少了预测范围；
- 线性回归在实数域上敏感度一致，而逻辑回归在 0 附近敏感，在远离 0 点位置不敏感，这个的好处就是模型更加关注分类边界，可以增加模型的鲁棒性。

### 2.2 与最大熵模型

逻辑回归和最大熵模型本质上没有区别，最大熵在解决二分类问题时就是逻辑回归，在解决多分类问题时就是多项逻辑回归。

首先进行符号定义：

1. ![[公式]](https://www.zhihu.com/equation?tex=%5Cpi+%28x%29_u) 表示，输入时 x，输出的 y=u 的概率；
2. A(u,v) 是一个指示函数，若 u=v，则 A(u,v)=1，否则 A(u,v)=0；
3. 我们的目标就是从训练数据中，学习得到一个模型，使得 ![[公式]](https://www.zhihu.com/equation?tex=+%5Cpi%28x%29_u) 最大化，也就是输入 x，预测结果是 y 的概率最大，也就是使得 ![[公式]](https://www.zhihu.com/equation?tex=+%5Cpi%28x%29_y) 最大。

对于逻辑回归而言： 

![[公式]](https://www.zhihu.com/equation?tex=P%28Y%3D1%7Cx%29+%3D+%5Cpi%28x%29_1+%3D%5Cdfrac%7Be%5E%7Bw+%5Ccdot+x%7D%7D%7B1%2Be%5E%7Bw+%5Ccdot+x%7D%7D+%5C%5C+++P%28Y%3D0%7Cx%29+%3D+%5Cpi%28x%29_0+%3D+1-%5Cpi%28x%29_1+%5C%5C)

我们这里可以用更泛化的形式来表示 π()： 

![[公式]](https://www.zhihu.com/equation?tex=+%5Cpi%28x%29_v%3D%5Cdfrac%7Be%5E%7Bw_v+%5Ccdot+x%7D%7D%7B%5Csum_%7Bu%3D1%7D%5Ek+e%5E%7Bw_u+%5Ccdot+x%7D%7D++%5C%5C) 

 回到我们的目标：令 ![[公式]](https://www.zhihu.com/equation?tex=%5Cpi%28x_i%29y_i) 最大，可以用极大似然估计的方法来求解。

![[公式]](https://www.zhihu.com/equation?tex=L%28w%29%3D%5Cprod_%7Bi%3D1%7D%5En+%5Cpi%28x_i%29%7By_i%7D+%5C%5C+lnL%28w%29%3D%5Csum_%7Bi%3D1%7D%5En+ln%28%5Cpi%28x_i%29%7By_i%7D%29++%5C%5C) 

然后我们求偏导：

![[公式]](https://www.zhihu.com/equation?tex=+%5Cfrac%7B%5Cpartial%7D%7B%5Cpartial+w_%7Bu%2Cj%7D%7DlnL%28w%29%3D...%3D%5Csum_%7Bi%3D1%2C%5C%3By_i%3Du%7D%5Enx_%7Bij%7D-%5Csum_%7Bi%3D1%7D%5Enx_%7Bij%7D%5Cpi%28x_i%29_u++%5C%5C) 

另偏导数为 0： 

![[公式]](https://www.zhihu.com/equation?tex=%5Csum_%7Bi%3D1%7D%5Enx_%7Bij%7D%5Cpi%28x_i%29_u%3D%5Csum_%7Bi%3D1%2C%5C%3By_i%3Du%7D%5Enx_%7Bij%7D%2C+%28for%5C%3Ball%5C%3B+u%2Cj%29++%5C%5C+)

使用 ![[公式]](https://www.zhihu.com/equation?tex=A%28u%2Cy_i%29+) 这个函数，我们可以重写等式： 

![[公式]](https://www.zhihu.com/equation?tex=%5Csum_%7Bi%3D1%7D%5Enx_%7Bij%7D%5Cpi%28x_i%29_u%3D%5Csum_%7Bi%3D1%7D%5En+A%28u%2Cy_i%29x_%7Bij%7D%2C+%28for%5C%3Ball%5C%3B+u%2Cj%29++%5C%5C) 

想要证明逻辑回归跟最大熵模型是等价的，那么，只要能够证明它们的 ![[公式]](https://www.zhihu.com/equation?tex=+%5Cpi+%28%29+) 是相同，结论自然就出来了。现在，我们不知道最大熵模型的 ![[公式]](https://www.zhihu.com/equation?tex=%5Cpi+%28%29) ，但是我们知道下面的一些性质： 

![[公式]](https://www.zhihu.com/equation?tex=+%5Cpi%28x%29_v%5Cgeq0+%5Cquad+always++%5C%5C+%5Csum_%7Bv%3D1%7D%5Ek%5Cpi%28x%29_v+%3D+1+%5Cquad+always+%5C%5C+%5Csum_%7Bi%3D1%7D%5Enx_%7Bij%7D%5Cpi%28x_i%29_u%3D%5Csum_%7Bi%3D1%7D%5En+A%28u%2Cy_i%29x_%7Bij%7D%2C+%5Cquad%28for%5C%3Ball%5C%3B+u%2Cj%29+%5C%5C) 

利用信息论，我们可以得到 ![[公式]](https://www.zhihu.com/equation?tex=%5Cpi+%28%29) 的**熵**，定义如下： 

![[公式]](https://www.zhihu.com/equation?tex=-%5Csum_%7Bv%3D1%7D%5Ek%5Csum_%7Bi%3D1%7D%5En%5Cpi%28x_i%29vlog%5B%5Cpi%28x_i%29_v%5D++%5C%5C)

现在，我们有了**目标**： ![[公式]](https://www.zhihu.com/equation?tex=%5Csum+%5Cpi%28%29) 最大，也有了上面的4个**约束条件**。求解约束最优化问题，可以通过拉格朗日乘子，将约束最优化问题转换为**无约束最优化**的对偶问题。我们的拉格朗日式子可以写成如下：

![[公式]](https://www.zhihu.com/equation?tex=L%3D%5Csum_%7Bj%3D1%7D%5Em%5Csum_%7Bv%3D1%7D%5Ekw_%7Bv%2Cj%7D%28%5Csum_%7Bi%3D1%7D%5En%5Cpi%28x_i%29_vx_%7Bij%7D-A%28v%2Cy_i%29x_%7Bij%7D%29+%5C%5C+%2B%5Csum_%7Bv%3D1%7D%5Ek%5Csum_%7Bi%3D1%7D%5En%5Cbeta_i%28%5Cpi%28x_i%29_v-1%29++%5C%5C+-%5Csum_%7Bv%3D1%7D%5Ek%5Csum_%7Bi%3D1%7D%5En+%5Cpi%28x_i%29_vlog%5B%5Cpi%28x_i%29_v%5D) 

对 L 求偏导，得到： 

![[公式]](https://www.zhihu.com/equation?tex=%5Cfrac%7B%5Cpartial%7D%7B%5Cpartial+%5Cpi%28x_i%29_u%7DL%3Dw_u+%5Ccdot+x_i%2B%5Cbeta_i-log%5B%5Cpi%28x_i%29_u%5D-1+%5C%5C) 

令偏导 = 0，得到：

![[公式]](https://www.zhihu.com/equation?tex=w_u+%5Ccdot+x_i%2B%5Cbeta_i-log%5B%5Cpi%28x_i%29_u%5D-1%3D0+%5C%5C)

从而得到： 

![[公式]](https://www.zhihu.com/equation?tex=%5Cpi%28x_i%29_u%3De%5E%7Bw_u+%5Ccdot+x_i%2B%5Cbeta_i-1%7D++%5C%5C) 

因为有约束条件：

![[公式]](https://www.zhihu.com/equation?tex=%5Csum_%7Bv%3D1%7D%5Ek+%5Cpi%28x%29_v+%3D+1++%5C%5C) 

所以：

![[公式]](https://www.zhihu.com/equation?tex=%5Csum_%7Bv%3D1%7D%5Eke%5E%7Bw_v+%5Ccdot+x_i%2B%5Cbeta_i-1%7D%3D1+%5C%5C) 

因此，可以得到：

![[公式]](https://www.zhihu.com/equation?tex=e%5E%5Cbeta%3D%5Cfrac%7B1%7D%7B%5Csum_%7Bv%3D1%7D%5Eke%5E%7Bw_v+%5Ccdot+x_i-1%7D%7D+%5C%5C) 

把 ![[公式]](https://www.zhihu.com/equation?tex=e%5E%5Cbeta) 代入  ![[公式]](https://www.zhihu.com/equation?tex=%5Cpi+%28%29) ，并且简化一下式子：  

![[公式]](https://www.zhihu.com/equation?tex=%5Cpi%28x%29_u%3D%5Cfrac%7Be%5E%7Bw_u%5Ccdot+x%7D%7D%7B%5Csum_%7Bv%3D1%7D%5Ek+e%5E%7Bw_v+%5Ccdot+x%7D%7D+%5C%5C) 

这就是逻辑回归中提到的那个泛化的式子，这就证明了逻辑回归是最大熵模型的一个特殊例子。到此，逻辑回归与最大熵模型的关系就解释完毕了。

### 2.3 与 SVM

相同点：

- 都是分类算法，本质上都是在找最佳分类超平面；
- 都是监督学习算法；
- 都是判别式模型，判别模型不关心数据是怎么生成的，它只关心数据之间的差别，然后用差别来简单对给定的一个数据进行分类；
- 都可以增加不同的正则项。

不同点：

- LR 是一个统计的方法，SVM 是一个几何的方法；
- SVM 的处理方法是只考虑 Support Vectors，也就是和分类最相关的少数点去学习分类器。而逻辑回归通过非线性映射减小了离分类平面较远的点的权重，相对提升了与分类最相关的数据点的权重；
- 损失函数不同：LR 的损失函数是交叉熵，SVM 的损失函数是 HingeLoss，这两个损失函数的目的都是增加对分类影响较大的数据点的权重，减少与分类关系较小的数据点的权重。对 HingeLoss 来说，其零区域对应的正是非支持向量的普通样本，从而所有的普通样本都不参与最终超平面的决定，这是支持向量机最大的优势所在，对训练样本数目的依赖大减少，而且提高了训练效率；
- LR 是参数模型，SVM 是非参数模型，参数模型的前提是假设数据服从某一分布，该分布由一些参数确定（比如正太分布由均值和方差确定），在此基础上构建的模型称为参数模型；非参数模型对于总体的分布不做任何假设，只是知道总体是一个随机变量，其分布是存在的（分布中也可能存在参数），但是无法知道其分布的形式，更不知道分布的相关参数，只有在给定一些样本的条件下，能够依据非参数统计的方法进行推断。所以 LR 受数据分布影响，尤其是样本不均衡时影响很大，需要先做平衡，而 SVM 不直接依赖于分布；
- LR 可以产生概率，SVM 不能；
- LR 不依赖样本之间的距离，SVM 是基于距离的；
- LR 相对来说模型更简单好理解，特别是大规模线性分类时并行计算比较方便。而 SVM 的理解和优化相对来说复杂一些，SVM 转化为对偶问题后，分类只需要计算与少数几个支持向量的距离，这个在进行复杂核函数计算时优势很明显，能够大大简化模型和计算。

### 2.4 与朴素贝叶斯

朴素贝叶斯和逻辑回归都属于分类模型，当朴素贝叶斯的条件概率 ![[公式]](https://www.zhihu.com/equation?tex=P%28X%7CY%3Dc_k%29) 服从高斯分布时，它计算出来的 P(Y=1|X) 形式跟逻辑回归是一样的。

两个模型不同的地方在于：

- 逻辑回归是判别式模型 p(y|x)，朴素贝叶斯是生成式模型 p(x,y)：判别式模型估计的是条件概率分布，给定观测变量 x 和目标变量 y 的条件模型，由数据直接学习决策函数 y=f(x) 或者条件概率分布 P(y|x) 作为预测的模型。判别方法关心的是对于给定的输入 x，应该预测什么样的输出 y；而生成式模型估计的是联合概率分布，基本思想是首先建立样本的联合概率概率密度模型 P(x,y)，然后再得到后验概率 P(y|x)，再利用它进行分类，生成式更关心的是对于给定输入 x 和输出 y 的生成关系；
- 朴素贝叶斯的前提是条件独立，每个特征权重独立，所以如果数据不符合这个情况，朴素贝叶斯的分类表现就没逻辑会好了。

## 3. 模型细节

### 3.1 为什么适合离散特征

我们在使用逻辑回归的时候很少会把数据直接丢给 LR 来训练，我们一般会对特征进行离散化处理，这样做的优势大致有以下几点：

1. 离散后稀疏向量内积乘法运算速度更快，计算结果也方便存储，容易扩展；
2. 离散后的特征对异常值更具鲁棒性，如 age>30 为 1 否则为 0，对于年龄为 200 的也不会对模型造成很大的干扰；
3. LR 属于广义线性模型，表达能力有限，经过离散化后，每个变量有单独的权重，这相当于引入了非线性，能够提升模型的表达能力，加大拟合；
4. 离散后特征可以进行特征交叉，提升表达能力，由 M+N 个变量编程 M*N 个变量，进一步引入非线形，提升了表达能力；
5. 特征离散后模型更稳定，如用户年龄区间，不会因为用户年龄长了一岁就变化；

总的来说，特征离散化以后起到了加快计算，简化模型和增加泛化能力的作用。

### 3.2 为什么不用平方误差

假设目标函数是 MSE，即：

![[公式]](https://www.zhihu.com/equation?tex=L%3D%5Cfrac%7B%28y-%5Chat%7By%7D%29%5E2%7D%7B2%7D+%5C%5C+%5Cfrac%7B%5Cpartial+L%7D%7B%5Cpartial+w%7D%3D%28%5Chat%7By%7D-y%29%5Csigma%27%28w%5Ccdot+x%29x+%5C%5C) 

这里 Sigmoid 的导数项为： 

![[公式]](https://www.zhihu.com/equation?tex=%5Csigma%5E%7B%27%7D%28w+%5Ccdot+x%29%3Dw%5Ccdot+x%281-w+%5Ccdot+x%29++%5C%5C) 

根据 w 的初始化，导数值可能很小（想象一下 Sigmoid 函数在输入较大时的梯度）而导致收敛变慢，而训练途中也可能因为该值过小而提早终止训练（梯度消失）。

另一方面，交叉熵的梯度如下，当模型输出概率偏离于真实概率时，梯度较大，加快训练速度，当拟合值接近于真实概率时训练速度变缓慢，没有 MSE 的问题。 

![](https://www.zhihu.com/equation?tex=g%5E%7B%27%7D%3D%5Csum_%7Bi%3D1%7D%5E%7BN%7D+x_%7Bi%7D%28y_%7Bi%7D-p%28x_%7Bi%7D%29%29++%5C%5C) 

### 3.3 L1正则存在的一些缺点

使用L1正则使得模型中的一些参数会变为0，从而得到一个sparse solution的解，但是使用L1正则的时候会存在一个问题，就是模型最终的好坏是由少数的几个重要特征决定的，比如w1，w2,w3，在实际情况中假设很可能存在w1,w2,w3之间存在比较高的相关性，这时候使用L1正则的话是在W1,W2,W3之间随机选择一个比如w1，但是选出来的W1在这三个参数中不一定会是最好的。

对于这个问题可以通过在L1正则的基础上再加上L2正则来解决。

## 4 引用

1. [L1 正则化与 L2 正则化](https://zhuanlan.zhihu.com/p/35356992)

2. [L1 相比于 L2 为什么容易获得稀疏解？](https://www.zhihu.com/question/37096933/answer/70426653)

3. [参数模型和非参数模型](https://link.zhihu.com/?target=https%3A//blog.csdn.net/sinat_27652257/article/details/80543604)

4. [SVM 和 Logistic 回归分别在什么情况下使用？](https://www.zhihu.com/question/21704547)

5. [Linear SVM 和 LR 有什么异同？](https://www.zhihu.com/question/26768865)

6. [Logistic Regression (LR) 详解](https://link.zhihu.com/?target=https%3A//blog.csdn.net/songbinxu/article/details/79633790%23%E5%9B%9Blr-%E6%AD%A3%E5%88%99%E5%8C%96)

7. [逻辑回归 LR 的特征为什么要先离散化](https://link.zhihu.com/?target=https%3A//blog.csdn.net/yang090510118/article/details/39478033)

8. [并行逻辑回归](https://link.zhihu.com/?target=http%3A//blog.sina.com.cn/s/blog_6cb8e53d0101oetv.html)

9. [连续特征的离散化](https://www.zhihu.com/question/31989952/answer/54184582)

   