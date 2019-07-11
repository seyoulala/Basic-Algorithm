#!/usr/bin/env python
# -*- coding: utf-8 -*-

# @Time : 2019/7/4 上午11:06 
# @Author : Ethan
# @Site :  
# @File : reg.py 
# @Software: PyCharm


import pandas as pd 
import numpy as np 
import warnings 
import os
import  calendar
import datetime
import tushare as ts
from dateutil.relativedelta import relativedelta
from lightgbm import LGBMRegressor
import  lightgbm as lgm
import seaborn as sns
import matplotlib.pyplot as plt
from sklearn.metrics import  mean_squared_error
from sklearn.model_selection import  RandomizedSearchCV

import scipy as sp
warnings.filterwarnings('ignore')
pd.set_option("display.max_rows",None)
pd.set_option("display.max_columns",None)



data_path = "./xuyinghao/data/"
train = pd.read_csv(os.path.join(data_path,'train.csv'))
test = pd.read_csv(os.path.join(data_path,'test.csv'))


train['repay_date'] = pd.to_datetime(train['repay_date'])
train['due_date'] = pd.to_datetime(train['due_date'])
train['auditing_date'] = pd.to_datetime(train['auditing_date'])
train['repay_amt']=pd.to_numeric(train['repay_amt'])

test['auditing_date'] = pd.to_datetime(test['auditing_date'])
test['due_date'] = pd.to_datetime(test['due_date'])
test['due_amt'] = pd.to_numeric(test['due_amt'])

alldays = ts.trade_cal()

def timelist(base_time):
    time_list =[]
    for i in range(1,12):
        time_list.append(base_time)
        base_time = base_time+relativedelta(months=1)
    return time_list

def istday(x):
    tradingdays = alldays[alldays['isOpen'] == 1]  
    today = x.strftime('%Y-%m-%d')
    if today in tradingdays['calendarDate'].values:
        return 1
    else:
        return 0

def generate_feature(df,time_list):
    feature_tabel = pd.DataFrame()
    for autitime in  time_list:
        #开始日期
        start = autitime
        end = autitime + pd.offsets.MonthEnd(n=2)
        range_time = pd.date_range(start=start,end=end)
        tmp_table = train.loc[train['auditing_date'].isin(range_time),:]
        min_repay_time = tmp_table['repay_date'].min()
        max_repay_time = tmp_table['repay_date'].max()
        timeseries = pd.date_range(start=min_repay_time,end=max_repay_time)
        flag = range_time[0].strftime('%Y-%m-%d')+"-"+range_time[-1].strftime('%Y-%m-%d')
        for repay_time in timeseries:
            tmp_df = pd.DataFrame(index=[0])
            tmp_df['flag'] = flag
            tmp_df['repay_time']=repay_time
            tmp_df['month']=repay_time.month
            tmp_df['month_day']=repay_time.day
            tmp_df['weekday'] = repay_time.weekday()
            #当前月天数以及当前时间天的差值
            tmp_df['month_day_L']=repay_time.daysinmonth - repay_time.day
            #当前时间是否交易日
            tmp_df['istday'] = istday(repay_time)
            ##T+1/2/3/4/5/6是否为交易日
            for time  in [1,2,3,4,5]:
                now_time=repay_time +relativedelta(days=time)
                tmp_df['istday_{}'.format(time)]=istday(now_time)
            ##还款特征
            #第一期还款日为
            tmp_df['due_amount'] = tmp_table.loc[tmp_table['due_date']==repay_time,'due_amt'].sum()
            ##due_amount_(1/2/3/4/5)：第一期还款日为T+(1/2/3/4/5)日的标的应还款总额
            for time in [1,2,3,4,5]:
                now_time=repay_time+relativedelta(days=time)
                tmp_df['due_amount_{}'.format(time)] = tmp_table.loc[tmp_table['due_date']==now_time,'due_amt'].sum()


            ##T日可能还款的标的应还款总额(T日往前推一个月
            #比如实际还款日为３月９号，那么可能在３月９号还款的应该为借款日在２月９号－３月９号以及应还款日在３月９号－４月９号的所有应还款总额 
            before_time = repay_time-relativedelta(months=1)
            after_time = repay_time+relativedelta(months=1)
            autiding_range = pd.date_range(before_time,repay_time)
            due_range = pd.date_range(repay_time,after_time)
            tmp_df['due_amount_sum_month']=tmp_table.loc[(tmp_table['auditing_date'].isin(autiding_range))|(tmp_table['due_date'].isin(due_range)),'due_amt'].sum()

            #due_amount_sum_10：第一期还款日为T日~T+10日的标的应还款总额
            now_time = repay_time+relativedelta(days=10)
            tmp_df['due_amount_sum_10']=tmp_table.loc[(tmp_table['due_date']>=repay_time)&(tmp_table['due_date']<=now_time),'due_amt'].sum()
            #due_amount_sum_20：第一期还款日为T日~T+20日的标的应还款总额
            now_time = repay_time+relativedelta(days=20)
            tmp_df['due_amount_sum_20']=tmp_table.loc[(tmp_table['due_date']>=repay_time)&(tmp_table['due_date']<=now_time),'due_amt'].sum()

            ## repay_time 实际还款总额
            tmp_df['label'] = tmp_table.loc[tmp_table['repay_date']==repay_time,'repay_amt'].sum()
            feature_tabel = pd.concat([feature_tabel,tmp_df],axis=0)
    feature_tabel.reset_index(drop=True,inplace=True)
    return feature_tabel
    
### 测试集
def generate_feature_test(df,time_list):
    feature_tabel = pd.DataFrame()
    for repay_time in time_list:
        tmp_df = pd.DataFrame(index=[0])
        tmp_df['repay_time']=repay_time
        tmp_df['month']=repay_time.month
        tmp_df['month_day']=repay_time.day
        tmp_df['weekday'] = repay_time.weekday()
        #当前月天数以及当前时间天的差值
        tmp_df['month_day_L']=repay_time.daysinmonth - repay_time.day
        #当前时间是否交易日
        tmp_df['istday'] = istday(repay_time)
        ##T+1/2/3/4/5/6是否为交易日
        for time  in [1,2,3,4,5]:
            now_time=repay_time +relativedelta(days=time)
            tmp_df['istday_{}'.format(time)]=istday(now_time)
        ##还款特征
        #第一期还款日为
        tmp_df['due_amount'] = df.loc[df['due_date']==repay_time,'due_amt'].sum()
        ##due_amount_(1/2/3/4/5)：第一期还款日为T+(1/2/3/4/5)日的标的应还款总额
        for time in [1,2,3,4,5]:
            now_time=repay_time+relativedelta(days=time)
            tmp_df['due_amount_{}'.format(time)] = df.loc[df['due_date']==now_time,'due_amt'].sum()


        ##T日可能还款的标的应还款总额(T日往前推一个月
        #比如实际还款日为３月９号，那么可能在３月９号还款的应该为借款日在２月９号－３月９号以及应还款日在３月９号－４月９号的所有应还款总额 
        before_time = repay_time-relativedelta(months=1)
        after_time = repay_time+relativedelta(months=1)
        autiding_range = pd.date_range(before_time,repay_time)
        due_range = pd.date_range(repay_time,after_time)
        tmp_df['due_amount_sum_month']=df.loc[(df['auditing_date'].isin(autiding_range))|(df['due_date'].isin(due_range)),'due_amt'].sum()

        #due_amount_sum_10：第一期还款日为T日~T+10日的标的应还款总额
        now_time = repay_time+relativedelta(days=10)
        tmp_df['due_amount_sum_10']=df.loc[(df['due_date']>=repay_time)&(df['due_date']<=now_time),'due_amt'].sum()
        #due_amount_sum_20：第一期还款日为T日~T+20日的标的应还款总额
        now_time = repay_time+relativedelta(days=20)
        tmp_df['due_amount_sum_20']=df.loc[(df['due_date']>=repay_time)&(df['due_date']<=now_time),'due_amt'].sum()

        feature_tabel = pd.concat([feature_tabel,tmp_df],axis=0)
    feature_tabel.reset_index(drop=True,inplace=True)
    return feature_tabel

def regression_lgb(train,test=None):
    predictors=list(filter(lambda x: x not in['repay_time','flag','label'],train.columns))
    train_df = train[train['flag']!="2018-11-01-2018-12-31"]
    valid_df = train[train['flag']=='2018-11-01-2018-12-31']
    label = train_df['label']
    
    params ={'reg_lambda': 0.2,
                     'reg_alpha': 0.7, 
                     'num_leaves': 32, 
                     'n_estimators': 1475,
                     'min_split_gain': 0.02,
                     'max_depth': 4, 
                     'learning_rate': 0.07,
                     'colsample_bytree':0.9,
                     'boosting_type': 'gbdt'}
    model = LGBMRegressor(**params)
    
    model.fit(train_df[predictors],label,eval_metric='mse')
    predict = model.predict(valid_df[predictors])
    valid_df['prediction']=predict
    
    sub_test = model.predict(test[predictors])
    test['prediction'] = sub_test
    print("valid rmse is %f"%(np.sqrt(mean_squared_error(valid_df['label'],predict))))
    
    return valid_df,test


if __name__ == '__main__':
	base_time = datetime.datetime(2018,1,1)
	time_range  = timelist(base_time)
	###测试集成交日区间
	start_time_test = test['auditing_date'].min()
	end_time_test = test['auditing_date'].max()
	time_range_test = pd.date_range(start=start_time_test,end=end_time_test+relativedelta(months=1))

	train_feature =  generate_feature(train,time_range)
	test_feature = generate_feature_test(test,time_range_test)

	valid,sub = regression_lgb(train_feature,test_feature)
	





