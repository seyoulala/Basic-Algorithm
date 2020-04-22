### 与传统空格分隔tokenizer技术的对比

- 传统词表示方法无法很好的处理未知或罕见的词汇
- 传统词tokenization方法不利于模型学到词缀之间的关系
  - E.g 模型学到的old，older,and,oldest之间的关系无法泛化到smart,smater,smartest
- character embedding 作为OOV的解决方法粒度太细了
- subword粒度在词与字符之间，能够较好的平衡OOV问题



### Byte Pair Encodinga

BPE(字节对)编码在GPT-2以及RoBerta中都使用到了，具体步骤如下

1. 确定足够大的训练预料
2. 确定期望的subword词表的大小
3. 将单词拆分为字符序列并在尾部添加一个后缀”</ w>“,例如，“ low”的频率为5，那么我们将其改写为“ l o w </ w>”：5
4. 统计每一个连续字节对出现的频率，选择最高频率的字节对进行合并
5. 重复第四步直到达第二步设定的subword词表大小或者下一个最高频子节点出现的次数为1

加上"</w>"的意义在于表明该字词出现在单词尾部

举例

初始化词库`{ 'l', 'o', 'w', 'e', 'r', 'n', 'w', 's', 't', 'i', 'd'}`

```json
{'l o w </w>': 5, 'l o w e r </w>': 2, 'n e w e s t </w>': 6, 'w i d e s t </w>': 3}
```

Iter 1, 最高频连续字节对"e"和"s"出现了6+3=9次，合并成"es"。输出：

```json
{'l o w </w>': 5, 'l o w e r </w>': 2, 'n e w es t </w>': 6, 'w i d es t </w>': 3}
```

更新词汇库`{ 'l', 'o', 'w', 'e', 'r', 'n', 'w', 's', 't', 'i', 'd','es'}`

Iter 2, 最高频连续字节对"es"和"t"出现了6+3=9次, 合并成"est"。输出：

```json
{'l o w </w>': 5, 'l o w e r </w>': 2, 'n e w est </w>': 6, 'w i d est </w>': 3}
```

更新词汇库`{ 'l', 'o', 'w', 'e', 'r', 'n', 'w', 's', 't', 'i', 'd','es','est'}`

Iter 3, 以此类推，最高频连续字节对为"est"和"</w>" 输出：

```json
{'l o w </w>': 5, 'l o w e r </w>': 2, 'n e w est</w>': 6, 'w i d est</w>': 3}
```

……

Iter n, 继续迭代直到达到预设的subword词表大小或下一个最高频的字节对出现频率为1。



~~~python

import  re

def process_raw_words(words, endtag='-'):
    '''把单词分割成最小的符号，并且加上结尾符号'''
    vocabs = {}
    for word, count in words.items():
        # 加上空格
        word = re.sub(r'([a-zA-Z])', r' \1', word)
        word += ' ' + endtag
        vocabs[word] = count
    return vocabs

def get_symbol_pairs(vocabs):
    ''' 获得词汇中所有的字符pair，连续长度为2，并统计出现次数
    Args:
        vocabs: 单词dict，(word, count)单词的出现次数。单词已经分割为最小的字符
    Returns:
        pairs: ((符号1, 符号2), count)
    '''
    #pairs = collections.defaultdict(int)
    pairs = dict()
    for word, freq in vocabs.items():
        # 单词里的符号
        symbols = word.split()
        for i in range(len(symbols) - 1):
            p = (symbols[i], symbols[i + 1])
            pairs[p] = pairs.get(p, 0) + freq
    return pairs

def merge_symbols(symbol_pair, vocabs):
    '''把vocabs中的所有单词中的'a b'字符串用'ab'替换
    Args:
        symbol_pair: (a, b) 两个符号
        vocabs: 用subword(symbol)表示的单词，(word, count)。其中word使用subword空格分割
    Returns:
        vocabs_new: 替换'a b'为'ab'的新词汇表
    '''
    vocabs_new = {}
    raw = ' '.join(symbol_pair)
    merged = ''.join(symbol_pair)
    # 非字母和数字字符做转义
    bigram =  re.escape(raw)
    p = re.compile(r'(?<!\S)' + bigram + r'(?!\S)')
    for word, count in vocabs.items():
        word_new = p.sub(merged, word)
        vocabs_new[word_new] = count
    return vocabs_new

#统计预料中单词出现的词频
raw_words = {"low":5, "lower":2, "newest":6, "widest":3}
#输入是空格分割的字符序列
vocabs = process_raw_words(raw_words)

num_merges = 10
print (vocabs)
for i in range(num_merges):
    pairs = get_symbol_pairs(vocabs)
    # 选择出现频率最高的pair
    symbol_pair = max(pairs, key=pairs.get)
    vocabs = merge_symbols(symbol_pair, vocabs)
print (vocabs)

~~~

### 编码过程

```text
# 给定单词序列
[“the</w>”, “highest</w>”, “mountain</w>”]

# 假设已有排好序的subword词表
[“errrr</w>”, “tain</w>”, “moun”, “est</w>”, “high”, “the</w>”, “a</w>”]

# 迭代结果
"the</w>" -> ["the</w>"]
"highest</w>" -> ["high", "est</w>"]
"mountain</w>" -> ["moun", "tain</w>"]
```

使用贪心的最大正向匹配来进行编码，如highest</w>，首先判断highest</w>不在subword词表中，然后判断highest也不在词表中，一次往左移动一个字符，发现high在subword词表中，然后从est</w>开始判断，发现est</w>也在subword词表中，最后highest</w>就可以使用["high", "est</w>"]这两个token进行编码。



## WordPiece (Schuster et al., 2012)

WordPiece算法可以看作是BPE的变种。不同点在于，WordPiece基于概率生成新的subword而不是下一最高频字节对。

### 算法

1. 准备足够大的训练语料
2. 确定期望的subword词表大小
3. 将单词拆分成字符序列
4. 基于第3步数据训练语言模型
5. 从所有可能的subword单元中选择加入语言模型后能最大程度地增加训练数据概率的单元作为新的单元
6. 重复第5步直到达到第2步设定的subword词表大小或概率增量低于某一阈值

