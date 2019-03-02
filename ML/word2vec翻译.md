# word2vec Parameter Learning Explained

由于word2vec模型学习生成的词向量表示方法能够携带句子的语义信息(semantic meanings),因此非常适用于多种NLP任务.

## 1. Continuous Bag-of-Word Model
### 1.1 one-word-context

我们从CBOW模型的最简单版本开始介绍-one-word context.即我们假定context(预测目标单词的上下文信息)只有一个单词,也就是说One-word context 模型是在只有一个上下文单词的情况下来预测一个目标单词的(one target word)


<img src='/home/xyh/Pictures/word2vec1.png'>

图1描述的就是one-word context定义下的神经网络模型.这里假设文本词汇量的大小为V,**隐藏层的**大小为N,相邻层的神经元是全连接的.**输入层**是一个用one-hot方式编码的单词向量$$x=(x_1,x_2,....,x_v)$,其中只有一个$x_i$为1,其它全为0.

从输入层到隐藏层的权重值可以用一个$V×N$维的矩阵W来表示,即

$$
W=
 \begin{pmatrix}
 \omega_{11}&\omega_{12}&...&\omega_{1N}\\
 \omega_{21}&\omega_{22}&...&\omega_{2N}\\
 ...&...&...&...\\
 \omega_{V1}&\omega_{V2}&...&\omega_{VN}
 \end{pmatrix}

$$

其中W矩阵的每一行代表的是与输入层相关单词的N维向量表示形式$V_w$.那么假设我们给定了一个输入单词(a context),其单词向量的第K哥元素$x_k=1$,其余均为0,则有

$$
\mathbf h= \mathbf W^Tx=\mathbf W_{(k,\bullet)}^T x_k=\mathbf v_{\omega_I}^T\tag{1}
$$

从(1)式看,h向量完全是从W矩阵第K行复制过来的(同$v_wi$均为N维向量).
$v_wi$也就是输入单词$w_i$的一种向量表示(其实就是输入向量)

同理,隐藏层到输出层的连接权(也就是投影矩阵)用一个新的N×V矩阵.
$\mathbf W'=\{\omega_{ij}' \}$来表示如下:

$$
\mathbf W'=
 \begin{pmatrix}
 \omega_{11}'&\omega_{12}'&...&\omega_{1V}'\\
 \omega_{21}'&\omega_{22}'&...&\omega_{2V}'\\
 ...&...&...&...\\
 \omega_{N1}'&\omega_{N2}'&...&\omega_{NV}'
 \end{pmatrix}
$$

通过这些权重,我们可以为词表中的每一个单词都计算出一个得分$\mu_j$.

$$
\mu_j=\mathbf {v_{\omega_j}'}^T\mathbf h\tag{2}
$$
其中,${v_{\omega_j}'}$就是矩阵$\mathbf W'$的第j列向量(也是N维向量,其实就是单词W的输出向量)

计算出分数之后,可以使用softmax函数来计算单词的后验分布(是多项式分布)

$$
p(\omega_j|\omega_I)=y_j=\frac{\exp(\mu_j)}{\sum_{j'=1}^V\exp(\mu_{j'})}\tag{3}
$$

其中,$y_j$表示输出层第j个神经单元的输出值.将(1),(2)代入(3)得到:

$$
p(\omega_j|\omega_I)=\frac{\exp({\mathbf v_{\omega_j}'}^T \mathbf v_{\omega_I})}{\sum_{j'=1}^V\exp({\mathbf v_{\omega_j}'}^T \mathbf v_{\omega_I})}\tag{4}
$$

如前文所诉,$v_w$和$v_w'$是单词的两种向量表示形式.其中$v_w$实际上是权重矩阵$W$(input->hidden)的某一行向量,
$\mathbf v_\omega'$是权重矩阵$\mathbf W'$的某一列向量.我们将$v_w$和$v_w'$分别称为*输入向量*和*输出向量*


