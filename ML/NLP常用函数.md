### 交叉验证

```python
##K_flod
def get_k_flod_data(k, i, X, y):
	# 返回第i折交叉验证时所需要的训练和验证数据
	assert k > 1
	fold_size = X.shape[0] // k
	X_train, y_train, X_valid, y_valid = None, None, None, None
	for j in range(k):
		# 设置一个切片对象
		idx = slice(j * fold_size, (j + 1) * fold_size)
		X_part, y_part = X[idx, :], y[idx]
		if j == i:
			X_valid, y_valid = X_part, y_part
		elif X_train is None:
			X_train, y_train = X_part, y_part
		else:
			X_train = torch.cat((X_train, X_part), dim=0)
			y_train = torch.cat((y_train, y_part), dim=0)
	return X_train, y_train, X_valid, y_valid


def k_flod(k, X_train, y_train, num_epochs, learning_rate, weight_decay, batch_size):
	train_l_sum, valid_l_sum = 0, 0
	for i in range(k):
		data = get_k_flod_data(k, i, X_train, y_train)
		net = get_net(X_train.shape[1])
		train_ls, valid_ls = train(net, *data, num_epochs, learning_rate, weight_decay, batch_size)
		train_l_sum += train_ls[-1]
		valid_l_sum += valid_ls[-1]

		if i == 0:
			d2l.semilogy(range(1, num_epochs + 1), train_ls, 'epochs', 'rmse',
			             range(1, num_epochs + 1), valid_ls,
			             ['train', 'valid'])
		print('fold %d, train rmse %f, valid rmse %f' % (i, train_ls[-1], valid_ls[-1]))
	return train_l_sum / k, valid_l_sum / k
```

### 训练函数

```python
def train(net,train_iter,test_iter,loss,optimizer,num_epoch,device):
	"""
	net:网络
	train_iter:训练集
	test_iter:测试集
	loss:损失函数
	optimizer:优化器
	num_epoch:迭代次数
	device
	"""
	net = net.to(device)
	print('train on ',device)
	for epoch in range(num_epoch):
		train_l_sum,train_acc_sum,n,start = 0,0,0,time.time()
		batch_count = 0
		for batch in train_iter:
			X, y= batch.comment_text,batch.label
			X = X.to(device)
			y = y.to(device)
			y_hat = net(X)
			l = loss(y_hat,y)
			optimizer.zero_grad()
			l.backward()
			optimizer.step()
			train_l_sum += l.cpu().item()
			train_acc_sum += (y_hat.argmax(dim=1) == y).sum().cpu().item()
			n += y.shape[0]
			batch_count += 1
		test_acc =  evaluate_accuracy(test_iter, net)
		print('epoch %d, loss %.4f, train acc %.3f, test acc %.3f, time %.1f sec'
		      % (epoch + 1, train_l_sum / batch_count, train_acc_sum / n, test_acc, time.time() - start))
```



 ### 测试函数

```python
def evaluate_accuracy(data_iter, net, device=None):
	if device is None and isinstance(net, torch.nn.Module):
		# 如果没指定device就使用net的device
		device = list(net.parameters())[0].device
	acc_sum, n = 0.0, 0
	with torch.no_grad():
		for batch in data_iter:
			X,y = batch.comment_text,batch.label
			if isinstance(net, torch.nn.Module):
				net.eval()  # 评估模式, 这会关闭dropout
				acc_sum += (net(X.to(device)).argmax(dim=1) == y.to(device)).float().sum().cpu().item()
				net.train()  # 改回训练模式
			else:  # 自定义的模型, 3.13节之后不会用到, 不考虑GPU
				if ('is_training' in net.__code__.co_varnames):  # 如果有is_training这个参数
					# 将is_training设置成False
					acc_sum += (net(X, is_training=False).argmax(dim=1) == y).float().sum().item()
				else:
					acc_sum += (net(X).argmax(dim=1) == y).float().sum().item()
			n += y.shape[0]
	return acc_sum / n
```

### 随机种子固定

```python
def seed_everything(seed=1234):
    random.seed(seed)
    os.environ['PYTHONHASHSEED'] = str(seed)
    np.random.seed(seed)
    torch.manual_seed(seed)
    torch.cuda.manual_seed(seed)
    torch.backends.cudnn.deterministic = True
seed_everything()
```

### 清洗函数

```python
def preprocess(data):
    '''
    Credit goes to https://www.kaggle.com/gpreda/jigsaw-fast-compact-solution
    '''
    punct = "/-'?!.,#$%\'()*+-/:;<=>@[\\]^_`{|}~`" + '""“”’' + '∞θ÷α•à−β∅³π‘₹´°£€\×™√²—–&'
    def clean_special_chars(text, punct):
        for p in punct:
            text = text.replace(p, ' ')
        return text

    data = data.astype(str).apply(lambda x: clean_special_chars(x, punct))
    return data
  
  
def clean_words(input_str):
  """
  input_str 是一个document
  """
    punctuation = '.,;:"!?”“_-'
    word_list = input_str.lower().replace('\n',' ').split()
    word_list = [word.strip(punctuation) for word in word_list]
    return word_list
```

### embedding相关函数

```python
#构建背景词和中心词
def get_centers_and_contexts(dataset, max_window_size):
    centers, contexts = [], []
    for st in dataset:
        if len(st) < 2:  # 每个句子至少要有2个词才可能组成一对“中心词-背景词”
            continue
        centers += st
        for center_i in range(len(st)):
            window_size = random.randint(1, max_window_size)
            indices = list(range(max(0, center_i - window_size),
                                 min(len(st), center_i + 1 + window_size)))
            indices.remove(center_i)  # 将中心词排除在背景词之外
            contexts.append([st[idx] for idx in indices])
    return centers, contexts
  
#负采样，对每个正样本构造出K个负样本
def get_negatives(all_contexts, sampling_weights, K):
    all_negatives, neg_candidates, i = [], [], 0
    population = list(range(len(sampling_weights)))
    for contexts in all_contexts:
        negatives = []
        while len(negatives) < len(contexts) * K:
            if i == len(neg_candidates):
                # 根据每个词的权重（sampling_weights）随机生成k个词的索引作为噪声词。
                # 为了高效计算，可以将k设得稍大一点
                i, neg_candidates = 0, random.choices(
                    population, sampling_weights, k=int(1e5))
            neg, i = neg_candidates[i], i + 1
            # 噪声词不能是背景词
            if neg not in set(contexts):
                negatives.append(neg)
        all_negatives.append(negatives)
    return all_negatives
  
#定于数据类
class MyDataset(torch.utils.data.Dataset):
    def __init__(self, centers, contexts, negatives):
        assert len(centers) == len(contexts) == len(negatives)
        self.centers = centers
        self.contexts = contexts
        self.negatives = negatives

    def __getitem__(self, index):
        return (self.centers[index], self.contexts[index], self.negatives[index])

    def __len__(self):
        return len(self.centers)

     
#构造batch数据
def batchify(data):
    """用作DataLoader的参数collate_fn: 输入是个长为batchsize的list, 
    list中的每个元素都是Dataset类调用__getitem__得到的结果
    """
    max_len = max(len(c) + len(n) for _, c, n in data)
    centers, contexts_negatives, masks, labels = [], [], [], []
    for center, context, negative in data:
        cur_len = len(context) + len(negative)
        centers += [center]
        contexts_negatives += [context + negative + [0] * (max_len - cur_len)]
        masks += [[1] * cur_len + [0] * (max_len - cur_len)]
        labels += [[1] * len(context) + [0] * (max_len - len(context))]
    return (torch.tensor(centers).view(-1, 1), torch.tensor(contexts_negatives),
            torch.tensor(masks), torch.tensor(labels))
  
  

```
