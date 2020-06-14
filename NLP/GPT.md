### GPT

GPT使用transformer中的decoder来作为特征的提取器，整个训练过程由两部分组成，第一部分是pretraning的过程，使用标准的语言模型在unlable的text 数据中学习神经网络的参数表示。第二阶段是finetuning的过程，使用特定的任务来微调模型参数。

###  Unsupervised pre-traning

给定一个无监督的文本语料 $\mu =\{\mu_{1},...,\mu_{2}\}$,使用标准的语言目标函数来最大思然函数
$$
L_{1}(\mu)=\sum_{i}{logP(\mu_{i}|\mu_{i-k},...\mu_{i-1};\theta)}
$$
其中k是窗口的大小，$\theta$是neural network的参数。

GPT模型使用Transformer的decoder架构来完成特征的提取。

### Supervised fine-tuning

通过第一阶段无监督训练得到了模型的参数，我们把这些参数用在监督学习的任务上面。将训练数据$x_{1},x_{2}...x_{m},以及标签y$，训练数据通过decoder得到最后的隐藏状态 $h_{l}^m \in [batch_size,hidden_size]$,

然后通过一个线性层以及一个softmax得到一个词汇表大小的概率分布。所以在监督学习阶段我们的目标就是最大化以下似然函数
$$
P(y|x^1,x^2,...,x^m) = softmax(h_{l}^mW_y) \\
max L_2(C) = \sum_{(x,y)}log(P(y|x^1,x^2,...,x^m))
$$
通过pre-traninig来增强模型的泛化能力，同时能加速模型的收敛。综合第一阶段的pre-traning和第二阶段的fine-turning我们最终需要优化以下目标函数$L_3(C) =L_2(C)+\lambda*L_1(C)$,同时在fine-turning的阶段只需要学习线性层的参数$W_y$

![](https://pic3.zhimg.com/80/v2-447968f91ef1904b2c11f5f343d19ad6_hd.jpg)