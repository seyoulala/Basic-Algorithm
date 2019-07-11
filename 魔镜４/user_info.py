#!/usr/bin/env python
# -*- coding: utf-8 -*-

# @Time : 2019/7/11 下午2:46 
# @Author : Ethan
# @Site :  
# @File : user_info.py 
# @Software: PyCharm

import pandas as pd
import numpy as np
import warnings
import matplotlib.pyplot as plt
import seaborn as sns
import os
import sys
import gc
import time
import datetime

warnings.filterwarnings('ignore')
pd.set_option("display.max_columns", None)
pd.set_option("display.max_rows", None)
data_path = "./data/"
train = pd.read_csv(os.path.join(data_path, 'train.csv'))
test = pd.read_csv(os.path.join(data_path, 'test.csv'))

user_info = pd.read_csv(os.path.join(data_path, 'user_info.csv'))

train = train.replace(to_replace='\\N', value=np.NaN)

train['repay_date'] = pd.to_datetime(train['repay_date'])
train['due_date'] = pd.to_datetime(train['due_date'])
train['auditing_date'] = pd.to_datetime(train['auditing_date'])
train['repay_amt'] = pd.to_numeric(train['repay_amt'])

test['auditing_date'] = pd.to_datetime(test['auditing_date'])
test['due_date'] = pd.to_datetime(test['due_date'])
test['due_amt'] = pd.to_numeric(test['due_amt'])
user_info.head()


def mapAge(x):
	if x <= 20:
		return 1
	elif x <= 30:
		return 2
	elif x <= 40:
		return 3
	elif x <= 50:
		return 4
	else:
		return 5


user_info['age_bin'] = user_info['age'].map(mapAge)
user_info['insertdate'] = pd.to_datetime(user_info['insertdate'])
user_info['reg_mon'] = pd.to_datetime(user_info['reg_mon'])

# 手机号归属省份和用户归属省份是否一致 一致为1 不一致为0
user_info['cell_is_same'] = user_info.apply(lambda x: 1 if x['cell_province'] == x['id_province'] else 0, axis=1)

##手机号归属省份是否缺失 缺失为1 不缺失为0
user_info['cell_missing'] = user_info['cell_province'].map(lambda x: 1 if not x else 0)

##数据插入时间和注册时间的间隔(天间隔)
user_info['insert_reg_diff'] = (user_info['insertdate'] - user_info['reg_mon']).dt.days

agg_ = {'age_bin': ['max'],  # 取用户最近的年龄
        'cell_is_same': ['max', 'nunique', 'min'],
        'cell_missing': ['min', 'max'],
        'cell_province': ['nunique'],  # 手机所属省份变动次数
        'insert_reg_diff': ['min', 'max', 'mean']
        }

start_time = train['auditing_date'].min()
end_time = train['auditing_date'].max()
time_range = pd.date_range(start=start_time, end=end_time)

# testset
start_time_test = test['auditing_date'].min()
end_time_test = test['auditing_date'].max()
time_range_test = pd.date_range(start=start_time_test, end=end_time_test)
train_feature_table = pd.DataFrame()
for time in time_range:
	tmp_train = train.loc[train['auditing_date'] == time, ['user_id']]
	# 用户表信息
	his_user = user_info.loc[user_info['insertdate'] < time, :]
	tmp_join = tmp_train.merge(his_user, on='user_id', how='left')
	feature_table = tmp_join.groupby('user_id').agg(agg_)
	feature_table.columns = pd.Index(["{}_{}".format(e[0], e[1]) for e in feature_table.columns.tolist()])
	feature_table = feature_table.reset_index()
	feature_table = tmp_train.merge(feature_table, on='user_id', how='left')
	train_feature_table = pd.concat([train_feature_table, feature_table], axis=0)

test_feature_tabel = pd.DataFrame()
for time in time_range_test:
	tmp_test = test.loc[test['auditing_date'] == time, ['user_id']]
	# 用户表信息
	his_user = user_info.loc[user_info['insertdate'] < time, :]
	tmp_join = tmp_test.merge(his_user, on='user_id', how='left')
	feature_table = tmp_join.groupby('user_id').agg(agg_)
	feature_table.columns = pd.Index(["{}_{}".format(e[0], e[1]) for e in feature_table.columns.tolist()])
	feature_table = feature_table.reset_index()
	feature_table = tmp_test.merge(feature_table, on='user_id', how='left')
	test_feature_tabel = pd.concat([test_feature_tabel, feature_table], axis=0)

###添加所在省份信息，以及性别信息
user_info = user_info.drop_duplicates(subset=['user_id'])
train_feature_table = train_feature_table.merge(user_info[['user_id', 'gender', 'id_province']], on='user_id',
                                                how='left')

test_feature_tabel = test_feature_tabel.merge(user_info[['user_id', 'gender', 'id_province']], on='user_id', how='left')
test_feature_tabel.head()
train_feature_table.to_csv('train_user_info_feature.csv', index=False)
test_feature_tabel.to_csv('test_user_info_feature.csv', index=False)
