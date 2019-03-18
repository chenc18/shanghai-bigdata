#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on 201901
@author: chencheng
"""
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import seaborn
from sklearn import preprocessing
from sklearn.linear_model import LogisticRegression
from sklearn.metrics import confusion_matrix
from scipy.interpolate import lagrange #导入拉格朗日插值函数
from sklearn.decomposition import PCA
from sklearn.cross_validation import train_test_split
import cc_tools


df = pd.read_csv('user_all_data.csv')

def main():
    '''
    建立模型，
    '''
    lr = LogisticRegression(penalty='l1')
    x1_train, x1_test, y1_train, y1_test = train_test_split(df[:,2:], df[:.0], test_size=0.3, random_state=0)
    lr.fit(x1_train,y1_train)
    train_y_predict = lr.predict(x1_test)
    confmat = confusion_matrix(y1_test, train_y_predict)
    print(confmat)  
    
    #计算WOE
    train_woe = []
    train_woe.append(cc_tools.calc_woe(x1_train[:, 0], y1_train, [-1, 30, 35, 40, 45, 50, 55, 65, 70, 75, 1000]))
    train_woe.append(cc_tools.calc_woe(x1_train[:, 1], y1_train, [-1, 0, 1, 3, 5, 1000]))
    train_woe.append(cc_tools.calc_woe(x1_train[:, 2], y1_train, [-1, 1000, 2000, 3000, 4000, 5000, 6000, 7000, 8000, 9000, 10000,11000,12000,10000000]))
    train_woe.append(cc_tools.calc_woe(x1_train[:, 3], y1_train, [-1, 0, 1, 3, 5, 10, 1000]))
    train_woe.append(cc_tools.calc_woe(x1_train[:, 4], y1_train, [-1, 0, 1, 2, 3, 5, 1000]))
    train_woe.append(cc_tools.calc_woe(x1_train[:, 5], y1_train, [-1, 0, 1, 3, 5, 1000]))
    train_woe.append(cc_tools.calc_woe(x1_train[:, 6], y1_train, [-1, 0, 1, 2, 3, 5, 1000]))
    #print("*" * 10 + "   WOE值的显示   " + "*" * 10)
    #print(train_woe[0])
    
    #将原数据中的数据换成WOE值
    #enumerate---python内置函数，返回序列元素和序号
    cc_train_X_woe = np.zeros_like(x1_train)
    for idx, woes in enumerate(train_woe):
        for woe in woes:
            tmp = x1_train[:, idx]
            cc_train_X_woe[np.logical_and(tmp > woe[1][0], tmp <= woe[1][1]), idx] = woe[0]
    
    lr_woe = LogisticRegression()
    lr_woe.fit(cc_train_X_woe, y1_train)
    coef = lr_woe.coef_       #得到的为权重
    intercept = lr.intercept_
    #y = ax + b    coef相当于a,intercept相当于b
    
    p = 20/np.log(2)
    q = 600-20*np.log(15)/np.log(2)
    
    base_score = q + p * intercept
    
    train_woe_score = []
    for idx, woes in enumerate(train_woe):
        tmp = []
        for woe in woes:
            tmp.append([int(woe[0]*p*coef[0, idx]), woe[1]])
        train_woe_score.append(tmp)
    
    print(train_woe_score)
    return train_woe_score,base_score
    
    
#将评分卡输出保存，然后单独写一个文件用来传入特征得到分数。是用户可以手动一次输入各特征
def getScore(data_one,score_bz,base_score):
    score = base_score
    for i in range(len(data_one)):
        x_scores = score_bz[i]
        for j in range(len(x_scores)):
            if data_one[i] in range(int(x_scores[j][1][0]),int(x_scores[j][1][1])):
                score = score + x_scores[j][0]
                break;
    return score    
    
    
def get_user(m,score_bz,base_score):
    '''
    对所有用户进行评分，保存评分前m的用户
    '''
    df = pd.read_csv("all_data.csv")
    df['socre'] = df.apply(getScore(df[:,1:],score_bz,base_score))
    df = df.sort_vales(by='socre')
    df = df[:m,:]
    df.to_csv("phone_end.csv",index=None)


if __name__ == "__main__":
    train_woe_score,base_score = main()
    get_user(m=10000,train_woe_score,base_score)
