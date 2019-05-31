## PyTorch 基础 :数据的加载和预处理

PyTorch通过torch.utils.data对一般常用的数据加载进行了封装，可以很容易地实现多线程数据预读和批量加载。

#### Dataset

Dataset是一个抽象类，为了能够方便的读取，需要将数据包装成Dataset类。自定义的dataset类需要继承它并实现两个成员方法。

1. `__getitem__()` 该方法定义用索引(`0` 到 `len(self)`)获取一条数据或一个样本
2. `__len__()` 该方法返回数据集的总长度

------



#### Dataloader

DataLoader为我们提供了对Dataset的读取操作，常用参数有：batch_size(每个batch的大小), shuffle(是否进行shuffle操作), num_workers(加载数据的时候使用几个子进程)



#### torchvision.transform

transforms 模块提供了一般的图像转换操作类，用作数据处理和数据增强.

```python
from torchvision import transforms as transforms
transform = transforms.Compose([
    transforms.RandomCrop(32, padding=4),  #先四周填充0，在把图像随机裁剪成32*32
    transforms.RandomHorizontalFlip(),  #图像一半的概率翻转，一半的概率不翻转
    transforms.RandomRotation((-45,45)), #随机旋转
    transforms.ToTensor(),
    transforms.Normalize((0.4914, 0.4822, 0.4465), (0.229, 0.224, 0.225)), #R,G,B每层的归一化用到的均值和方差
])
```





##  损失函数(Loss Function)
损失函数（loss function）是用来估量模型的预测值(我们例子中的output)与真实值（例子中的y_train）的不一致程度，它是一个非负实值函数,损失函数越小，模型的鲁棒性就越好。
我们训练模型的过程，就是通过不断的迭代计算，使用梯度下降的优化算法，使得损失函数越来越小。损失函数越小就表示算法达到意义上的最优。

这里有一个重点：因为PyTorch是使用mini-batch来进行计算的，所以损失函数的计算出来的结果已经对mini-batch取了平均

常见（PyTorch内置）的损失函数有以下几个：
### nn.L1Loss:
输入x和目标y之间差的绝对值，要求 x 和 y 的维度要一样（可以是向量或者矩阵），得到的 loss 维度也是对应一样的
$$
loss(x,y)=1/n\sum|x_i-y_i|
$$


### nn.NLLLoss:
用于多分类的负对数似然损失函数
$$
loss(x, class) = -x[class]
$$
NLLLoss中如果传递了weights参数，会对损失进行加权，公式就变成了
$$
loss(x, class) = -weights[class] * x[class]
$$


### nn.MSELoss:
均方损失函数 ，输入x和目标y之间均方差
$$
loss(x,y)=1/n\sum(x_i-y_i)^2
$$

### nn.CrossEntropyLoss:
多分类用的交叉熵损失函数，LogSoftMax和NLLLoss集成到一个类中，会调用nn.NLLLoss函数,我们可以理解为CrossEntropyLoss()=log_softmax() + NLLLoss()
$$
\begin{aligned} loss(x, class) &= -\text{log}\frac{exp(x[class])}{\sum_j exp(x[j]))}\ &= -x[class] + log(\sum_j exp(x[j])) \end{aligned}
$$
 因为使用了NLLLoss，所以也可以传入weight参数，这时loss的计算公式变为：


$$
loss(x, class) = weights[class] * (-x[class] + log(\sum_j exp(x[j])))
$$
 所以一般多分类的情况会使用这个损失函数



### nn.BCELoss:
计算 x 与 y 之间的二进制交叉熵。

$$
loss(o,t)=-\frac{1}{n}\sum_i(t[i]* log(o[i])+(1-t[i])* log(1-o[i]))
$$
与NLLLoss类似，也可以添加权重参数： 

$$
loss(o,t)=-\frac{1}{n}\sum_iweights[i]* (t[i]* log(o[i])+(1-t[i])* log(1-o[i])) 
$$
用的时候需要在该层前面加上 Sigmoid 函数。





### pytorch函数的作用

------

pytorch中在rnn的batch中处理可变长序列的函数

`torch.nn.utils.rnn.pack_padded_sequence()`

`torch.nn.utils.rnn.pad_packed_sequence()`

[pytorch中处理变长序列](<https://zhuanlan.zhihu.com/p/34418001>)

结合上面两个函数来避免padding对句子表示的影响



`torch.squeeze()`

这个函数的作用是对数据的维度进行压缩。

`b = torch.squeeze(b)`意思就是将b中维度为1的维度删除

```pyton
t = torch.randn(10,1,4)
t.size()
torch.Size([10, 1, 4])
t.squeeze_()
tensor([[-1.2979,  1.0459,  0.8371, -1.1103],
        [-0.8757,  0.0768,  0.7131, -0.0699],
        [ 2.1082,  0.9104,  0.4271,  0.0503],
        [ 0.2596, -0.2568,  0.2504,  0.6831],
        [ 0.4804, -0.0536,  0.3152, -0.6436],
        [ 1.0560,  0.5040, -0.4237,  0.5763],
        [ 0.3579,  1.3508,  0.1080, -0.5490],
        [ 0.7102,  0.1416,  0.7483, -0.8637],
        [ 2.4638, -1.3936,  0.4531,  0.2021],
        [-0.7095,  1.4866,  0.5356,  0.0461]])
t.size()
torch.Size([10, 4])
```



`torch.unsqueeze()`

这个函数的作用是扩充维度

```python
t = torch.randn(10,4)
t.size()
torch.Size([10, 4])
t = t.unsqueeze(0)
t.size()
torch.Size([1, 10, 4])
```



### 拼接向量的一些方法

`torch.cat()`

对tensor的列表在指定的dim上进行拼接

`torch.Tensor.expand(*sizes)`

返回张量的一个新视图，可以讲张量的单个维度扩到更大的尺寸

在某个维度上传－１意味维度扩大不涉及这个维度

```
t = torch.randn(1,1,1)
t.size()
torch.Size([1, 1, 1])
t = t.expand(3,4,-1)
t.size()
torch.Size([3, 4, 1])
```



`torch.topk()`

返回一个tensor中topk个元素以及对应的索引

```
>>> x = torch.arange(1., 6.)
>>> x
tensor([ 1.,  2.,  3.,  4.,  5.])
>>> torch.topk(x, 3)
torch.return_types.topk(values=tensor([5., 4., 3.]), indices=tensor([4, 3, 2]))
```



`torch.mul(input, value, out=**None**)`

用标量值`value`乘以输入`input`的每个元素，并返回一个新的结果张量。 *o**u**t*=*t**e**n**s**o**r*∗*v**a**l**u*

```
>>> a = torch.randn(4,4)
>>> a

-0.7280  0.0598 -1.4327 -0.5825
-0.1427 -0.0690  0.0821 -0.3270
-0.9241  0.5110  0.4070 -1.1188
-0.8308  0.7426 -0.6240 -1.1582
[torch.FloatTensor of size 4x4]

>>> b = torch.randn(2, 8)
>>> b

 0.0430 -1.0775  0.6015  1.1647 -0.6549  0.0308 -0.1670  1.0742
-1.2593  0.0292 -0.0849  0.4530  1.2404 -0.4659 -0.1840  0.5974
[torch.FloatTensor of size 2x8]

>>> torch.mul(a, b)

-0.0313 -0.0645 -0.8618 -0.6784
 0.0934 -0.0021 -0.0137 -0.3513
 1.1638  0.0149 -0.0346 -0.5068
-1.0304 -0.3460  0.1148 -0.6919
[torch.FloatTensor of size 4x4]
```



## RNN 

![img](https://i.imgur.com/Z2xbySO.png)



```python

class RNN(nn.Module):
	def __init__(self,input_size,hidden_size,output_size):
		super(RNN, self).__init__()

		#rnn 需要输入起始的hidden state
		self.hidden_size = hidden_size

		#output层
		self.i20 = nn.Linear(in_features=input_size+hidden_size,out_features=output_size)
		self.i2h = nn.Linear(input_size+output_size,hidden_size)
		# softmax层
		self.softmax = nn.LogSoftmax(dim=1)


	def forward(self,input,hidden):
		#拼接两个向量,按列拼接,(3,1) ,(3,4)->(3,5)
		combined_vec = torch.cat([input,hidden],dim=1)
		hidden = self.i2h(combined_vec)
		output = self.i20(combined_vec)
		output = self.softmax(output)

		#RNN需要返回两个状态，每个时间步的输出，以及每个时间步的隐藏状态
		return  output,hidden


	def initHidden(self):
		#shape（batch_size,hidden_size）
		return torch.zeros(1,self.hidden_size）
                           
                           
                           
                           
```

## LSTM

![](https://zh.gluon.ai/_images/lstm_3.svg)



```python
def get_params():
    def _one(shape):
        return nd.random.normal(scale=0.01, shape=shape, ctx=ctx)

    def _three():
        return (_one((num_inputs, num_hiddens)),
                _one((num_hiddens, num_hiddens)),
                nd.zeros(num_hiddens, ctx=ctx))

    W_xi, W_hi, b_i = _three()  # 输入门参数
    W_xf, W_hf, b_f = _three()  # 遗忘门参数
    W_xo, W_ho, b_o = _three()  # 输出门参数
    W_xc, W_hc, b_c = _three()  # 候选记忆细胞参数
    # 输出层参数
    W_hq = _one((num_hiddens, num_outputs))
    b_q = nd.zeros(num_outputs, ctx=ctx)
    # 附上梯度
    params = [W_xi, W_hi, b_i, W_xf, W_hf, b_f, W_xo, W_ho, b_o, W_xc, W_hc,
              b_c, W_hq, b_q]
    for param in params:
        param.attach_grad()
    return params



def lstm(inputs, state, params):
    [W_xi, W_hi, b_i, W_xf, W_hf, b_f, W_xo, W_ho, b_o, W_xc, W_hc, b_c,
     W_hq, b_q] = params
    (H, C) = state
    outputs = []
    for X in inputs:
        I = nd.sigmoid(nd.dot(X, W_xi) + nd.dot(H, W_hi) + b_i)
        F = nd.sigmoid(nd.dot(X, W_xf) + nd.dot(H, W_hf) + b_f)
        O = nd.sigmoid(nd.dot(X, W_xo) + nd.dot(H, W_ho) + b_o)
        C_tilda = nd.tanh(nd.dot(X, W_xc) + nd.dot(H, W_hc) + b_c)
        C = F * C + I * C_tilda
        H = O * C.tanh()
        Y = nd.dot(H, W_hq) + b_q
        outputs.append(Y)
    return outputs, (H, C)
```

