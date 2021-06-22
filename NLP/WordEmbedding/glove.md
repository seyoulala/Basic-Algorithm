## **基本思想**

要讲GloVe模型的思想方法，我们先介绍两个其他方法：

一个是基于奇异值分解（SVD）的[LSA](https://link.zhihu.com/?target=https%3A//en.wikipedia.org/wiki/Latent_semantic_analysis)算法，该方法对term-document矩阵（矩阵的每个元素为tf-idf）进行奇异值分解，从而得到term的向量表示和document的向量表示。此处使用的tf-idf主要还是term的全局统计特征。

另一个方法是[word2vec](https://link.zhihu.com/?target=https%3A//www.cnblogs.com/Weirping/p/(http%3A//blog.csdn.net/itplus/article/details/37969519))算法，该算法可以分为skip-gram 和 continuous bag-of-words（CBOW）两类,但都是基于局部滑动窗口计算的。即，该方法利用了局部的上下文特征（local context）

LSA和word2vec作为两大类方法的代表，一个是利用了全局特征的矩阵分解方法，一个是利用局部上下文的方法。

**GloVe模型就是将这两中特征合并到一起的，即使用了语料库的全局统计（overall statistics）特征，也使用了局部的上下文特征（即滑动窗口）。为了做到这一点GloVe模型引入了Co-occurrence Probabilities Matrix。**

首先引入word-word的共现矩阵XX，

![img](https://pic1.zhimg.com/v2-714cc481b28d04a33b5235652184b960_b.jpg)

![img](https://pic2.zhimg.com/v2-f2f19c44ba6af9af6f699157101d658d_b.jpg)

讲到这里，没有一个例子来说明，那就真是一件很遗憾的事情了，所以必须来个实例，实例永远是帮助理解最好的方式。

**统计共现矩阵**

![img](https://pic1.zhimg.com/v2-f8e65b16ab7a7c01b8e3f1be0d063e64_b.jpg)

![img](https://pic1.zhimg.com/v2-c2a077f234433b37cf4e0962a9814910_b.jpg)

![img](https://pic2.zhimg.com/v2-53c96f5b67884a3ad808b753a7e07179_b.jpg)

**模型推导**

**以下内容看似公式很多，其实挺容易理解的，耐心看**

![img](https://pic2.zhimg.com/v2-33e51493fa8e2170bba8df468e41e685_b.jpg)

![img](https://pic2.zhimg.com/v2-11fe585fa53b9e54d94c9c996187bf89_b.jpg)

![img](https://pic4.zhimg.com/v2-fef86f8c0487368408f20e453727104b_b.jpg)