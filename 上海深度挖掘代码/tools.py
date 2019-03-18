# -*- coding: utf-8 -*-
"""
Created on 201901

@author: Chencheng
"""

import numpy as np
import matplotlib.pyplot as plt


def train_test_split(data,test_size=0.3):
    '''
    分割数据集，保证数据中为0和为1的分割比例一样
    返回值： 训练集、测试集
    '''
#    data0将数据为0的数据按照比例划分
    data0 = data[data[:,0]==0]
    data0_test_len = int(len(data0) * test_size)
    data0_test = data0[:data0_test_len]
    data0_train = data0[data0_test_len:]

#    data1将数据为1的数据按照比例划分
    data1 = data[data[:,0]==1]
    data1_test_len = int(len(data1) * test_size)
    data1_test = data1[:data1_test_len]
    data1_train = data1[data1_test_len:]

#将0和1的数据连接起来，形成测试集和训练集
    data_test = np.vstack((data0_test,data1_test))
    data_train = np.vstack((data0_train,data1_train))

#    将合并起来的数据随机排序，将数据中的0和1全部打乱-----自己学习并了解下将数据随机打乱的方法
    np.random.seed(0)
    data_test_random = data_test[np.random.permutation(range(0,len(data_test)))]
    data_train_random = data_train[np.random.permutation(range(0,len(data_train)))]

    return data_test_random,data_train_random


def calc_woe(data_x,data_y,range_list):
    train_woe = []
    start = -1
    end = -1
    y_0_count, y_1_count = np.bincount(data_y.astype(np.int)).tolist()  # 计数numpy数组中各值的数量
    for value in range_list[1:]:
        start = end
        end = value
        good, bad = np.bincount(data_y[np.logical_and(data_x>start, data_x<=end)].astype(np.int)).tolist()
        _woe = np.log((bad/y_1_count)/(good/y_0_count))
        woe_value = float(_woe)
        train_woe.append([woe_value, [start, end]])
    return train_woe


