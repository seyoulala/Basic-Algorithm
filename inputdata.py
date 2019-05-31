#!/usr/bin/env python
# -*- coding: utf-8 -*-

# @Time : 2019/5/31 下午2:12 
# @Author : Ethan
# @Site :  
# @File : inputdata.py 
# @Software: PyCharm

import  collections
import numpy as np

## 负采样。,以 count(word)**0.75/(sum(word_frequence))采样出负采样表


"""
文本数据中一行就是一个训练样本
1.讲文本数据一行变为一个列表
2.移除停用词
3建立词语索引

"""

def discard(idx):
	"""
	idx词频越高丢弃的概率越大
	:param idx: 词索引
	:return: boolean
	"""
	boolean = np.random.uniform(0,1) < 1-np.sqrt(1e-4/counter[ix_to_word[idx]]*num_tokens)
	return boolean

def compare_counts(token):
	return '# %s: before=%d ,after=%d'%(token,sum([st.count(word_to_ix[token])for st in dataset]),
	                                    sum([st.count(word_to_ix[token]) for st in subsampled_dataset]))


def get_centers_and_contexts(dataset,max_window_size):
	conters,contexts =[],[]
	for st in dataset:
		if len(st)<2:
			continue
		#st中每个词都会成为中心词
		conters.extend(st)
		for i in range(len(st)):
			window_size = np.random.randint(1,max_window_size+1)
			#确定当前词的窗口的左右边界
			indices = list(range(max(0,i-window_size),min(len(st),i+window_size+1)))
			#移除中心词
			indices.remove(i)
			contexts.append([st[idx] for idx in indices])
	return conters,contexts



path = "/home/ethan/PycharmProjects/ml_python/ptb.train.txt"
with open(path,'r') as f:
	lines = f.readlines()
	raw_dataset = [st.split() for st in lines]

#统计词汇表中词出现的次数
counter = collections.Counter([tk for st in raw_dataset for tk in st])
#过滤掉出现次数小于5的单词
counter = dict(filter(lambda x:x[1]>=5,counter.items()))

vacab = counter.keys()
word_to_ix = {word:ix for ix,word in enumerate(vacab)}
ix_to_word = {ix:word for ix,word in enumerate(vacab)}
dataset = [[word_to_ix[word] for word in st if word in vacab] for st in raw_dataset]

num_tokens = sum([len(st) for st in dataset])
##在背景窗口中，一个词和低频次出现比和高频词同时出现更有利于词向量的训练

#二次采样后的数据集合
subsampled_dataset = [[tk for tk in st if not discard(tk)]for st in dataset]

#提取背景词和中心词.窗口的大小为一个不固定的数，在1-maxsize之间均匀采样一个整数

all_centers,all_contexts = get_centers_and_contexts(subsampled_dataset,5)

##使用负采样来近似训练,对于一对中心词和背景词，随机采样K个噪声词。噪声词的采样概率P(w)为w词频与总词频之比的0.75次方
#每一对中心词和背景词就要采集K个噪声词，因此对一行数据来说，需要采集k×len(context)个噪声词



