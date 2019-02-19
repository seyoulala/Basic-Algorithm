Date | Title | Author |  Confirmer  | Version
:-------:  | :-------: |:-------: | :-------:  | :-------: 
2018-08-17 | 评分卡技术详细流程 | Xu | Xu、Blair | ~ | 1.0

# 评分A卡详细的分析流程与理论基础(详版)

**本文将以金融评分卡模型为例，讲解一整套 ![lr](https://www.zhihu.com/equation?tex=lr) 配套的数据处理流程，包括数据获取，EDA (探索性数据分析)，数据预处理，到变量筛选，![lr](https://www.zhihu.com/equation?tex=lr) 模型的开发和评估，生成评分卡模型**

[gitlab代码地址](http://192.168.0.12/data/smy_xgboost/tree/master/LR)

我会重点从以下三个方面来介绍评分卡：
- 用户的属性有很多，但是评分卡模型使用的字段在30个以下，这些字段是如何挑选出来的
- 评分法卡模型采用的是对每个字段的分段进行评分，那么怎样对评分卡进行有效分段呢？
- 怎样对字段的每个分段进行评分呢？这个评分是怎么来的？
## **1\. 评分卡模型的背景知识**
信用评分卡模型是最常见的金融风控手段之一，它是指根据客户的各种属性和行为数据，利用一定的信用评分模型，对客户进行信用评分，据此决定是否给予授信以及授信的额度和利率，从而识别和减少在金融交易中存在的交易风险。

评分卡模型在不同的业务阶段体现的方式和功能也不一样。按照借贷用户的借贷时间，评分卡模型可以划分为以下三种：

*   贷前：申请评分卡（Application score card），又称为A卡
*   贷中：行为评分卡（Behavior score card），又称为B卡
*   贷后：催收评分卡（Collection score card），又称为C卡

以下为评分卡模型的示意图：

<img src="/scoring_card/images/v2-1c61edf5d441089e24160a5e363f44ae_hd.jpg" width="600" />


## **2\. 评分卡模型的开发**

典型的开发流程:
![](https://pic1.zhimg.com/80/v2-db979466aa6abc3f74b917b21b88a76f_hd.jpg)
## **2.1数据获取**
主要的数据获取途径：
- 金融机构自身字段：例用户的年龄，户籍，性别，收入，负债比，在本机构的借款和还款行为等；
- 第三方机构的数据：如用户在其他机构的借贷行为，用户的消费行为数据等。

## 2.2 **EDA（探索性数据分析）**

该步骤主要是获取数据的大概情况，例如每个字段的缺失值情况、异常值情况、平均值、中位数、最大值、最小值、分布情况等。以便制定合理的数据预处理方案
## 2.3 **数据预处理**
数据预处理主要包括数据清洗，变量分箱和 WOE 编码三个步骤。
## 2.3.1 数据清洗

数据清洗主要是对原始数据中脏数据，缺失值，异常值进行处理。关于对缺失值和异常值的处理，我们采用的方法非常简单粗暴，即删除缺失率超过某一阈值（阈值自行设定，可以为30%，50%，90%等）的变量，将剩余变量中的缺失值和异常值作为一种状态 。（作为-1）


## 2.3.2 **变量分箱**
在这里我们回答第二个问题评分卡是怎样对变量进行分段的，评分卡模型通过对变量进行分箱来实现变量的分段。那么什么是分箱呢？以下为分箱的定义：
- 对连续变量进行分段离散化
- 将多状态的离散变量进行合并，减少离散变量的状态数

常见的分箱类型：

<img src="/scoring_card/images/v2-31cba8dc3a08bf93a79f0c1c24291c37_hd.jpg" width="500" />

这里我主要讲一下在分箱过程过用到过的分箱方法
1. 等频分箱：把自变量的值从小到大排序，按照自变量的个数等分为K部分，然后每部分都作为一个箱子
2. ChiMerge分箱：基本思想是如果两个相邻区间有类似的分布，则这两个区间合并，否则它们应该分开，Chimerge通常采用卡方值来衡量两相邻区间的类分布情况。

![merge分箱示意图](https://pic1.zhimg.com/80/v2-5cc1a90cfe6a418b61b85aff77383e4f_hd.jpg)

Chimerge的具体算法如下：

1\. 输入：分箱的最大区间数 ![n](https://www.zhihu.com/equation?tex=n)

2\. 初始化

*   连续值按升序排列，离散值先转化为坏客户的比率，然后再按升序排列；
*   为了减少计算量，对于状态数大于某一阈值 (建议为100) 的变量，利用等频分箱进行粗分箱。
*   若有缺失值，则缺失值单独作为一个分箱。

3\. 合并区间

*   计算每一对相邻区间的卡方值；
*   将卡方值最小的一对区间合并

![](https://www.zhihu.com/equation?tex=X%5E2+%3D+%5Csum_%7Bi%3D1%7D%5E2+%5Csum_%7Bj%3D1%7D%5E2%5Cfrac%7B%28A_%7Bij%7D+-+E_%7Bij%7D%29%5E2%7D%7BE_%7Bij%7D%7D+%5C%5C)

![](https://www.zhihu.com/equation?tex=A_%7Bij%7D)：第 i 区间第 j 类的实例数量 ![](https://www.zhihu.com/equation?tex=E_%7Bij%7D) ： ![](https://www.zhihu.com/equation?tex=E_%7Bij%7D+%3D+%5Cfrac%7BN_i+%7D%7BN%7D%5Ctimes+C_j) ，
![N](https://www.zhihu.com/equation?tex=N) 是合并区间的样本数， ![N_i](https://www.zhihu.com/equation?tex=N_i) 是第 ![i](https://www.zhihu.com/equation?tex=i) 组的样本数， ![C_j](https://www.zhihu.com/equation?tex=C_j) 是第 ![j](https://www.zhihu.com/equation?tex=j) 类样本在合并区间的样本数。

*   重复以上两个步骤，直到分箱数量不大于 ![n](https://www.zhihu.com/equation?tex=n)

4\. 分箱后处理

*   对于坏客户比例为 0 或 1 的分箱进行合并 (一个分箱内不能全为好客户或者全为坏客户)。
*   对于分箱后的箱子检验其bad_rate是否单调，若不单调合并箱子，直到单调为止
*   对于分箱后某一箱样本占比小于%5 的箱子进行合并。

5\. 输出：分箱后的数据和分箱区间。

**分箱的优势**：

1. 特征分箱后可以有效处理特征中的缺失值和异常值，
2. 特征分箱后可以简化逻辑回归模型，降低模型过拟合的风险，提高模型的泛化能力
3. 分箱后才可以使用标准的评分卡格式，即对不同的分段进行评分

## 2.3.3 WOE编码

分箱之后我们便得到了一系列的离散变量，下面需要对变量进行编码，将离散变量转化为连续变量。WOE编码是评分卡模型常用的编码方式。
WOE 称为证据权重(weight of evidence)，是一种有监督的编码方式，将预测类别的集中度的属性作为编码的数值。对于自变量第 $i$ 箱的WOE值为：
![](https://www.zhihu.com/equation?tex=WOE_i+%3D%5Ctext%7Blog%7D%28%5Cfrac%7Bp_%7Bi_1%7D%7D%7Bp_%7Bi_0%7D%7D%29+%3D+%5Ctext%7Blog%7D%28%5Cfrac%7B%5C%23B_i%2F%5C%23B_T%7D%7B%5C%23G_i%2F%5C%23G_T%7D%29+%5C%5C) 

![p_{i_1}](https://www.zhihu.com/equation?tex=p_%7Bi_1%7D) 是第 ![i](https://www.zhihu.com/equation?tex=i) 箱中坏客户占所有坏客户比例

![p_{i_0}](https://www.zhihu.com/equation?tex=p_%7Bi_0%7D) 是第 ![i](https://www.zhihu.com/equation?tex=i) 箱中好客户占所有好客户比例

![\#B_i](https://www.zhihu.com/equation?tex=%5C%23B_i) 是第 ![i](https://www.zhihu.com/equation?tex=i) 箱中坏客户人数

![\#G_i](https://www.zhihu.com/equation?tex=%5C%23G_i) 是第 ![i](https://www.zhihu.com/equation?tex=i) 箱中好客户人数

![\#B_T](https://www.zhihu.com/equation?tex=%5C%23B_T) 是所有坏客户人数

![\#G_T](https://www.zhihu.com/equation?tex=%5C%23G_T) 是所有好客户人数

WOE可以理解为当前分箱中坏客户和好客户的比值，和所有样本中这个比值的差异 (**也就是我们随机的坏客户和好客户的比例**)。WOE越大，这种差异越大，当前分组里的坏客户的可能性就越大，WOE越小，差异越小，这个分组里的样本响应的可能性就越小。当分箱中坏客户和好客户的比例等于随机坏客户和好客户的比值时，说明这个分箱没有预测能力，即WOE=0。

WOE具体计算过程:

![](https://pic3.zhimg.com/80/v2-c8bc15a546c4f52456268ab24e6d48dd_hd.jpg)

**总结一下WOE编码的优势：**

*   可提升模型的预测效果
*   将自变量规范到同一尺度上
*   WOE能反映自变量取值的贡献情况
*   有利于对变量的每个分箱进行评分
*   转化为连续变量之后，便于分析变量与变量之间的相关性
*   与独热向量编码相比，可以保证变量的完整性，同时避免稀疏矩阵和维度灾难
## 2.4 变量筛选

之前我们说到过用户的属性有千千万万个维度，而评分卡模型所选用的字段在30个以下，那么怎样挑选这些字段呢？

挑选入模变量需要考虑很多因素，比如：变量的预测能力，变量之间的线性相关性，变量的简单性（容易生成和使用），变量的强壮性（不容易被绕过），变量在业务上的可解释性（被挑战时可以解释的通）等等。其中最主要和最直接的衡量标准是变量的预测能力和变量的线性相关性。本文主要探讨基于变量预测能力的单变量筛选，变量两两相关性分析，变量的多重共线性分析

## 2.4.1 单变量筛选

单变量的筛选基于变量预测能力，常用方法：

*   **基于IV值的变量筛选**
*   **基于stepwise的变量筛选**
*   **基于特征重要度的变量筛选：RF, GBDT…**
*   **基于LASSO正则化的变量筛选**

**1\. 基于IV值的变量筛选**

IV称为信息价值(information value)，是目前评分卡模型中筛选变量最常用的指标之一，自变量的IV值越大，表示自变量的预测能力越强。类似的指标还有信息增益、基尼(gini)系数等。常用判断标准如下：

![](https://pic1.zhimg.com/80/v2-7bb7434331b8ab5a48c83539a349365e_hd.jpg)

![](https://pic2.zhimg.com/80/v2-66525b302bcacf7b616e2b012487a75d_hd.jpg)
## 2.4.2 变量相关性分析

**1 变量两两相关性分析**

对于自变量 ![](https://www.zhihu.com/equation?tex=X_1%2C+X_2)，如果存在常数 ![](https://www.zhihu.com/equation?tex=c_0%2Cc_1%2Cc_2) 使得以下线性等式近似成立: 

![](https://www.zhihu.com/equation?tex=c_1X_1+%2B+c_2X_2+%5Capprox+c_0+%5C%5C)

称自变量 ![](https://www.zhihu.com/equation?tex=X_1%2C+X_2) 具有较强的线性相关性。

两变量间的线性相关性可以利用皮尔森相关系数来衡量。系数的取值为 
![[-1.0,1.0]](https://www.zhihu.com/equation?tex=%5B-1.0%2C1.0%5D) ，
相关系数越接近0的说明两变量线性相关性越弱，越接近1或-1两变量线性相关性越强。

![](https://www.zhihu.com/equation?tex=r_%7BX%2CY%7D%3D%5Cfrac%7Bcov%28X%2CY%29%7D%7B%5Csigma_X%5Csigma_Y%7D%3D%5Cfrac%7BE%28%28X-%5Cbar+X%29%28Y-%5Cbar+Y%29%29%7D%7B%5Csqrt%7B%5Csum%5Climits_%7Bi%3D1%7D%5En%28X_i-%5Cbar+X%29%5E2%7D+%5Csqrt%7B+%5Csum%5Climits_%7Bi%3D1%7D%5En%28Y_i-%5Cbar+Y%29%5E2%7D%7D+%3D+%5Cfrac%7BE%28XY%29-E%28X%29%28Y%29%7D%7B%5Csqrt%7BE%28X%5E2%29-E%5E2%28X%29%7D%5Csqrt%7BE%28Y%5E2%29-E%5E2%28Y%29%7D%7D+%5C%5C)

当两变量间的相关系数大于阈值时（一般阈值设为 0.7 或 0.4），剔除IV值较低的变量，或分箱严重不均衡的变量。

**2. 变量的多重共线性分析**

对于自变量 ![](https://www.zhihu.com/equation?tex=X_1%2C+X_2%2C+%5Ccdots+%2C+X_n) ，如果存在常数 ![](https://www.zhihu.com/equation?tex=c_0%2Cc_1%2Cc_2%2C+%5Ccdots%2C+c_n) 使得以下线性等式近似成立: 

![](https://www.zhihu.com/equation?tex=c_1X_1+%2B+c_2X_2+%2B+%5Ccdots+%2B+c_nX_n+%5Capprox+c_0+%5C%5C) 

称自变量 ![](https://www.zhihu.com/equation?tex=X_1%2C+X_2%2C+%5Ccdots+%2C+X_n)具有较强的多重共线性。

通常用 VIF 值来衡量一个变量和其他变量的多重共线性：

![](https://www.zhihu.com/equation?tex=VIF_i+%3D+%5Cfrac%7B1%7D%7B1-R%5E2_i%7D+%5C%5C)

当某个变量的 VIF 大于阈值时（一般阈值设为10 或 7），需要逐一剔除解释变量。当剔除掉 ![X_k](https://www.zhihu.com/equation?tex=X_k)时发现VIF低于阈值，从 ![{X_k，X_i}](https://www.zhihu.com/equation?tex=%7BX_k%EF%BC%8CX_i%7D) 中剔除IV值较低的一个。

**总结一下变量筛选的意义：**

1.  剔除跟目标变量不太相关的特征
2.  消除由于线性相关的变量，避免特征冗余
3.  减轻后期验证、部署、监控的负担
4.  保证变量的可解释性

## 2.5 构建逻辑回归模型

主要包括构建初步的逻辑回归模型，根据p-value进行变量筛选，根据各个变量的系数符号进行筛选，得到最终的逻辑回归模型。

以下为几种常用模型的优势和劣势对比：

![](https://pic4.zhimg.com/80/v2-611ec9e91d3b985c7aca785e48f95e7c_hd.jpg)

## 2.5.1 根据系数符号进行筛选

检查逻辑回归模型中各个变量的系数，如果所有变量的系数均为正数，模型有效。假如有一些变量的系数出现了负数，说明有一些自变量的线性相关性较强，需要进一步进行变量筛选。通常的做法是：

*   综合考虑变量的IV值和业务的建议，按照变量的优先级进行降序排列；
*   选择优先级最高的4-5个基本变量；
*   按优先级从高到低逐渐添加变量，当新添加的变量之后，出现系数为负的情况，舍弃该变量；
*   直到添加最后一个变量。

## 2.5.2 根据p-value进行筛选

p-value是假设检验的里面的概念。模型假设某自变量与因变量线性无关，p-value可以理解为该假设成立的可能性 (便于理解，不太准确)。一般，当p-value大于阈值时，表示假设显著，即自变量与因变量线性无关；当p-value小于阈值时，表示假设不显著，即自变量与因变量线性相关。阈值又称为显著性水平，通常取0.05。

因此当某个字段的 p-value 大于0.05时，应该删除此变量。
## 2.6模型评价
## 2.6.1 混淆矩阵，TPR (Recal)，FPR

TPR (或Recall) 为坏客户的查全率，表示被模型抓到的坏客户占总的坏客户的比例，表达式为：

![](https://www.zhihu.com/equation?tex=TPR%3D+%5Cfrac+%7BTP%7D+%7BTP%2BFN%7D+%5C%5C) 

FPR 为好客户误判率，表示好客户中倍模型误误判的比例，表达式为：

![](https://www.zhihu.com/equation?tex=FPR+%3D+%5Cfrac+%7BFP%7D%7BFP%2BTN%7D+%5C%5C) 

可以把TPR看做模型的收益，FPR看做模型付出的代价。如果一个模型 TPR越大，表示模型能够抓到的坏客户比例越大，即收益越大；FPR越大，表示模型能够将好客户误抓的比例越大，即代价越大
## 2.6.2 AUC

AUC 表示模型对任意坏客户的输出结果为大于模型对任意好客户的输出结果的概率。AUC的取值范围在0.5和1之间，AUC 越大，表示模型预测性能越好。

## 2.6.3 KS值

KS 值表示了模型区分好坏客户的能力。其实质是![TPR-FPR](https://www.zhihu.com/equation?tex=TPR-FPR)随好坏客户阈值变化的最大值。KS 的取值范围在0.5和1之间，值越大，模型的预测准确性越好。一般，KS > 0.4 即认为模型有比较好的预测性能。
## 2.7 转换成评分卡
![](https://pic1.zhimg.com/80/v2-fec98ff9de65d835a5be217f01f678a5_hd.jpg)

从以上公式中，我们发现每个分箱的评分都可以表示为 ![-B(\theta_i w_{ij} ) ](https://www.zhihu.com/equation?tex=-B%28%5Ctheta_i+w_%7Bij%7D+%29+) ，也就是说影响每个分箱的因素包括三部分，分别为参数 ![B](https://www.zhihu.com/equation?tex=B) ，变量系数 ![\theta_i](https://www.zhihu.com/equation?tex=%5Ctheta_i) ，和对应分箱的WOE编码 ![w_{ij}](https://www.zhihu.com/equation?tex=w_%7Bij%7D) 。
## 2.8 小结

最后我们再来回答最初的三个问题作为本文的小结：

1\. 用户的属性有千千万万个维度，而评分卡模型所选用的字段在30个以下，那么怎样挑选这些字段呢？

*   变量预测能力筛选，
*   变量相关性分析（包括两两相关性分析，多重共线性分析），
*   根据p-value筛选，
*   根据变量的系数符号进行筛选。

2\. 评分法卡模型采用的是对每个字段的分段进行评分，那么怎样对评分卡进行分段呢？

*   变量分箱。

3\. 怎样对字段的每个分段进行评分呢？这个评分是怎么来的？

*   WOE编码，
*   将预测概率值转化为评分，
*   利用变量相关性分析和变量的系数符号保证每个分箱评分的合理性。


