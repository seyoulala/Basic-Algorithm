Date | Title | Author |  Confirmer  | Version
:-------:  | :-------: |:-------: | :-------:  | :-------: 
2018-08-17  | 评分卡 A | Xu、Blair | Luo | ~ | 1.0

# 互联网金融业申请评分卡的介绍

信用评分卡是一个通过个人数据设法对其还款能力和还款意愿进行定量评估的系统

## 1. 评分卡在互联网金融业中的应用场景

<img src="/scoring_card/images/20170714152807050.png" width="750" />

## 2. 什么是评分卡

信贷场景中的评分卡

- 以分数的形式来衡量风险几率的一种手段
- 是对未来一段时间内违约/逾期/失联概率的预测
- 通常分数越高越安全
- 数据驱动（搜集数据，对数据研究，建立模型）

### 2.1 评分卡的分类

反欺诈评分卡、申请评分卡是在贷前准入环节里面 
   
 1. 贷前：申请评分卡（Application score card），又称为A卡
 2. 贷中：行为评分卡（Behavior score card），又称为B卡
 3. 贷后：催收评分卡（Collection score card），又称为C卡

以下是评分卡最后得出的规则图：

<img src="/scoring_card/images/v2-1c61edf5d441089e24160a5e363f44ae_hd.jpg" width="600" />

## 3. 评分卡开发常用的模型

Model | Advantage | Disadvantage
:-------: | :-------:  | :-------: 
逻辑回归 | 简单,稳定,**可解释**,技术成熟,易于监测和部署 | 准确度不高
决策树 | 对数据质量要求低,易解释 | 准确度不高
组合模型 | 准确度高,不易过拟合  | 不易解释;部署困难;计算量大
.. | .. | ..

## 4. 模型评价指标

###  4.1 混淆矩阵，TPR (Recal)，FPR

TPR (或Recall) 为坏客户的查全率，表示被模型抓到的坏客户占总的坏客户的比例，表达式为：

![](https://www.zhihu.com/equation?tex=TPR%3D+%5Cfrac+%7BTP%7D+%7BTP%2BFN%7D+%5C%5C)

FPR 为好客户误判率，表示好客户中倍模型误误判的比例，表达式为:

![](https://www.zhihu.com/equation?tex=FPR+%3D+%5Cfrac+%7BFP%7D%7BFP%2BTN%7D+%5C%5C) 

可以把TPR看做模型的收益，FPR看做模型付出的代价。

- 如果一个模型 TPR越大，表示模型能够抓到的坏客户比例越大，即收益越大；  
- FPR越大，表示模型能够将好客户误抓的比例越大，即代价越大。

<img src="/scoring_card/images/6069502-fe0ce89931844b5d.png" width="600" />


### 4.2 AUC

AUC 表示模型对任意坏客户的输出结果为大于模型对任意好客户的输出结果的概率。AUC的取值范围在0.5和1之间，AUC 越大，表示模型预测性能越好。

![](http://sklearn.apachecn.org/cn/0.19.0/_images/sphx_glr_plot_roc_001.png)

### 4.3 KS
衡量分数区分能力的指标,ks取值越大，模型区分好坏客户能力越强

<img src="/scoring_card/images/20170714140407038.png" width="600" />

把样本按分数由低到高排序，Ｘ轴是总样本累积比例，Ｙ是累积好，坏样本分别占总的好，坏样本的比例。两条曲线在Ｙ轴方向上的相差最大值即 KS。KS 越大说明模型的区分能力越好。

## 5. 模型开发步骤

信用评分卡的开发有一套科学的、严密的流程，包括数据获取，EDA，数据预处理，到变量筛选，![lr](https://www.zhihu.com/equation?tex=lr) 模型的开发和评估，生成评分卡模型以及布置上线和模型监测。

典型的开发流程如下图所示：

![](https://pic1.zhimg.com/80/v2-db979466aa6abc3f74b917b21b88a76f_hd.jpg)


## 6. 萨摩耶数据集结果
 
LogisticRegression

**AUC**
**trainset:0.737**
**testset:0.727**

**ks值**

<img src="/scoring_card/images/20180816112254.png" width="700" />

**入模变量**

<img src="/scoring_card/images/_20180816112744.png" width="700" />

**入模变量权重**

<img src="/scoring_card/images/20180816112305.png" width="700" />







