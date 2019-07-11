#!/usr/bin/env python
# -*- coding: utf-8 -*-

# @Time : 2019/7/11 下午2:51 
# @Author : Ethan
# @Site :  
# @File : 回归模型.py 
# @Software: PyCharm
import pandas as pd
import numpy as np
import warnings
import os
import calendar
import datetime
import tushare as ts
from dateutil.relativedelta import relativedelta
from lightgbm import LGBMRegressor
import lightgbm as lgm
import seaborn as sns
import matplotlib.pyplot as plt
from sklearn.metrics import mean_squared_error
from sklearn.model_selection import RandomizedSearchCV

import scipy as sp

warnings.filterwarnings('ignore')
pd.set_option("display.max_rows", None)
pd.set_option("display.max_columns", None)

data_path = "./xyh/data/"
train = pd.read_csv(os.path.join(data_path, 'train.csv'))
test = pd.read_csv(os.path.join(data_path, 'test.csv'))
### 标的信息
listing_info = pd.read_csv('xyh/data/listing_info.csv')
train.head()
test.head()
train = train.replace(to_replace='\\N', value=np.NaN)
train['repay_date'] = pd.to_datetime(train['repay_date'])
train['due_date'] = pd.to_datetime(train['due_date'])
train['auditing_date'] = pd.to_datetime(train['auditing_date'])
train['repay_amt'] = pd.to_numeric(train['repay_amt'])
##类型转换
test['auditing_date'] = pd.to_datetime(test['auditing_date'])
test['due_date'] = pd.to_datetime(test['due_date'])
test['due_amt'] = pd.to_numeric(test['due_amt'])


def timelist(base_time):
	time_list = []
	for i in range(1, 12):
		time_list.append(base_time)
		base_time = base_time + relativedelta(months=1)
	return time_list


def cut_dataframe(df, time_list):
	for time in time_list:
		start_time = time
		end_time = time + pd.offsets.MonthEnd(n=2)
		time_range = pd.date_range(start=start_time, end=end_time)
		tmp_df = df.loc[df['repay_time'].isin(time_range), :]
		tmp_df.to_csv('./xuyinghao/data/{}.csv'.format(time.date()))


base_time = datetime.datetime(2018, 1, 1)

###所有交易日
alldays = ts.trade_cal()


##判断是否时交易日
def istday(x):
	tradingdays = alldays[alldays['isOpen'] == 1]  # 开盘日
	today = x.strftime('%Y-%m-%d')
	if today in tradingdays['calendarDate'].values:
		return 1
	else:
		return 0


##训练集实际还款日区间
start_time = train['repay_date'].min()
end_time = train['repay_date'].max()

time_range = pd.date_range(start=start_time, end=end_time)
###测试集成交日区间
start_time_test = test['auditing_date'].min()
end_time_test = test['auditing_date'].max()

# 可能还款区间
time_range_test = pd.date_range(start=start_time_test, end=end_time_test + relativedelta(months=1))

tmp_df = pd.DataFrame(columns=['date', 'istday'])
tmp_df['date'] = pd.date_range(start='2018-1-1', end='2019-12-31')
tmp_df['istday'] = tmp_df['date'].map(lambda x: istday(x))
for i in [1, 2, 3, 4, 5]:
	tmp_df['istday_{}'.format(i)] = tmp_df['date'].map(lambda x: istday(x + relativedelta(days=i)))
###以auditing_date为主键聚合求利率的平均
weigth = pd.crosstab(listing_info['auditing_date'], listing_info['rate'], margins=True)
weigth = weigth.reset_index()
col_name = {6.5: '6.5', 6.9: '6.9', 7.2: '7.2', 7.6: '7.6', 8.0: '8.0', 8.3: '8.3', 8.6: '8.6', 9.3: '9.3'}
weigth = weigth.rename(columns=col_name)
weigth['avg_weight'] = weigth.apply(lambda x: (x['6.5'] * 6.5 + x['6.9'] * 6.9 + x['7.2'] * 7.2 + x['8.0'] * 8.0 + x[
	'8.3'] * 8.3 + x['8.6'] * 8.6 + x['9.3'] * 9.3) / x['All'], axis=1)
weigth = weigth.drop(axis=1, index=998)
weigth['auditing_date'] = pd.to_datetime(weigth['auditing_date'])
x = pd.DataFrame({'auditing_date': pd.date_range('2019-4-1', '2019-12-31')})
weigth = pd.concat([weigth, x], axis=0)

### 没有2个月滚动切分
# feature_tabel1
"""
### 每日滚动切分
"""


def generate_feature(df, time_list):
	feature_tabel = pd.DataFrame()
	for autitime in time_list:
		# 开始日期
		start = autitime
		end = autitime + pd.offsets.MonthEnd(n=2)
		range_time = pd.date_range(start=start, end=end)
		tmp_table = train.loc[train['auditing_date'].isin(range_time), :]
		#         min_repay_time = tmp_table['repay_date'].min()
		#         max_repay_time = tmp_table['repay_date'].max()
		timeseries = pd.date_range(start=start, end=end + relativedelta(months=1))
		#         flag = range_time[0].strftime('%Y-%m-%d')+"-"+range_time[-1].strftime('%Y-%m-%d')
		flag = autitime
		for repay_time in timeseries:
			tmp_df = pd.DataFrame(index=[0])
			tmp_df['flag'] = flag
			tmp_df['repay_time'] = repay_time
			tmp_df['month'] = repay_time.month
			tmp_df['month_day'] = repay_time.day
			tmp_df['weekday'] = repay_time.weekday()
			# 当前月天数以及当前时间天的差值
			tmp_df['month_day_L'] = repay_time.daysinmonth - repay_time.day
			# 当前时间是否交易日
			tmp_df['istday'] = istday(repay_time)
			##T+1/2/3/4/5/6是否为交易日
			for time in [1, 2, 3, 4, 5]:
				now_time = repay_time + relativedelta(days=time)
				tmp_df['istday_{}'.format(time)] = istday(now_time)
			##还款特征
			# 第一期还款日为
			tmp_df['due_amount'] = tmp_table.loc[tmp_table['due_date'] == repay_time, 'due_amt'].sum()
			auditing_time = repay_time - relativedelta(months=1)
			tmp_df['rate_weight'] = weigth.loc[weigth['auditing_date'] == auditing_time, 'avg_weight'].values
			##due_amount_(1/2/3/4/5)：第一期还款日为T+(1/2/3/4/5)日的标的应还款总额
			for time in [1, 2, 3, 4, 5]:
				now_time = repay_time + relativedelta(days=time)
				tmp_df['due_amount_{}'.format(time)] = tmp_table.loc[tmp_table['due_date'] == now_time, 'due_amt'].sum()

			##当天借款总额
			tmp_df['load_amount'] = tmp_table.loc[
				tmp_table['due_date'] == (autitime + relativedelta(months=1)), 'due_amt'].sum()
			##T日可能还款的标的应还款总额(T日往前推一个月
			# 比如实际还款日为３月９号，那么可能在３月９号还款的应该为借款日在２月９号－３月９号以及应还款日在３月９号－４月９号的所有应还款总额
			before_time = repay_time - relativedelta(months=1)
			after_time = repay_time + relativedelta(months=1)
			autiding_range = pd.date_range(before_time, repay_time)
			due_range = pd.date_range(repay_time, after_time)
			tmp_df['due_amount_sum_month'] = tmp_table.loc[(tmp_table['auditing_date'].isin(autiding_range)) | (
				tmp_table['due_date'].isin(due_range)), 'due_amt'].sum()
			# T日可能还款的利率的加权平均
			tmp_df['rate_weight_month'] = weigth.loc[weigth['auditing_date'].isin(autiding_range), 'avg_weight'].mean()
			# due_amount_sum_10：第一期还款日为T日~T+10日的标的应还款总额
			now_time = repay_time + relativedelta(days=10)
			tmp_df['due_amount_sum_10'] = tmp_table.loc[
				(tmp_table['due_date'] >= repay_time) & (tmp_table['due_date'] <= now_time), 'due_amt'].sum()
			# due_amount_sum_20：第一期还款日为T日~T+20日的标的应还款总额
			now_time = repay_time + relativedelta(days=20)
			tmp_df['due_amount_sum_20'] = tmp_table.loc[
				(tmp_table['due_date'] >= repay_time) & (tmp_table['due_date'] <= now_time), 'due_amt'].sum()

			## repay_time 实际还款总额
			tmp_df['label'] = tmp_table.loc[tmp_table['repay_date'] == repay_time, 'repay_amt'].sum()
			feature_tabel = pd.concat([feature_tabel, tmp_df], axis=0)
	feature_tabel.reset_index(drop=True, inplace=True)
	return feature_tabel


time_list = pd.date_range(start='2018-1-1', end='2018-12-31')
feature_tabel = generate_feature(train, time_list)
feature_tabel.head()


### 测试集
def generate_feature_test(df, time_list):
	feature_tabel = pd.DataFrame()
	for autitime in time_list:
		# 开始日期
		start = autitime
		end = autitime + pd.offsets.MonthEnd(n=2)
		range_time = pd.date_range(start=start, end=end)
		tmp_table = df.loc[df['auditing_date'].isin(range_time), :]
		#         min_repay_time = tmp_table['repay_date'].min()
		#         max_repay_time = tmp_table['repay_date'].max()
		timeseries = pd.date_range(start=start, end=end + relativedelta(months=1))
		#         flag = range_time[0].strftime('%Y-%m-%d')+"-"+range_time[-1].strftime('%Y-%m-%d')
		flag = autitime
		for repay_time in timeseries:
			tmp_df = pd.DataFrame(index=[0])
			tmp_df['flag'] = flag
			tmp_df['repay_time'] = repay_time
			tmp_df['month'] = repay_time.month
			tmp_df['month_day'] = repay_time.day
			tmp_df['weekday'] = repay_time.weekday()
			# 当前月天数以及当前时间天的差值
			tmp_df['month_day_L'] = repay_time.daysinmonth - repay_time.day
			# 当前时间是否交易日
			tmp_df['istday'] = istday(repay_time)
			##T+1/2/3/4/5/6是否为交易日
			for time in [1, 2, 3, 4, 5]:
				now_time = repay_time + relativedelta(days=time)
				tmp_df['istday_{}'.format(time)] = istday(now_time)
			##还款特征
			# 第一期还款日为
			tmp_df['due_amount'] = tmp_table.loc[tmp_table['due_date'] == repay_time, 'due_amt'].sum()
			auditing_time = repay_time - relativedelta(months=1)
			tmp_df['rate_weight'] = weigth.loc[weigth['auditing_date'] == auditing_time, 'avg_weight'].values
			##due_amount_(1/2/3/4/5)：第一期还款日为T+(1/2/3/4/5)日的标的应还款总额
			for time in [1, 2, 3, 4, 5]:
				now_time = repay_time + relativedelta(days=time)
				tmp_df['due_amount_{}'.format(time)] = tmp_table.loc[tmp_table['due_date'] == now_time, 'due_amt'].sum()

			##当天借款总额
			tmp_df['load_amount'] = tmp_table.loc[
				tmp_table['due_date'] == (autitime + relativedelta(months=1)), 'due_amt'].sum()
			##T日可能还款的标的应还款总额(T日往前推一个月
			# 比如实际还款日为３月９号，那么可能在３月９号还款的应该为借款日在２月９号－３月９号以及应还款日在３月９号－４月９号的所有应还款总额
			before_time = repay_time - relativedelta(months=1)
			after_time = repay_time + relativedelta(months=1)
			autiding_range = pd.date_range(before_time, repay_time)
			due_range = pd.date_range(repay_time, after_time)
			tmp_df['due_amount_sum_month'] = tmp_table.loc[(tmp_table['auditing_date'].isin(autiding_range)) | (
				tmp_table['due_date'].isin(due_range)), 'due_amt'].sum()
			# T日可能还款的利率的加权平均
			tmp_df['rate_weight_month'] = weigth.loc[weigth['auditing_date'].isin(autiding_range), 'avg_weight'].mean()
			# due_amount_sum_10：第一期还款日为T日~T+10日的标的应还款总额
			now_time = repay_time + relativedelta(days=10)
			tmp_df['due_amount_sum_10'] = tmp_table.loc[
				(tmp_table['due_date'] >= repay_time) & (tmp_table['due_date'] <= now_time), 'due_amt'].sum()
			# due_amount_sum_20：第一期还款日为T日~T+20日的标的应还款总额
			now_time = repay_time + relativedelta(days=20)
			tmp_df['due_amount_sum_20'] = tmp_table.loc[
				(tmp_table['due_date'] >= repay_time) & (tmp_table['due_date'] <= now_time), 'due_amt'].sum()

			feature_tabel = pd.concat([feature_tabel, tmp_df], axis=0)
	feature_tabel.reset_index(drop=True, inplace=True)
	return feature_tabel


time_range_test = pd.date_range(start='2019-2-1', end='2019-3-31')
feature_tabel_test = generate_feature_test(test, time_range_test)
LGBMRegressor()

param_grid = {
	'boosting_type': ['gbdt'],
	'n_estimators': list(np.arange(100, 3000, step=10)),
	'num_leaves': list(range(20, 150)),
	'learning_rate': list(np.logspace(np.log10(0.005), np.log10(0.5), base=10, num=1000)),
	'subsample_for_bin': list(range(20000, 300000, 20000)),
	'min_child_samples': list(range(20, 500, 5)),
	'reg_alpha': list(np.linspace(0, 1)),
	'reg_lambda': list(np.linspace(0, 1)),
	'colsample_bytree': list(np.linspace(0.6, 1, 10)),
	'subsample': list(np.linspace(0.5, 1, 100)),
}
predictors = list(filter(lambda x: x not in ['repay_time', 'flag', 'label'], feature_tabel.columns))
model = LGBMRegressor()
random_search = RandomizedSearchCV(model, param_distributions=param_grid, n_iter=1000, scoring='neg_mean_squared_error',
                                   n_jobs=8, cv=5)
date_range = pd.date_range(start='2018-1-1', end='2018-10-31')
train_df = feature_tabel[feature_tabel['flag'].isin(date_range)]
data = np.array(train_df[predictors])
label = np.array(train_df['label'])
random_search.fit(data, label)

random_params_tabel = pd.DataFrame(random_search.cv_results_)
random_params_tabel.to_csv("random_search_params.csv", index=False)


def report(results, n_top=5):
	for i in range(1, n_top + 1):
		candidates = np.flatnonzero(results['rank_test_score'] == i)
		for candidate in candidates:
			print("Model with rank: {0}".format(i))
			print("Mean validation score: {0:.3f} (std: {1:.3f})".format(
				results['mean_test_score'][candidate],
				results['std_test_score'][candidate]))
			print("Parameters: {0}".format(results['params'][candidate]))
			print("")


# report(random_search.cv_results_)
def regression_lgb(train, test=None):
	predictors = list(filter(lambda x: x not in ['repay_time', 'flag', 'label'], train.columns))
	date_range = pd.date_range(start='2018-1-1', end='2018-10-31')
	train_df = train[train['flag'].isin(date_range)]
	valid_df = train[train['flag'] == '2018-11-01']
	label = train_df['label']

	#     params ={'reg_lambda': 0.2,
	#                      'reg_alpha': 0.7,
	#                      'num_leaves': 32,
	#                      'n_estimators': 1800,
	#                      'min_split_gain': 0.02,
	#                      'max_depth': 4,
	#                      'learning_rate': 0.07,
	#                      'colsample_bytree': 0.9,
	#                      'boosting_type': 'gbdt'}
	params = {'n_estimators': 3000,
	          'subsample_for_bin': 40000,
	          'subsample': 0.8535353535353536,
	          'reg_lambda': 0.3061224489795918,
	          'reg_alpha': 0.36734693877551017,
	          'num_leaves': 57,
	          'min_child_samples': 40,
	          'learning_rate': 0.14074061802537896,
	          'colsample_bytree': 0.9111111111111111,
	          'boosting_type': 'gbdt'}
	model = LGBMRegressor(**params)

	model.fit(train_df[predictors], label, eval_metric='mse')
	predict = model.predict(valid_df[predictors])
	valid_df['prediction'] = predict

	sub_test = model.predict(test[predictors])
	test['prediction'] = sub_test
	print("valid rmse is %f" % (np.sqrt(mean_squared_error(valid_df['label'], predict))))

	return valid_df, test


val, sub = regression_lgb(feature_tabel, feature_tabel_test)

flag_list = pd.date_range(start='2018-11-1', end='2018-12-31')
for i, flag in enumerate(flag_list[:10]):
	plt.figure(figsize=(14, 28))
	plt.subplot(10, 1, i + 1)
	tmp_df = val[val['flag'] == flag]
	x = np.arange(tmp_df.shape[0])
	width = 0.4
	plt.bar(x, tmp_df['label'], width=0.4, label='label')
	plt.bar(x + width, tmp_df['prediction'], width=0.4, label='predict')
	plt.xticks(ticks=x, labels=tmp_df['repay_time'], rotation=90)
	plt.legend(loc='best')
	plt.show()


val.to_csv('xyh/data/2019-11-12.csv', index=False)
sub[sub['flag'] == '2019-02-01'].to_csv('xyh/data/2019-3-4.csv', index=False)
