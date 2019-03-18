#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on 201901
@author: chencheng
将有效用户的数据进行清洗整理，然后提取特征，保存，一遍后续建模使用。
"""
import pandas as pd
import glob
from sklearn import preprocessing
import matplotlib.pyplot as plt
import numpy as np
import seaborn
from sklearn.decomposition import PCA

le = preprocessing.LabelEncoder()

df_user_phone = pd.read_csv("really_user_data.csv", names=["phone_nm"])


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
    df_attr = pd.read_csv("/data1/Attribute/attr201810.csv")
    df_attr = [["phone_nm","user_num_6m","jw_flag_12m","sex","age","arpu","phone_brand","cust_level","acct_charge_6m","voice_cnt_6m","sms_cnt_6m","flux_cnt_6m"]]
    df_attr['age'] = deal_age(df_attr['age'])
    df_attr['sex'] = deal_sex(df_attr['sex'])
    df_attr['phone_brand'] = deal_phone_brand(df_attr['phone_brand'])
    df_attr['cust_level'] = deal_cust_level(df_attr['cust_level'])
    df_attr.fillna(0)
    return df_attr

def analysis(df):
    # #特征分析
    #使用直方图查看数据特征
    columns = list(df.columns)
    for col_index in range(0, len(columns)):
        print("特征 %s 直方图" % columns[col_index])
        plt.hist(df[:, col_index])
        plt.show()
        
def analysis1(df):
    # 绘制皮尔逊相关系数热力图
    columns = list(df.columns)
    cm = np.corrcoef(df.T)
    seaborn.set(font_scale=1.5)
    print(columns)
    print(cm.shape)
    hm = seaborn.heatmap(cm,
                          cbar=True,
                          annot=True,
                          square=True,
                          fmt='.2f',
                          annot_kws={'size': 8},
                          yticklabels=columns,
                          xticklabels=columns)
     # # plt.tight_layout()
     #plt.savefig('相关性矩阵.png', dpi=300)
    plt.show()
 
 
def concat_data():
    '''
    清洗、整理、提取所有数据的特征，并保存
    本次为了走流程，仅使用部分特征。后续将逐步加入app、语音、短信等等其他特征。
    '''
    df_attr = get_attr()
    df0 = df_attr[~df_attr.phone_nm.isin(df_user_phone.phone_nm.tolist())]
    df0['label'] = 0
    df1 = df_attr[df_attr.phone_nm.isin(df_user_phone.phone_nm.tolist())]
    df1['label'] = 1
    df = pd.concat([df0,df1])
    print("*" * 10 + "   缺失值相关信息显示   " + "*" * 10)
    for column in list(df.columns):
        rows = df[df.loc[:,column].isnull()].loc[:, column]
        if not rows.empty:
            print("特征 %s 存在 %d 缺失值" % (column, len(rows)))
    print("*" * 50)
    #缺失值处理 ------------------- 用于完成缺失值的插补变压器
    df = preprocessing.Imputer(missing_values='NaN',strategy='mean',axis=0).fit_transform(df)
    analysis(df)
    analysis(df1)
    #特征选择
    print('*'*30)
    cc_data_tz = df[:,1:]
    pca = PCA()
    pca.fit(cc_data_tz)
    tz_score = pca.explained_variance_ratio_
    print(tz_score)
    print('*'*30)
    
    df.to_csv("all_data.csv",index=None)
    

if __name__ == "__main__":
    concat_data()



