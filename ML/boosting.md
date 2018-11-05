##  boosting
提升(boosting)方法通过改变训练样本的权重学习多个分类器，并将这些分类器进行线性组合，提高分类的性能。 

###  1. boosting的基本思路
boosting是怎么出现的？因为在实际中发现弱分类器比发现强分类器更容易，那么有没有一种方法能将弱分类器提升成强分类器呢？也就是将多个**弱分类器**进行**线性组合**使得其摇身一变成**强分类器**，可以通过**boosting**。
那么现在有两个问题

1.  如何根据给定的数据集$D$训练出多个弱分类器呢？
2. 如何将多个若分类器进行线性组合呢？

接下来通过boosting的代表性算法Adaboost来回答这两个问题。

**首先**大多数的提升算法是通过改变训练数据的概率分布(训练数据的权值分布)，通过对不同分布数据集训练出多个弱分类器。那么Adaboost是如何改变数据集的概率分布也就是样本的权重呢？

- Adaboost的做法是通过**提高**那些被**前一轮弱分类器错分**的样本的权重，**降低**那些被**分对**样本的权值。

**伪代码如下**
      

  输入:训练数据集$T= \lbrace{(x_1,y_1),(x_2,y_2),....,(x_n,y_n) \rbrace}，y_i \in {-1,+1}$; 弱学习算法；

  输入:训练数据集$T= \lbrace{(x_1,y_1),(x_2,y_2),....,(x_n,y_n) \rbrace}，y_i \in \lbrace{-1,+1\rbrace}$; 弱学习算法；

  
  输出：最终分类器$G(x)$
  
  (1)初始化训练数据的权值分布
$$
D_1 = (w_{11},...w_{1i},..w_{iN}),w_{1i} = \frac{1}{N},i=1,2,...N
$$
(2) for m=1,2,....M
(a)使用具有权值分布$D_m$的训练数据集学习，得到基本分类器
$$
G_m(x): \chi \to \lbrace{-1,+1 \rbrace}
$$
(b)计算$G_m(x)$在训练数据集上的分类误差率
$$
e_m = P(G_m(x_i) \not= y_i ) = \sum_{i=1}^N{w_{mi}I(G_m(x_i) \not= y_i)}
$$

(c)计算$G_m(x)$的系数
$$
\alpha_{m} = \frac{1}{2}log\frac{1-e_m}{e_m}
$$
(d)更新训练数据集的权值分布
$$
\begin{align}
D_{m+1} = (w_{m+1,1},...w_{m+1,i},...w_{m+1,N}) \\
W_{m+1,i} = \frac{w_{m,i}}{Z_m}exp(-\alpha_my_iG_m(x_i))
\end{align}
$$
$Z_m$是一个归一化因子
$$
Z_m = \sum_{i=1}^N{w_{m,i}} {exp(-\alpha_my_iG_m(x_i)}
$$
（3）构建基本分类器的线性组合
$$
f(x) = \sum_{i=1}^m{\alpha_m}{G_m(x)}
$$
得到最终的分类器
$$
G(x) = sign(f(x)) = sign \left (\sum_{i=1}^m{\alpha_m}{G_m(x)} \right)
$$
线性组合$f(x)$实现了M个基本分类器的加权表决，系数$\alpha_m$表示基本分类器 $G_m(x)$的在表决时候的话语权。所以随着迭代，后面的弱分类器的权重越来越大的



## 2. 前向分布算法
Adaboost可以认为是加法模型的一种特例。认为Adaboost算法是模型为加法模型，损失函数为指数损失，学习算法为前向分布算法。

加法模型如下：
$$
f(x) = \sum_{m =1}^M{\beta_m}{b(x,\gamma_m)}
$$
在给定训练数据及损失函数$L(y,f(x))$的条件下，极小化如下损失:
$$
\min_{\beta_m,\gamma_m}\sum_{i=1}^N L \left(y_i,\sum_{m=1}^M{\beta_mb(x_i;\gamma_m)} \right)           （1）
$$
由公式可知，再计算LOSS时我们需要同时求解 m=1到M的所有基函数参数，前向分布算法通过每次只学习一个基函数及其系数来使loss逐步逼近（1）式。

**具体地**，每步只需优化如下损失函数:
$$
\min_{\beta,\gamma}{\sum_{i=1}^N{L(y_i,\beta b(x_i;\gamma))}}
$$

**伪代码如下**
      
  输入:训练数据集$T= \lbrace{(x_1,y_1),(x_2,y_2),....,(x_n,y_n) \rbrace}$; 损失函数$L(y,f(x))$；基函数集合$\lbrace{b(x;\gamma) \lbrace}$
  
  输出：加法模型$f(x)$

(1)初始化$f_0(x)=0$

(2)$for  m =1,2,3,...M$

(a)极小化损失函数
$$
(\beta_m,\gamma_m) = arg\min_{\beta,\gamma}{\sum_{i=1}^N{L(y_i,f_{m-1}(x_i)+\beta b(x_i;\gamma))}}
$$
得到参数$\beta_m,\gamma_m$

(b)更新
$$
f_m(x) = f_{m-1}(x)+\beta_m b(x_i;\gamma_m)
$$

(3)得到加法模型
$$
f_m(x) = f_M(x) = \sum_{m=1}^M{\beta_m b(x_i;\gamma_m)}
$$

