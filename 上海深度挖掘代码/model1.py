#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created 201901
@author: chencheng
对与行业电话有过语音来往的数据进行数据分析，建立模型。得到真实的客户。
当前走流程为加入很多特征，只选取部分特征。后期优化逐渐增加有效特征
"""
import pandas as pd
from sklearn import preprocessing
from sklearn import datasets as dss
from sklearn.cross_validation import train_test_split
from sklearn.cluster import KMeans, DBSCAN

import matplotlib.pyplot as plt

le = preprocessing.LabelEncoder()

df_call_phone = pd.read_csv("/data1/machine_learning01/yy_phone_all.csv", names=["phone_nm"])



def deal_age(series):
    series[~((series>18)|(series<80))] = series.mean()
    return series

def deal_sex(series):
    le.fit(['F','M','U'])
    return le.transform(series)

def deal_phone_brand(series):
    spliter = (series=='苹果')|(series=='欧珀')|(series=='维沃')|(series=='华为')|(series=='小米')|(series=='荣耀')|(series=='三星')
    series[~spliter] = '其它'
    le.fit(['苹果','欧珀','维沃','华为','小米','荣耀','三星','其它'])
    return le.transform(series)

def deal_cust_level(series):
    series[series=='一星忠诚用户'] = '一星用户'
    series[series=='二星忠诚用户'] = '二星用户'
    series[series=='三星忠诚用户'] = '三星用户'
    series[series=='四星忠诚用户'] = '四星用户'
    series[series=='五星忠诚用户'] = '五星用户'
    spliter = (series=='一星用户')|(series=='二星用户')|(series=='三星用户')|(series=='四星用户')|(series=='五星用户')
    series[~spliter] = '其它'
    le.fit(['一星用户','二星用户','三星用户','四星用户','五星用户','其它'])
    return le.transform(series)

def get_attr():
    '''
    提取用户属性数据，并对其进行处理
    '''
    df_attr_all = pd.read_csv("/data1/Attribute/attr201810.csv")
    df_attr = df_attr_all[df_attr_all.phone_nm.isin(df_call_phone.phone_nm.tolist())]
    df_attr = [["phone_nm","user_num_6m","jw_flag_12m","sex","age","arpu","phone_brand","cust_level","acct_charge_6m","voice_cnt_6m","sms_cnt_6m","flux_cnt_6m"]]
    df_attr['age'] = deal_age(df_attr['age'])
    df_attr['sex'] = deal_sex(df_attr['sex'])
    df_attr['phone_brand'] = deal_phone_brand(df_attr['phone_brand'])
    df_attr['cust_level'] = deal_cust_level(df_attr['cust_level'])
    df_attr.fillna(0)
    return df_attr

def k():
    #确认k值,
    df_attr = get_attr()
    inertia = []
    for k in range(1, 20):
        km = KMeans(n_clusters=k, init='random')
        km.fit(df_attr[:,1:])
        inertia.append(km.inertia_)
    
    plt.plot(list(range(1, 20)), inertia)
    plt.show()

def main():
    '''
    对当前数据进行聚类分析，得出真实的有效客户。
    '''
    df_attr = get_attr()
    km = KMeans(n_clusters=2, init='random', tol=1e-4)
    y_predict = km.fit_predict(df_attr[:,1:])
    df_attr["types"] = list(y_predict)
    df = df_attr[df_attr.types==1]
    print("类别为0的长度%s，为1的长度：%s" % (len(df), len(df_attr)-len(df) ))
    df_phone = df[["phone_nm"]]
    df_phone.to_csv("really_user_data.csv",index=None)
    

if __name__ == "__main__":
    main()



