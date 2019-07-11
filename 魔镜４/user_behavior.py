#!/usr/bin/env python
# -*- coding: utf-8 -*-

# @Time : 2019/7/11 下午2:48 
# @Author : Ethan
# @Site :  
# @File : user_behavior.py 
# @Software: PyCharm
import pandas as pd
import numpy as np
import warnings
from dateutil.relativedelta import relativedelta
from collections import Counter

warnings.filterwarnings('ignore')
pd.set_option("display.max_columns", None)
pd.set_option("display.max_rows", None)

train = pd.read_csv('xyh/data/train.csv')
test = pd.read_csv('xyh/data/test.csv')

user_behave_info = pd.read_csv('xyh/data/user_behavior_logs.csv')
user_behave_info.head()
train = train.replace(to_replace="\\N", value=np.NaN)
##
train['due_date'] = pd.to_datetime(train['due_date'])
train['repay_date'] = pd.to_datetime(train['repay_date'])
train['auditing_date'] = pd.to_datetime(train['auditing_date'])

test['due_date'] = pd.to_datetime(test['due_date'])
test['auditing_date'] = pd.to_datetime(test['auditing_date'])


time_range = list(sorted(train['auditing_date'].unique()))
time_range_test = list(sorted(test['auditing_date'].unique()))
user_behave_info['behavior_time'] = pd.to_datetime(user_behave_info['behavior_time'])
user_behave_info['map_time'] = user_behave_info['behavior_time'].dt.hour


##不同行为的次数
def difftypecount(x):
	count_ = Counter(x)
	dict_ = count_.items()
	return dict(dict_)


def map_time(x):
	if 0 <= x < 6:
		return 1
	elif 6 <= x < 12:
		return 2
	elif 12 <= x < 18:
		return 3
	else:
		return 4


"""
- behave_counts_week：T-7 ~ T-1 day，总的行为次数
- behave_rate_type(1/2/3)_week：T-7 ~ T-1 day，类型为1，2，3的行为占比
- behave_rate_time(1/2/3/4)_week：T-7 ~ T-1 day，将发生时间分为4个区段(0-5,6-11,12-17,18-23点)，计算其行为占比
- behave_counts_month：T-30~ T-1 day，总的行为次数
- behave_rate_type(1/2/3)_month：T-30 ~ T-1 day，类型为1，2，3的行为占比
- behave_rate_time(1/2/3/4)_month：T-30 ~ T-1 day，将发生时间分为4个区段(0-5,6-11,12-17,18-23点)，计算其行为占比
"""


# # prefix = 'T30'
# train_feature_table = pd.DataFrame()
# for time in time_range:
#     #往前推一个礼拜
#     before_week_start = time - relativedelta(days=30)
#     before_week_end = time - relativedelta(days=1)
#     week_range = pd.date_range(before_week_start,before_week_end)
#     #当前成交时间的标
#     tmp_train = train.loc[train['auditing_date']==time,['user_id']]

#     his_behave_info = user_behave_info[user_behave_info['behavior_time'].isin(week_range)]
#     tmp_join = tmp_train.merge(his_behave_info,on='user_id',how='left')
#     tmp_join['map_time'] = tmp_join['map_time'].map(map_time)

#     #计算总的行为次数,#计算类型为1,2,3的行为占比
#     feature_table = tmp_join.groupby('user_id').agg({'behavior_type':['count',difftypecount]})
#     feature_table.columns = pd.Index(["{}_{}".format(e[0],e[1]) for e in feature_table.columns.tolist()])
#     feature_table = feature_table.reset_index()

#     type_1 = []
#     type_2 =[]
#     type_3 =[]
#     for item in feature_table['behavior_type_difftypecount']:
#         type_1.append(item.get(1,np.nan))
#         type_2.append(item.get(2,np.nan))
#         type_3.append(item.get(3,np.nan))
#     feature_table['type_1'] = type_1
#     feature_table['type_2'] = type_2
#     feature_table['type_3'] = type_3
#     #计算不同时间段的行为占比
#     rename_col ={1:'time_1',2:'time_2',3:'time_3',4:'time_4'}
#     tmp_crosstab = pd.crosstab(tmp_join['user_id'],tmp_join['map_time'],tmp_join['behavior_type'],aggfunc='count').rename(columns=rename_col)
#     feature_table = feature_table.join(tmp_crosstab,on='user_id',how='left')

#     col_name=['type_1','type_2','type_3','time_1','time_2','time_3','time_4']
#     for col in col_name:
#         feature_table[prefix+'_'+col] = feature_table[col]/feature_table['behavior_type_count']

#     feature_table = tmp_train.merge(feature_table,on='user_id',how='left')
#     feature_table.drop(columns='behavior_type_count',inplace=True)
#     feature_table = feature_table.rename(columns={'behavior_type_count':prefix+'_'+'behavior_type_count'})
#     train_feature_table = pd.concat([train_feature_table,feature_table],axis=0)
# prefix = 'T7'
# train_feature_table = pd.DataFrame()
# time = time_range[0]
# #往前推一个礼拜
# before_week_start = time - relativedelta(days=7)
# before_week_end = time - relativedelta(days=1)
# week_range = pd.date_range(before_week_start,before_week_end)
# #当前成交时间的标
# tmp_train = train.loc[train['auditing_date']==time,['user_id']]

# his_behave_info = user_behave_info[user_behave_info['behavior_time'].isin(week_range)]
# tmp_join = tmp_train.merge(his_behave_info,on='user_id',how='left')
# tmp_join['map_time'] = tmp_join['map_time'].map(map_time)

# #计算总的行为次数,#计算类型为1,2,3的行为占比
# feature_table = tmp_join.groupby('user_id').agg({'behavior_type':['count',difftypecount]})
# feature_table.columns = pd.Index(["{}_{}".format(e[0],e[1]) for e in feature_table.columns.tolist()])
# feature_table = feature_table.reset_index()

# type_1 = []
# type_2 =[]
# type_3 =[]
# for item in feature_table['behavior_type_difftypecount']:
#     type_1.append(item.get(1,np.nan))
#     type_2.append(item.get(2,np.nan))
#     type_3.append(item.get(3,np.nan))
# feature_table['type_1'] = type_1
# feature_table['type_2'] = type_2
# feature_table['type_3'] = type_3
# #计算不同时间段的行为占比
# rename_col ={1:'time_1',2:'time_2',3:'time_3',4:'time_4'}
# tmp_crosstab = pd.crosstab(tmp_join['user_id'],tmp_join['map_time'],tmp_join['behavior_type'],aggfunc='count').rename(columns=rename_col)
# feature_table = feature_table.join(tmp_crosstab,on='user_id',how='left')
def gen_behave_feature(train_set, test_set, data):
	data['behavior_time'] = pd.to_datetime(data['behavior_time'])
	user_behave_info['map_time'] = user_behave_info['behavior_time'].dt.hour

	train_feature_table = pd.DataFrame()
	for time in time_range:
		#         #往前推一个礼拜
		#         before_week_start = time - relativedelta(days=7)
		#         before_week_end = time - relativedelta(days=1)
		#         week_range = pd.date_range(before_week_start,before_week_end)
		# 当前成交时间的标
		tmp_train = train_set.loc[train_set['auditing_date'] == time, ['user_id']]

		his_behave_info = user_behave_info[user_behave_info['behavior_time'] < time]
		tmp_join = tmp_train.merge(his_behave_info, on='user_id', how='left')
		tmp_join['map_time'] = tmp_join['map_time'].map(map_time)

		# 计算总的行为次数,#计算类型为1,2,3的行为占比
		feature_table = tmp_join.groupby('user_id').agg({'behavior_type': ['count', difftypecount]})
		feature_table.columns = pd.Index(["{}_{}".format(e[0], e[1]) for e in feature_table.columns.tolist()])
		feature_table = feature_table.reset_index()

		type_1 = []
		type_2 = []
		type_3 = []
		for item in feature_table['behavior_type_difftypecount']:
			type_1.append(item.get(1, np.nan))
			type_2.append(item.get(2, np.nan))
			type_3.append(item.get(3, np.nan))
		feature_table['type_1'] = type_1
		feature_table['type_2'] = type_2
		feature_table['type_3'] = type_3
		# 计算不同时间段的行为占比
		rename_col = {1: 'time_1', 2: 'time_2', 3: 'time_3', 4: 'time_4'}
		tmp_crosstab = pd.crosstab(tmp_join['user_id'], tmp_join['map_time'], tmp_join['behavior_type'],
		                           aggfunc='count').rename(columns=rename_col)
		feature_table = feature_table.join(tmp_crosstab, on='user_id', how='left')

		col_name = ['type_1', 'type_2', 'type_3', 'time_1', 'time_2', 'time_3', 'time_4']
		for col in col_name:
			feature_table[col] = feature_table[col] / feature_table['behavior_type_count']

		feature_table = tmp_train.merge(feature_table, on='user_id', how='left')
		feature_table.drop(columns='behavior_type_difftypecount', inplace=True)
		train_feature_table = pd.concat([train_feature_table, feature_table], axis=0)

	test_feature_table = pd.DataFrame()
	for time in time_range_test:
		#         #往前推一个礼拜
		#         before_week_start = time - relativedelta(days=7)
		#         before_week_end = time - relativedelta(days=1)
		#         week_range = pd.date_range(before_week_start,before_week_end)
		# 当前成交时间的标
		tmp_test = test_set.loc[test_set['auditing_date'] == time, ['user_id']]

		his_behave_info = user_behave_info[user_behave_info['behavior_time'] < time]
		tmp_join = tmp_test.merge(his_behave_info, on='user_id', how='left')
		tmp_join['map_time'] = tmp_join['map_time'].map(map_time)

		# 计算总的行为次数,#计算类型为1,2,3的行为占比
		feature_table = tmp_join.groupby('user_id').agg({'behavior_type': ['count', difftypecount]})
		feature_table.columns = pd.Index(["{}_{}".format(e[0], e[1]) for e in feature_table.columns.tolist()])
		feature_table = feature_table.reset_index()

		type_1 = []
		type_2 = []
		type_3 = []
		for item in feature_table['behavior_type_difftypecount']:
			type_1.append(item.get(1, np.nan))
			type_2.append(item.get(2, np.nan))
			type_3.append(item.get(3, np.nan))
		feature_table['type_1'] = type_1
		feature_table['type_2'] = type_2
		feature_table['type_3'] = type_3
		# 计算不同时间段的行为占比
		rename_col = {1: 'time_1', 2: 'time_2', 3: 'time_3', 4: 'time_4'}
		tmp_crosstab = pd.crosstab(tmp_join['user_id'], tmp_join['map_time'], tmp_join['behavior_type'],
		                           aggfunc='count').rename(columns=rename_col)
		feature_table = feature_table.join(tmp_crosstab, on='user_id', how='left')

		col_name = ['type_1', 'type_2', 'type_3', 'time_1', 'time_2', 'time_3', 'time_4']
		for col in col_name:
			feature_table[col] = feature_table[col] / feature_table['behavior_type_count']

		feature_table = tmp_test.merge(feature_table, on='user_id', how='left')
		feature_table.drop(columns='behavior_type_difftypecount', inplace=True)
		test_feature_table = pd.concat([test_feature_table, feature_table], axis=0)
	return train_feature_table, test_feature_table

if __name__ =="__main__":

	train_feature_table, test_feature_table = gen_behave_feature(train, test, user_behave_info)
	train_feature_table.to_csv('xyh/data/train_user_repay.csv', index=False)
	test_feature_table.to_csv('xyh/data/test_user_repay.csv', index=False)
