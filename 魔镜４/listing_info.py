#!/usr/bin/env python
# -*- coding: utf-8 -*-

# @Time : 2019/7/11 下午2:41 
# @Author : Ethan
# @Site :  
# @File : listing_info.py 
# @Software: PyCharm

import pandas as pd
import numpy as np
import warnings

warnings.filterwarnings('ignore')
pd.set_option("display.max_columns", None)
pd.set_option("display.max_rows", None)

train = pd.read_csv('data/train.csv')
test = pd.read_csv('data/test.csv')

listing_info = pd.read_csv('data/listing_info.csv')
listing_info.head()
train = train.replace(to_replace="\\N", value=np.NaN)

train['due_date'] = pd.to_datetime(train['due_date'])
train['repay_date'] = pd.to_datetime(train['repay_date'])
train['auditing_date'] = pd.to_datetime(train['auditing_date'])

test['due_date'] = pd.to_datetime(test['due_date'])
test['auditing_date'] = pd.to_datetime(test['auditing_date'])

start_time = train['auditing_date'].min()
end_time = train['auditing_date'].max()

start_time_test = test['auditing_date'].min()
end_time_test = test['auditing_date'].max()

time_range = pd.date_range(start=start_time, end=end_time)
time_range_test = pd.date_range(start=start_time_test, end=end_time_test)
listing_info['auditing_date'] = pd.to_datetime(listing_info['auditing_date'])

agg_ = {
	'listing_id': ['nunique'],
	'term': ['min', 'max', 'mean'],
	'rate': ['min', 'max', 'mean'],
	'principal': ['min', 'max', 'mean']

}
train_feature_table = pd.DataFrame()
for time in time_range:
	tmp_train = train.loc[train['auditing_date'] == time, ['user_id']]
	his_listing = listing_info.loc[listing_info['auditing_date'] < time, :]
	tmp_join = tmp_train.merge(his_listing, on='user_id', how='left')
	feature_table = tmp_join.groupby('user_id').agg(agg_)
	feature_table.columns = pd.Index(["{}_{}".format(e[0], e[1]) for e in feature_table.columns.tolist()])
	feature_table = feature_table.reset_index()
	feature_table = tmp_train.merge(feature_table, on='user_id', how='left')
	train_feature_table = pd.concat([train_feature_table, feature_table], axis=0)

test_feature_table = pd.DataFrame()
for time in time_range_test:
	tmp_test = test.loc[test['auditing_date'] == time, ['user_id']]
	his_listing = listing_info.loc[listing_info['auditing_date'] < time, :]
	tmp_join = tmp_test.merge(his_listing, on='user_id', how='left')
	feature_table = tmp_join.groupby('user_id').agg(agg_)
	feature_table.columns = pd.Index(["{}_{}".format(e[0], e[1]) for e in feature_table.columns.tolist()])
	feature_table = feature_table.reset_index()
	feature_table = tmp_test.merge(feature_table, on='user_id', how='left')
	test_feature_table = pd.concat([test_feature_table, feature_table], axis=0)

##当前标的信息
train_listing_now = train.merge(listing_info, on=['user_id', 'listing_id', 'auditing_date'], how='left')
test_listing_now = test.merge(listing_info, on=['user_id', 'listing_id', 'auditing_date'], how='left')
train_listing_now.head()
##
train_feature_table = train_feature_table.sort_values(by='user_id').reset_index(drop=True)
test_feature_table = test_feature_table.sort_values(by='user_id').reset_index(drop=True)
train_listing_now = train_listing_now.sort_values(by='user_id').reset_index(drop=True)
test_listing_now = test_listing_now.sort_values(by='user_id').reset_index(drop=True)

train_feature_table = pd.concat([train_feature_table, train_listing_now[['term', 'rate', 'principal']]], axis=1)
test_feature_table = pd.concat([test_feature_table, test_listing_now[['term', 'rate', 'principal']]], axis=1)

train_feature_table.head()
##衍生利率是否提高,期数是否提高，贷款金额是否提高
train_feature_table['rate_more_flag'] = train_feature_table.apply(
	lambda x: 1 if (x['rate'] - x['rate_mean']) > 0 else 0, axis=1)
test_feature_table['rate_more_flag'] = test_feature_table.apply(lambda x: 1 if (x['rate'] - x['rate_mean']) > 0 else 0,
                                                                axis=1)

##期数是否变高
train_feature_table['term_more_flag'] = train_feature_table.apply(
	lambda x: 1 if (x['term'] - x['term_mean']) > 0 else 0, axis=1)
test_feature_table['term_more_flag'] = test_feature_table.apply(lambda x: 1 if (x['term'] - x['term_mean']) > 0 else 0,
                                                                axis=1)

##贷款金额是否提高
train_feature_table['principal_more_flag'] = train_feature_table.apply(
	lambda x: 1 if (x['principal'] - x['principal_mean']) > 0 else 0, axis=1)
test_feature_table['principal_more_flag'] = test_feature_table.apply(
	lambda x: 1 if (x['principal'] - x['principal_mean']) > 0 else 0, axis=1)

train_feature_table.head()
test_feature_table.head()
train_feature_table.to_csv("train_listing_info_feature.csv", index=False)
test_feature_table.to_csv("test_listing_info_feature.csv", index=False)
