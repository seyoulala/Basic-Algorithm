## Embedding



pytorch中Embedding模块的输入时对应word的index，输出时相应的embedding vector



```python
>>> # an Embedding module containing 10 tensors of size 3
>>> embedding = nn.Embedding(10, 3)
>>> # a batch of 2 samples of 4 indices each
>>> input = torch.LongTensor([[1,2,4,5],[4,3,2,9]])
>>> embedding(input)
tensor([[[-0.0251, -1.6902,  0.7172],
         [-0.6431,  0.0748,  0.6969],
         [ 1.4970,  1.3448, -0.9685],
         [-0.3677, -2.7265, -0.1685]],

        [[ 1.4970,  1.3448, -0.9685],
         [ 0.4362, -0.4004,  0.9400],
         [-0.6431,  0.0748,  0.6969],
         [ 0.9124, -2.3616,  1.1151]]])
```

输出shape为(2,4,3)

## Ngram



```python
#!/usr/bin/env python
# -*- coding: utf-8 -*-

# @Time : 2019/5/29 下午5:36 
# @Author : Ethan
# @Site :  
# @File : Classifying Names.py 
# @Software: PyCharm

import glob
import os
from io import open
import random
import matplotlib.pyplot as plt

import torch
import torch.nn as nn
import torch.nn.functional as F


CONTEXT_SIZE=2
EMBEDDING_DIM=10

test_sentence = """When forty winters shall besiege thy brow,
And dig deep trenches in thy beauty's field,
Thy youth's proud livery so gazed on now,
Will be a totter'd weed of small worth held:
Then being asked, where all thy beauty lies,
Where all the treasure of thy lusty days;
To say, within thine own deep sunken eyes,
Were an all-eating shame, and thriftless praise.
How much more praise deserv'd thy beauty's use,
If thou couldst answer 'This fair child of mine
Shall sum my count, and make my old excuse,'
Proving his beauty by succession thine!
This were to be new made when thou art old,
And see thy blood warm when thou feel'st it cold.""".split()


#　窗口大小为２([a,b],c)为一个训练样本
trigrams = [([test_sentence[i],test_sentence[i+1]],test_sentence[i+2]) for
            i in range(len(test_sentence)-2)]

#词汇表
vocab = set(test_sentence)
#
word_to_ix = {word:i for i, word in enumerate(vocab)}


class NGramLanguageModerler(nn.Module):
	def __init__(self,vacab_size,embedding_dim,context_size):
		super(NGramLanguageModerler, self).__init__()
		self.embeddings =  nn.Embedding(vacab_size,embedding_dim)
		self.fc1 = nn.Linear(context_size*embedding_dim,128)
		self.fc2 = nn.Linear(128,vacab_size)

	def forward(self,x):
		embeds= self.embeddings(x).view((1,-1))
		out = F.relu(self.fc1(embeds))
		out = self.fc2(out)
		log_probs = F.log_softmax(out,dim=1)
		return log_probs


model = NGramLanguageModerler(len(vocab),EMBEDDING_DIM,CONTEXT_SIZE)
losses =[]
loss_func = nn.NLLLoss()
optimizer = torch.optim.SGD(model.parameters(),lr=0.001)

for epoch in range(100):
	total_loss = 0
	for context,target in trigrams:
		#准备输入的ｔｅｎｓｏｒ,将单词对应的ｉｎｄｅｘ装换为ｔｅｎｓｏｒ输入模型中
		context_idxs = torch.tensor([word_to_ix[i] for i in context],dtype=torch.long)

		optimizer.zero_grad()
		output = model(context_idxs)
		#计算loss
		loss = loss_func(output,torch.tensor([word_to_ix[target]],dtype=torch.long))

		loss.backward()
		optimizer.step()

		total_loss+=loss.item()
	losses.append(total_loss)

# plt.plot(losses)
# plt.xlabel("epoch")
# plt.ylabel("loss")
# plt.show()
```



## CBOW

```python
#!/usr/bin/env python
# -*- coding: utf-8 -*-

# @Time : 2019/5/29 下午5:36 
# @Author : Ethan
# @Site :  
# @File : Classifying Names.py 
# @Software: PyCharm

import glob
import os
from io import open
import random
import matplotlib.pyplot as plt

import torch
import torch.nn as nn
import torch.nn.functional as F

CONTEXT_SIZE = 2
EMBEDDING_DIM = 128

test_sentence = """When forty winters shall besiege thy brow,
And dig deep trenches in thy beauty's field,
Thy youth's proud livery so gazed on now,
Will be a totter'd weed of small worth held:
Then being asked, where all thy beauty lies,
Where all the treasure of thy lusty days;
To say, within thine own deep sunken eyes,
Were an all-eating shame, and thriftless praise.
How much more praise deserv'd thy beauty's use,
If thou couldst answer 'This fair child of mine
Shall sum my count, and make my old excuse,'
Proving his beauty by succession thine!
This were to be new made when thou art old,
And see thy blood warm when thou feel'st it cold.""".split()

# 　窗口大小为２([a,b],c)为一个训练样本
trigrams = [([test_sentence[i], test_sentence[i + 1]], test_sentence[i + 2]) for
            i in range(len(test_sentence) - 2)]

# 词汇表
vocab = set(test_sentence)
#
vacab_size = len(vocab)
word_to_ix = {word: i for i, word in enumerate(vocab)}

data = []
for i in range(2, len(test_sentence) - 2):
	context = [test_sentence[i - 2], test_sentence[i - 1], test_sentence[i + 1], test_sentence[i + 2]]
	target = test_sentence[i]
	data.append((context, target))


class CBOW(nn.Module):
	def __init__(self, vacab_size, embedding_size, context_size):
		super(CBOW, self).__init__()
		# Embedding层
		self.embeddings = nn.Embedding(vacab_size, embedding_size)
		#窗口左边两个词，右边两个词,所以input_size = embedding_size * 2*context_siz
		self.fc1 = nn.Linear(embedding_size * 2*context_size, 128)
		self.fc2 = nn.Linear(128, vacab_size)

	def forward(self, x):
		embeds = self.embeddings(x).view(1, -1)
		output = self.fc1(embeds)
		output = F.relu(output)
		output = self.fc2(output)
		output = F.log_softmax(output, dim=1)
		return output


model = CBOW(vacab_size,EMBEDDING_DIM,CONTEXT_SIZE)
loss_func = nn.NLLLoss()
optimizer = torch.optim.SGD(model.parameters(), lr=0.001)

losses = []
for epoch in range(10):
	total_loss = 0
	# 准备输入输出
	for contexts, target in data:
		input_tensor = torch.tensor([word_to_ix[i] for i in contexts], dtype=torch.long)
		target_tensor = torch.tensor([word_to_ix[target]], dtype=torch.long)

		optimizer.zero_grad()
		output = model(input_tensor)
		loss = loss_func(output,target_tensor)
		loss.backward()
		optimizer.step()

		total_loss+=loss.item()
	losses.append(total_loss)
print(losses)
```



## Skipgram

跳字模型假设基于某个中心词来生成背景词。举个例子，假设文本序列是“the”“man”“loves”“his”“son”。以“loves”作为中心词，设背景窗口大小为2。如图10.1所示，跳字模型所关心的是，给定中心词“loves”，生成与它距离不超过2个词的背景词“the”“man”“his”“son”的条件概率，即
$$
P(``the",``man",``his",``son"∣``loves").
$$
假设给定中心词的情况下，背景词的生成时独立的。那么上式子可以改写为
$$
P(``the"∣``loves")⋅P(``man"∣``loves")⋅P(``his"∣``loves")⋅P(``son"∣``loves").
$$
跳字模型的核心在于使用softmax运算来得到给定中心词来生成背景词的概率
$$
P(w_0|w_c) = \frac{exp(u_{o}^T\cdot v_c)}{\sum_{i \in v}exp(u_i^T\cdot v_c)}
$$
该条件概率对应的相应的对数损失
$$
-logP(w_o|w_c) = -u_o^T \cdot v_c + log(\sum_{i\in v}{u_i^T \cdot v_c})
$$
由于条件概率中使用了softmax运算，那么对应词汇量很大的情况下，softmax计算复杂度太高了，为了节省计算资源使用近似训练的方法：1.负采样 2.hierarchical softmax



#### 负采样

负采样修改了原来的目标函数。给定中心词wc的一个背景窗口，我们把背景词wo出现在该背景窗口看作一个事件，并将该事件的概率计算为
$$
p(D=1|w_c,w_o) = \alpha(u_0^T \cdot v_c)
$$
同时，根据某种概率分布采样出K个不在背景窗口中的词.此时需要最小化的目标函数变为

![](https://ask.qcloudimg.com/draft/1528151/h5ar6ot5mg.png?imageView2/2/w/1620)

![](https://ask.qcloudimg.com/draft/1528151/o8lowzw7ti.png?imageView2/2/w/1620)

